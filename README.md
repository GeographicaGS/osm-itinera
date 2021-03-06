# OSM Itinera

### Prepare your config file.

Copy the config file and fill it with your settings.
```
$ cp config.example.env config.env
```
Now, you can edit this file using your favourite text editor.


### Build PgSQL container
Compile CGAL, PgRouting and Osm2pgrouting, and prepare Python packages over geographica/postgis:pleasant_yacare Docker image (PgSQL 10 / PostGIS 2.4):
```
$ docker-compose build --no-cache
```

### Get data from OSM and import to PgSQL
```
$ docker-compose up -d
$ docker-compose exec postgis python3 itinera/osm_cli.py sevilla_demo --dbschema sevilla_test --dropdb
```

### Usage help
```                               
usage: osm_cli.py [-h] [--dbschema DBSCHEMA] [--dropdb] [--wtype WTYPE]
                  bbox_zone

OSM itinera

positional arguments:
  bbox_zone            Bounding box zone

optional arguments:
  -h, --help           show this help message and exit
  --dbschema DBSCHEMA  New DB schema name
  --dropdb             Drop DB
  --wtype WTYPE        Ways type (default | car | bike | pedestrian)
```
