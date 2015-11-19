mkdir log 2>/dev/null

if [ $# -ne 2 ]; then
   echo "Please pass Test name for logfile (to sync log files when executing from different machines)."
   echo "also parallel clients number"
   exit 1
fi


export testName=$1
export parallelClients=$2
export neoUrl=localhost
export nodeCount=2000000
export printResults=N
export countOrRes=R

date
echo Starting stress test
echo
echo
./neo4jStressTestRun_clientLimit.sh $testName  $neoUrl  $nodeCount  $printResults  $countOrRes  $parallelClients
echo
echo
echo
date
