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
from contextlib import closing

PG_DATABASE = os.environ['PG_DATABASE']
PG_USER = os.environ['PG_USER']
PG_PASSWORD = os.environ['PG_PASSWORD']
PG_HOST = os.environ['PG_HOST']
PG_PORT = os.environ['PG_PORT']
OSM_FILEPATH = '/tmp/output_osm.osm'
OVERPASS_API = 'http://overpass-api.de/api/interpreter'


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

def getOsmDataset(osm_script, osm_url=OVERPASS_API, chunk_size=1024, 
    filepath=OSM_FILEPATH):
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

def osmData2Pg(filepath=OSM_FILEPATH, dbase=PG_DATABASE, dbuser=PG_USER,
    dbpassw=PG_PASSWORD, dbport=PG_PORT, dbhost=PG_HOST):
    
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
            
            osmData2Pg()
            print("OSM to PGSQL sucessfully finshed!")
            
        else:
            print("BBOX data must be a tuple with 4 coords...")

    except Exception as err:
        print(err)

if __name__ == '__main__':
    run()


