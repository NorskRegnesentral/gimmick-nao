#!/bin/sh

source ~/rosa/scripts/activate-py2zqm.sh

# Make sure that the python encoding is utf-8 always.
PYTHONIOENCODING=utf8
export PYTHONIOENCODING

cd /home/nao/gimmick/test/scripts && python2 -u ./main.py >& /home/nao/gimmick/test/scripts/client.log
