#!/bin/bash

#PM="${1?Please specify the pm setting}"
MAX="${1:-3600}"
echo "test.bash: MAX=$MAX"

set -e

mpremote reset
echo "test.bash: Waiting for reset"
sleep 10
#mpremote cp <(echo -n "$PM") :pm
(mpremote run main.py | tee mp.log)&

set +e

# kill mpremote on exit
trap "kill -- -$$" EXIT

URL="http://192.168.1.4/temp"

echo "test.bash: Waiting for the server to start"
sleep 10

n=1
while [ $n -le $MAX ]
do
  echo "test.bash: Sleeping for $n seconds"
  echo "Current time: $(date)"
  echo "Sleeping until $(date -d "+$n seconds")"
  sleep $n
  echo "test.bash: Running wget"
  out=$(wget -q "$URL" -O /dev/stdout) || (echo "test.bash: Failed at $n seconds"; false) || exit 1
  echo "test.bash: Response: $out"
  n=$((n * 2))
done

echo "test.bash: Test succeeded"
exit 0