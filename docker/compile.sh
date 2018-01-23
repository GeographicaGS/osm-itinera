# Compilation of CGAL, PGRouting and OSM2pgrouting

# Install osm2pgrouting prerequisites
apt-get update -y \
    && apt-get install -y \
	       cmake \
	       libboost-dev \
	       libboost-thread-dev \
	       libgmp3-dev \
	       libmpfr-dev \
         expat \
         libexpat1-dev \
         libboost-program-options-dev \
         libpqxx-dev \
         libosmium2-dev

# Install Python3 dependencies
apt-get update -y && apt-get install -y python3-pip
python3 -m pip install requests
python3 -m pip install psycopg2


# Untar
cd $ROOTDIR/src ; tar -xvf CGAL-${CGAL_VERSION}.tar.gz ; cd ..
cd $ROOTDIR/src ; tar -xvf v${PGROUTING_VERSION}.tar.gz ; cd ..
cd $ROOTDIR/src ; tar -xvf v${OSM2PGR_VERSION}.tar.gz ; cd ..


# Compilation of CGAL
cd $ROOTDIR/src/cgal-releases-CGAL-${CGAL_VERSION}
mkdir build
cd build
cmake ..
make
make install
ldconfig
cd ../../..


# Compilation of PGRouting
cd $ROOTDIR/src/pgrouting-${PGROUTING_VERSION}
mkdir build
cd build
cmake ..
make
make install
ldconfig
cd ../../..


# Compilation of osm2pgrouting
cd $ROOTDIR/src/osm2pgrouting-${OSM2PGR_VERSION}
mkdir build
cd build
cmake .. -DBOOST_ROOT:PATH=/local/projects/rel-boost-1.58.0
make
make install
ldconfig
cd ../../..

# Compilation of osm2pgrouting osmium restrictions tool
cd $ROOTDIR/src/osm2pgrouting-${OSM2PGR_VERSION}/tools/osmium
mkdir build
cd build
cmake ..
make
make install
ldconfig
cd ../../../../..

# Clean up
rm -Rf $ROOTDIR/src/*
