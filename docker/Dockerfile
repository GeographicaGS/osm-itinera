FROM geographica/postgis:breezy_badger

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

# Install Python3 dependencies
RUN apt-get update -y && apt-get install -y python3-pip
RUN python3 -m pip install requests
RUN python3 -m pip install psycopg2

# Install osm2pgrouting prerequisites
RUN apt-get update -y && apt-get install -y expat \
  libexpat1-dev \
  libboost-dev \
  libboost-program-options-dev \
  libpqxx-dev

# Compilation
RUN chmod 777 src/compile.sh
RUN src/compile.sh

WORKDIR /usr/src/app/
