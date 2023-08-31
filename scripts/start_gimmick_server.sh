#!/bin/sh

export LD_LIBRARY_PATH=/home/nao/gimmick/python3.10/lib:/home/nao/gimmick/opt/lib:/home/nao/gimmick/opt/OpenBLAS/lib:/home/nao/gimmick/cross/lib

export LD_PRELOAD=/data/home/nao/gimmick/python3.10/lib/python3.10/site-packages/mediapipe/python/_framework_bindings.cpython-310-i386-linux-gnu.so:/usr/lib/libffi.so.6


/home/nao/gimmick/python3.10/bin/python3 /home/nao/gimmick/test/mediapipe_server/mp_server.py
