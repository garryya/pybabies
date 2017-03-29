#!/usr/bin/python -B

import sys
import struct
import dis
import marshal


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        magic = f.read(4)
        timestamp = f.read(4)
        code = f.read()


    magic = struct.unpack('<H', magic[:2])
    timestamp = struct.unpack('<H', timestamp)
    code = marshal.loads(code)

    print()