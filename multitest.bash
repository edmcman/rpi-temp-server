#!/usr/bin/env bash

DIR="${1:-logs}"
shift
N="${2:-20}"
shift

OTHERARGS=("$@")

mkdir -p "$DIR"

for n in $(seq $N)
do

    echo $n
    test -f "$DIR"/$n.log && continue

    sudo airodump-ng --background 1 --beacons --channel 11 wlxe84e0698f7fc -w "$DIR"/"capture$n" &
    sleep 1
    setsid bash ./test.bash "${OTHERARGS[@]}" | tee "$DIR"/$n.log

    echo Killing airodump-ng
    sudo killall airodump-ng
    sleep 1
    sudo killall -9 airodump-ng

done
