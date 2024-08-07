#!/bin/sh

unset PYTHONPATH
export LD_LIBRARY_PATH=/home/nao/gimmick/python3.10/lib:/home/nao/gimmick/opt/lib:/home/nao/gimmick/opt/OpenBLAS/lib:/home/nao/gimmick/cross/lib:/home/nao/gimmick/openssl3/lib

export LD_PRELOAD=/data/home/nao/gimmick/python3.10/lib/python3.10/site-packages/mediapipe/python/_framework_bindings.cpython-310-i386-linux-gnu.so:/usr/lib/libffi.so.6

# Make sure that the python encoding is utf-8 always.
PYTHONIOENCODING=utf8
export PYTHONIOENCODING

cd /home/nao/gimmick/test/scripts && /home/nao/gimmick/python3.10/bin/python3 -u ./main.py >& /home/nao/gimmick/test/scripts/client.log

