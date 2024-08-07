#!/bin/sh

# Script to sync between git repo and the robot

if [ $# -lt 1 ]; then
    echo "Usage $0 <host>"
    exit 2
fi

ROBOT_ADDRESS=$1
ROBOT_USERNAME=nao

SCRIPT_DIR=$(cd $(dirname "$0") && pwd)
SRC_DIR=$(dirname $SCRIPT_DIR)
SSH_BASE=$ROBOT_USERNAME@$ROBOT_ADDRESS
DEST_DIR=$SSH_BASE:

DEST_PROGS="gimmick/test"
ssh $SSH_BASE mkdir -p $DEST_PROGS

RSYNC=$(which rsync)
SYNC_ARGS="-avdz"
${RSYNC:?"rysnc not found!"} $SYNC_ARGS -f '- *.pyc' -f '- .#*' "$SRC_DIR/src/nao/app/scripts" ${DEST_DIR}${DEST_PROGS}
$RSYNC $SYNC_ARGS "$SRC_DIR/src/mediapipe_server" ${DEST_DIR}${DEST_PROGS}

DEST_SCRIPTS="gimmick/scripts"
ssh $SSH_BASE mkdir -p "$DEST_SCRIPTS"

for script in start_gimmick_client.sh; do
    $RSYNC $SYNC_ARGS "$SRC_DIR/scripts/$script" ${DEST_DIR}${DEST_SCRIPTS}
done
