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


PG_DATABASE = os.environ['PG_DATABASE']
PG_USER = os.environ['PG_USER']
PG_PASSWORD = os.environ['PG_PASSWORD']
PG_HOST = os.environ['PG_HOST']
PG_PORT = os.environ['PG_PORT']
OSM_FILEPATH = '/tmp/output_data.osm'
OVERPASS_API = 'http://overpass-api.de/api/interpreter'

folder_path = os.path.dirname(__file__)

MAPCFG_DICT = {
    'default': os.path.join(folder_path, 'mapconfig/mapconfig.xml'),
    'car': os.path.join(folder_path, 'mapconfig/mapconfig_car.xml'),
    'bikes':os.path.join(folder_path, 'mapconfig/mapconfig_bikes.xml')
}

BBOX_DICT = {
    'sevilla': (
        37.3282387449,
        -6.0597701657,
        37.4438529953,
        -5.88779199411,
    ),
    'sevilla_demo': (
        37.3424966101,
        -5.98360108474,
        37.347384398,
        -5.9750619501
    ),
    'bcn_demo': (
        41.3860722001,
        2.10899098555,
        41.4844881298,
        2.2223547892
    ),
    'bcn': (
        41.26684,
        1.97180,
        41.55818,
        2.26478
    )
}
