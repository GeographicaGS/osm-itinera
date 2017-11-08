FROM geographica/postgis:nimble_newt

MAINTAINER Cayetano Benavent "cayetano.benavent@geographica.gs"


# Environment
ENV PGROUTING_VERSION 2.5.1
ENV CGAL_VERSION 4.9
ENV OSM2PGR_VERSION 2.3.1

# Sources
ADD https://github.com/pgRouting/pgrouting/archive/v${PGROUTING_VERSION}.tar.gz $ROOTDIR/src/
ADD https://github.com/CGAL/cgal/archive/releases/CGAL-${CGAL_VERSION}.tar.gz $ROOTDIR/src/
ADD https://github.com/pgRouting/osm2pgrouting/archive/v${OSM2PGR_VERSION}.tar.gz $ROOTDIR/src/
ADD compile.sh $ROOTDIR/src/

# Compilation
RUN chmod 777 $ROOTDIR/src/compile.sh
RUN $ROOTDIR/src/compile.sh

WORKDIR /usr/src/app/
