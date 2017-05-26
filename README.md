# OSM Itinera

### Create data container for PgSQL
```
$ docker create --name osm_itinera_data -v /data debian /bin/true
```

### Prepare your config file.

Copy the config file and fill it with your settings.
```
$ cp config.example.env config.env
```
Now, you can edit this file using your favourite text editor.


### Build PgSQL container
Compile CGAL, PgRouting and Osm2pgrouting, and prepare Python packages over geographica/postgis:breezy_badger Docker image (PgSQL 9.6 / PostGIS 2.3):
```
$ docker-compose build
```

### Get data from OSM and import to PgSQL
```
$ docker-compose up -d
$ docker-compose exec postgis python3 /usr/src/app/osm_itinera.py
```
