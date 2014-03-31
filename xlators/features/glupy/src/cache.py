import sys
from uuid import UUID
from gluster import *

# Caching example.


class Cache(object):
    def __init__(self):
        self.table = dict()

    def __contents__(self, key):
        return key in self.table

    def is_valid(self):
        return True

    def get(self, key):
        return self.table.get(key)

    def set(self, key, name):
        self.table[key] = name

    def remove(self, key):
        del self.table[key]


cache = Cache()

# TBD: we need a better way of handling per-request data (frame->local in C).
dl.get_id.restype = c_long
dl.get_id.argtypes = [POINTER(call_frame_t)]


def uuid2str(gfid):
    return str(UUID(''.join(map("{0:02x}".format, gfid))))


class xlator(Translator):
    def __init__(self, c_this):
        self.requests = {}
        Translator.__init__(self, c_this)

    def lookup_fop(self, frame, this, loc, xdata):
        pargfid = uuid2str(loc.contents.pargfid)
        print "lookup FOP: {0}:{1}".format(pargfid, loc.contents.name)
        # Check the cache.
        key = dl.get_id(frame)
        self.requests[key] = (pargfid, loc.contents.name[:])
        if (pargfid + loc.contents.name) in cache and cache.is_valid():
            print "short-circuiting for {0}:{1}".format(pargfid,
                                                        loc.contents.name)
            #dl.unwind_lookup(frame,0,this,-1,2,None,None,None,None)
            # Get from cache
            # return 0
        # TBD: get real child xl from init, pass it here
        dl.wind_lookup(frame, POINTER(xlator_t)(), loc, xdata)
        return 0

    def lookup_cbk(self, frame, cookie, this, op_ret, op_errno, inode, buf,
                   xdata, postparent):
        print "lookup CBK: {0:d} ({1:d})".format(op_ret, op_errno)
        key = dl.get_id(frame)
        pargfid, name = self.requests[key]
        # Update the cache.
        if op_ret == 0:
            print "found {0}, update cache".format(name)
            cache.set(pargfid + name, None)
        elif op_errno == 2:  # ENOENT
            print "failed to find {0}, remove from cache".format(name)
            if pargfid in cache:
                cache.remove(pargfid)
        dl.unwind_lookup(frame, cookie, this, op_ret, op_errno,
                         inode, buf, xdata, postparent)
        return 0

    def create_fop(self, frame, this, loc, flags, mode, umask, fd, xdata):
        pargfid = uuid2str(loc.contents.pargfid)
        print "create FOP: {0}:{1}".format(pargfid, loc.contents.name)
        key = dl.get_id(frame)
        self.requests[key] = (pargfid, loc.contents.name[:])
        # TBD: get real child xl from init, pass it here
        dl.wind_create(frame, POINTER(xlator_t)(), loc, flags, mode, umask, fd,
                       xdata)
        return 0

    def create_cbk(self, frame, cookie, this, op_ret, op_errno, fd, inode,
                   buf, preparent, postparent, xdata):
        print "create CBK: {0:d} ({1:d})".format(op_ret, op_errno)
        key = dl.get_id(frame)
        pargfid, name = self.requests[key]
        # Update the cache.
        if op_ret == 0:
            print "created {0:s}, removing from cache".format(name)
            if (pargfid + name) in cache:
                cache.set(pargfid + name, buf)
        del self.requests[key]
        dl.unwind_create(frame, cookie, this, op_ret, op_errno, fd, inode, buf,
                         preparent, postparent, xdata)
        return 0

