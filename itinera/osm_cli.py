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


import argparse
from osm_itinera import OsmItinera
from const import BBOX_DICT


def main():
    descr = "OSM itinera"
    arg_parser = argparse.ArgumentParser(description=descr)

    arg_parser.add_argument('bbox_zone', type=str, help='Bounding box zone')
    arg_parser.add_argument('--dbschema', type=str, help='New DB schema name')
    arg_parser.add_argument('--dropdb', help='Drop DB', action="store_true")

    args = arg_parser.parse_args()

    bbox_zone = args.bbox_zone

    osm_kargs = {}

    bbox_zone = BBOX_DICT[bbox_zone]

    if args.dbschema:
        osm_kargs['dbschema'] = args.dbschema

    if args.dropdb:
        osm_kargs['dropdb'] = args.dropdb

    osmIt = OsmItinera(bbox_zone)
    osmIt.run(**osm_kargs)

if __name__ == '__main__':
    main()
