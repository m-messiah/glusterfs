#!/bin/bash

./autogen.sh
./configure --prefix=/usr \
--build=i686-pc-linux-gnu \
--host=i686-pc-linux-gnu \
--mandir=/usr/share/man \
--infodir=/usr/share/info \
--datadir=/usr/share \
--sysconfdir=/etc \
--localstatedir=/var/lib \
--libdir=/usr/lib \
--disable-dependency-tracking \
--enable-fuse-client \
--disable-ibverbs \
--disable-static \
--enable-georeplication \
--disable-bdb \
--docdir=/usr/share/doc/glusterfs\
CFLAGS="-O3 -pipe"\
CXXFLAGS="${CFLAGS}"
make clean
make
make install
