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

date
echo Starting stress test
./neo4jStressTestRun_deleteUpdate.sh $testName  $neoUrl  $nodeCount  $parallelClients
echo
date
