#!/bin/bash

mpremote reset
(mpremote run main.py | tee mp.log)&

# kill mpremote on exit
trap "kill -- -$$" EXIT

URL="http://192.168.1.4/temp"

echo "test.bash: Waiting for the server to start"
sleep 10

n=1
while true
do
  echo "test.bash: Sleeping for $n seconds"
  sleep $n
  date
  echo "test.bash: Running wget"
  out=$(wget -q "$URL" -O /dev/stdout) || break
  echo "test.bash: Response: $out"
  n=$((n * 2))
done
