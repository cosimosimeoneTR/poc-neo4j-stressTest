#!/bin/bash

shopt -s expand_aliases
alias echoi='echo `date +%Y-%m-%d\ %H:%M.%S` -INFO-'

mkdir log 2>/dev/null


if [ $# -ne 6 ]; then
   echo "Please pass Test name for logfile (to sync log files when executing from different machines)."
   echo "also pass neo4j URL"
   echo "also pass your collection node number"
   echo "also pass if you want results in csv (Y / N)"
   echo "also pass if you want count or results to be printed (C / R)"
   echo "also pass parallel client number"
   exit 1
fi
export testName=$1
export neoUrl=$2
export nodeCount=$3
export printResults=$4
export countOrRes=$5
export parallelClients=$6

export myLOGFILE="log/$1.csv"
export arch=`uname -a | cut -d " " -f 1`
export pids=""
export procs=0


export instanceType=`wget -q -O - http://instance-data/latest/meta-data/instance-type || echo REMOTE`
#echo $instanceType

#touch $myLOGFILE
echo "Test name,Type and executerId,#paralClients,Date time,Connected to and instance type,Query id,Execution Time (seconds),Error,Query,Results" >> $myLOGFILE

echo -n "Clients running: "
for j in `seq 1 $parallelClients`; do
   #echoi "   ./neo4jStressTest_NT.py $neoUrl $parallelClients $instanceType $j $printResults $nodeCount $countOrRes $testName "
   echo -n "#"
   nohup ./neo4jStressTest_NT.py $neoUrl $parallelClients $instanceType $j $printResults $nodeCount $countOrRes $testName >> $myLOGFILE 2>&1 &
   pids="$pids $!"

   let procs=procs+1
   # Don't stress poor Window$...
   if [ "$arch" != "Linux" ] && [ "$procs" -gt "399" ]; then
     sleep 3
     procs=0
     echoi "sleeping..."
   fi

done
echo

echoi waiting for pids
wait $pids
echoi pids ended
pids=""

export best=`grep -v Execution $myLOGFILE  | cut -d"," -f 7 | sort -n |head`
export worst=`grep -v Execution $myLOGFILE | cut -d"," -f 7 | sort -n -r | head`
echoi bests=$best
echoi worst=$worst

