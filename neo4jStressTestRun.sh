#!/bin/bash

if [ $# -ne 2 ]; then
   echo "Please pass Test name for logfile (to sync log files when executing from different machines)."
   echo "(single word will do it)"
   echo "also pass neo4j URL"
   exit 1
fi
export testName=$1
export neoUrl=$2

#export LOGFILE="log/neo4jStressTestRunLog_$1.`date +%Y%m%d%H%M`.log"
export LOGFILE="log/neo4jStressTestRunLog_$1.log"
export arch=`uname -a | cut -d " " -f 1`
pids=""

export instanceType=`wget -q -O - http://instance-data/latest/meta-data/instance-type || echo REMOTE`
#echo $instanceType


for i in `seq 1 2`; do
   let loopNums=10**$i
   for i in `seq 1 $loopNums`; do
      ./neo4jStressTest.py $neoUrl $loopNums $instanceType >> $LOGFILE &
      #pids="$pids $!"
      # Don't stress poor Window$...
      if [ "$arch" != "Linux" ]
      then
        sleep 1
      fi
   done

   #wait $pids
done
