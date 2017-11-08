# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2017.
#  cayetano.benavent@geographica.gs
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import os
import logging
import requests
import subprocess
import psycopg2
import const
from contextlib import closing
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



class GetOsmDataError(Exception):
    pass

class Logger:

    def __init__(self, level=logging.INFO):
        logfmt = "[%(asctime)s - %(levelname)s] - %(message)s"
        dtfmt = "%Y-%m-%d %I:%M:%S"
        logging.basicConfig(level=level, format=logfmt, datefmt=dtfmt)

    def get(self):
        return logging.getLogger()

class OsmItinera:

    def __init__(self, bbox_coords, verbose=True):
        if not verbose:
            lg = Logger(level=logging.ERROR)
        else:
            lg = Logger()

        self.__logger = lg.get()

        self.__bbox_coords = bbox_coords

    def composeOsmScript(self, timeout=1000):
        """
        Composing OpenStreetMap Overpass API script
        to get data by bounding box
        """
        try:
            osm_script = """
                <osm-script timeout="{0}">
                    <union into="_">
                        <bbox-query s="{1}" w="{2}" n="{3}" e="{4}"/>
                        <recurse type="up"/>
                        <recurse type="down"/>
                    </union>
                    <print limit="" mode="meta" order="id"/>
                </osm-script>"""

            osm_cfg = (timeout,) + self.__bbox_coords

            return osm_script.format(*osm_cfg)

        except Exception as err:
            self.__logger.error("Error composing osm script: {0}".format(err))
            raise GetOsmDataError("Error composing osm script: {0}".format(err))

    def getOsmDataset(self, osm_script, osm_url=const.OVERPASS_API, chunk_size=1024,
        filepath=const.OSM_FILEPATH):
        """
        Make request to get osm datafile
        and write to disk
        """
        try:
            headers = {'Content-Type': 'application/xml'}

            with closing(requests.post(url=osm_url, data=osm_script,
                headers=headers, stream=True)) as resp:

                resp.raise_for_status()

                if resp.status_code == 200:
                    with open(filepath, 'wb') as osm_file:
                        for chunk in resp.iter_content(chunk_size):
                            osm_file.write(chunk)

        except Exception as err:
            self.__logger.error("Error requesting osm data: {0}".format(err))
            raise GetOsmDataError("Error requesting osm data: {0}".format(err))

    def createPgDb(self, dbschema, dbdrop, dbase=const.PG_DATABASE, dbuser=const.PG_USER, dbpassw=const.PG_PASSWORD,
        dbport=const.PG_PORT, dbhost=const.PG_HOST):
        """
        Create new PostGIS+PgRouting database

        """
        try:
            conn = None
            if dbdrop:
                conn = psycopg2.connect(database="postgres", user="postgres",
                        password=None, host=dbhost, port=dbport)

                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()

                cur.execute("DROP DATABASE IF EXISTS {0};".format(dbase))
                self.__logger.info("Database {0} removed".format(dbase))

                cur.execute("DROP USER IF EXISTS {0};".format(dbuser))
                cur.execute("CREATE USER {0} with password '{1}';".format(dbuser, dbpassw))
                self.__logger.info("User {0} created".format(dbuser))

                cur.execute("CREATE DATABASE {0} WITH OWNER {1};".format(dbase, dbuser))
                cur.close()
                conn.close()
                self.__logger.info("Database {0} created".format(dbase))

            conn = psycopg2.connect(database=dbase, user="postgres",
                    password=None, host=dbhost, port=dbport)
            cur = conn.cursor()
            cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
            cur.execute("CREATE EXTENSION IF NOT EXISTS pgrouting;")
            cur.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
            cur.execute("CREATE SCHEMA IF NOT EXISTS {0} AUTHORIZATION {1};".format(dbschema, dbuser))
            self.__logger.info("Added PostGIS and PgRouting extensions to {0}".format(dbase))

            conn.commit()
            cur.close()
            conn.close()

        except Exception as err:
            self.__logger.error("Database creation error: {0}".format(err))
            raise GetOsmDataError("Database creation error: {0}".format(err))

    def osmData2Pg(self, mapconfig, dbschema, filepath=const.OSM_FILEPATH,
        dbase=const.PG_DATABASE, dbuser=const.PG_USER, dbpassw=const.PG_PASSWORD,
        dbport=const.PG_PORT, dbhost=const.PG_HOST):

        osm_cdm = [
            "osm2pgrouting", "--file", filepath, "--dbname", dbase, "--conf",
            mapconfig, "--user", dbuser, "--password", dbpassw, "--port", dbport,
            "--host", dbhost, "--schema", dbschema, "--clean", "--addnodes",
            "--tags", "--attributes"
        ]

        out, err = self.__cmdCall(osm_cdm)
        if err:
            self.__logger.error("OSM data to postgres message: {0}".format(err))
        else:
            self.__logger.info("OSM data to postgres: successfully process! (File: {0})".format(filepath))

    def __cmdCall(self, params):
        """
        Launch shell commands
        """
        try:
            cmd_call = subprocess.Popen(params, stderr=subprocess.PIPE)
            out, err = cmd_call.communicate()
            return(out, err)

        except ValueError as err:
            self.__logger.error("Invalid arguments: {0}".format(err))

        except Exception as err:
            self.__logger.error("Shell command error: {0}".format(err))

    def cleanOsmData(self, filepath=const.OSM_FILEPATH):
        """
        Remove osm data file
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.__logger.info("OSM file successfully removed from local folder...")

        except Exception as err:
            self.__logger.error("Error removing OSM downloaded file: {0}".format(err))

    def run(self, dbschema="osm", dropdb=False, mapconfig=const.MAPCFG_DICT.get("default", None)):

        try:
            if isinstance(self.__bbox_coords, tuple) and len(self.__bbox_coords) == 4:

                self.__logger.info("Composing OSM script...")
                osm_script = self.composeOsmScript()

                self.__logger.info("Downloading OSM data...")
                osm_data = self.getOsmDataset(osm_script)

                self.__logger.info("OSM file sucessfully created!")

                self.__logger.info("Creating and preparing database...")
                self.createPgDb(dbschema, dropdb)

                self.__logger.info("Importing OSM data to PgSQL...")
                self.osmData2Pg(mapconfig, dbschema)

                self.cleanOsmData()

                self.__logger.info("OSM to PGSQL sucessfully finshed!")

            else:
                self.__logger.error("BBOX data must be a tuple with 4 coords...")

        except Exception as err:
            self.__logger.error(err)
