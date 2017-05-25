# Compilation of CGAL, PGRouting and OSM2pgrouting

# Update and apt-get basic packages
apt-get update \
    && apt-get install -y \
	       cmake \
	       libboost-dev \
	       libboost-thread-dev \
	       libgmp3-dev \
	       libmpfr-dev \
         expat \
         libexpat1-dev \
         libboost-program-options-dev


# Untar
cd src ; tar -xvf CGAL-${CGAL_VERSION}.tar.gz ; cd ..
cd src ; tar -xvf v${PGROUTING_VERSION}.tar.gz ; cd ..
cd src ; tar -xvf v${OSM2PGR_VERSION}.tar.gz ; cd ..


# Compilation of CGAL
cd src/cgal-releases-CGAL-${CGAL_VERSION}
mkdir build
cd build
cmake ..
make
make install
ldconfig
cd ../../..


# Compilation of PGRouting
cd src/pgrouting-${PGROUTING_VERSION}
mkdir build
cd build
cmake ..
make
make install
ldconfig
cd ../../..


# Compilation of osm2pgrouting
cd src/osm2pgrouting-${OSM2PGR_VERSION}
mkdir build
cd build
cmake .. -DBOOST_ROOT:PATH=/local/projects/rel-boost-1.58.0
make
make install
ldconfig
cd ../../..


# Clean up
rm -Rf /usr/local/src
