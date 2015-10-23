#!/bin/bash

mkdir log 2>/dev/null


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
export pids=""
export procs=0


export instanceType=`wget -q -O - http://instance-data/latest/meta-data/instance-type || echo REMOTE`
#echo $instanceType


for i in `seq 1 3`; do
   let loopNums=10**$i
   for i in `seq 1 $loopNums`; do
      echo RUN $i
      ./neo4jStressTest.py $neoUrl $loopNums $instanceType >> $LOGFILE &
      pids="$pids $!"
      let procs=procs+1
      # Don't stress poor Window$...
      if [ "$arch" != "Linux" ] && [ "$procs" -gt "399" ]; then
        sleep 3
        procs=0
        #echo "sleeping..."
      fi
   done

   echo waiting for $pids
   wait $pids
   pids=""
done

