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
import requests
import subprocess
import psycopg2
import const
from contextlib import closing
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



class GetOsmDataError(Exception):
    pass

def composeOsmScript(bbox_coords, timeout=1000):
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
        
        osm_cfg = (timeout,) + bbox_coords
        
        return osm_script.format(*osm_cfg)
        
    except Exception as err:
        # print("Error composing osm script: {0}".format(err))
        raise GetOsmDataError("Error composing osm script: {0}".format(err))

def getOsmDataset(osm_script, osm_url=const.OVERPASS_API, chunk_size=1024, 
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
        # print("Error requesting osm data: {0}".format(err))
        raise GetOsmDataError("Error requesting osm data: {0}".format(err))

def createPgDb(dbase=const.PG_DATABASE, dbuser=const.PG_USER, dbpassw=const.PG_PASSWORD, 
    dbport=const.PG_PORT, dbhost=const.PG_HOST):
    """
    Create new PostGIS+PgRouting database

    """
    try:
        conn = None
        conn = psycopg2.connect(database="postgres", user="postgres",
                password=None, host=dbhost, port=dbport)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("DROP DATABASE IF EXISTS {0};".format(dbase))
        print("Database {0} removed".format(dbase))
        
        cur.execute("DROP USER IF EXISTS {0};".format(dbuser))
        cur.execute("CREATE USER {0} with password '{1}';".format(dbuser, dbpassw))
        print("User {0} created".format(dbuser))

        cur.execute("CREATE DATABASE {0} WITH OWNER {1};".format(dbase, dbuser))
        cur.close()
        conn.close()
        print("Database {0} created".format(dbase))

        conn = psycopg2.connect(database=dbase, user="postgres",
                password=None, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("CREATE EXTENSION postgis;")
        cur.execute("CREATE EXTENSION pgrouting;")
        print("Added PostGIS and PgRouting extensions to {0}".format(dbase))
        conn.commit()
        cur.close()
        conn.close()

    except Exception as err:
            raise GetOsmDataError("Database creation error: {0}".format(err))

def osmData2Pg(filepath=const.OSM_FILEPATH, dbase=const.PG_DATABASE, dbuser=const.PG_USER,
    dbpassw=const.PG_PASSWORD, dbport=const.PG_PORT, dbhost=const.PG_HOST):
    
    osm_cdm = ["osm2pgrouting", "--file", filepath, "--dbname", dbase, 
                "--user", dbuser, "--password", dbpassw, "--port", dbport, 
                "--host", dbhost, "--clean"]
    
    out, err = cmdCall(osm_cdm)
    if err:
        print("OSM data to postgres Error: {0}".format(err))
    else:
        print("OSM data to postgres: successfully process! (File: {0})".format(filepath))

def cmdCall(params):
    """
    Launch shell commands
    """
    try:
        cmd_call = subprocess.Popen(params, stderr=subprocess.PIPE)
        out, err = cmd_call.communicate()
        return(out, err)

    except ValueError as err:
        print("Invalid arguments: {0}".format(err))

    except Exception as err:
        print("Shell command error: {0}".format(err))

def cleanOsmData(filepath=const.OSM_FILEPATH):
    """
    Remove osm data file
    """
    try:
        if os.path.exists(filepath)
            os.remove(filepath)
            print("OSM file successfully removed from local folder...")

    except Exception as err:
        print("Error removing OSM downloaded file: {0}".format(err))

def run():
    # bbox_coords = (
    #     37.3282387449,
    #     -6.0597701657,
    #     37.4438529953,
    #     -5.88779199411,
    # )

    bbox_coords = (
        37.3424966101,
        -5.98360108474,
        37.347384398,
        -5.9750619501
    )
    
    try:
        if isinstance(bbox_coords, tuple) and len(bbox_coords) == 4:
            
            print("Composing OSM script...")
            osm_script = composeOsmScript(bbox_coords)
            
            print("Downloading OSM data...")
            osm_data = getOsmDataset(osm_script)
            
            print("OSM file sucessfully created!")
            
            print("Creating and preparing database...")
            createPgDb()
            
            print("Importing OSM data to PgSQL...")
            osmData2Pg()
            
            cleanOsmData()
            
            print("OSM to PGSQL sucessfully finshed!")
            
        else:
            print("BBOX data must be a tuple with 4 coords...")

    except Exception as err:
        print(err)

if __name__ == '__main__':
    run()


