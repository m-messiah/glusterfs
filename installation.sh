#!/bin/bash

#CLEAN=
#make clean || CLEAN="make clean"
#./autogen.sh
#./configure --prefix=/usr \
#--build=x86_64-pc-linux-gnu \
#--host=x86_64-pc-linux-gnu \
#--mandir=/usr/share/man \
#--infodir=/usr/share/info \
#--datadir=/usr/share \
#--sysconfdir=/etc \
#--localstatedir=/var/lib \
#--libdir=/usr/lib \
#--disable-dependency-tracking \
#--enable-fuse-client \
#--disable-ibverbs \
#--disable-static \
#--enable-georeplication \
##--disable-bdb \
#--docdir=/usr/share/doc/glusterfs \
LDFLAGS=-L/usr/local/lib \
CFLAGS="-O3 -pipe -mmmx -msse2 -msse3 -mssse3" \
CXXFLAGS="${CFLAGS}"
#$CLEAN
make || exit 1
#make uninstall || exit 1
make install || exit 2
#rm -f /usr/sbin/glusterfs
#cp /usr/sbin/glusterfs{d,}
