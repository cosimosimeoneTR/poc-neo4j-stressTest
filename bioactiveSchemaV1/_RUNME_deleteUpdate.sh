mkdir log 2>/dev/null

if [ $# -ne 3 ]; then
   echo "Please pass Test name for logfile (to sync log files when executing from different machines)."
   echo "also parallel clients number"
   echo "also test type: U to test updates, D to delete nodes, DR to test relationships"
   exit 1
fi


export testName=$1
export parallelClients=$2
export updateOrDelete=$3
export neoUrl=localhost
export nodeCount=2000000

date
echo Starting stress test
./neo4jStressTestRun_deleteUpdate.sh $testName  $neoUrl  $nodeCount  $parallelClients $updateOrDelete
echo
date
