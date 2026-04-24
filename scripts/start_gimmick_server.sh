#!/bin/sh

# SPDX-License-Identifier: BSD-2-Clause

export LD_LIBRARY_PATH=/home/nao/gimmick/python3.10/lib:/home/nao/gimmick/opt/lib:/home/nao/gimmick/opt/OpenBLAS/lib:/home/nao/gimmick/cross/lib

export LD_PRELOAD=/data/home/nao/gimmick/python3.10/lib/python3.10/site-packages/mediapipe/python/_framework_bindings.cpython-310-i386-linux-gnu.so:/usr/lib/libffi.so.6

# Make sure that the python encoding is utf-8 always.
PYTHONIOENCODING=utf8
export PYTHONIOENCODING

cd /home/nao/gimmick/test/mediapipe_server && /home/nao/gimmick/python3.10/bin/python3 -u ./mp_server.py >& /home/nao/gimmick/test/scripts/server.log
