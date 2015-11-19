mkdir log 2>/dev/null

if [ $# -ne 3 ]; then
   echo "Please pass Test name for logfile (to sync log files when executing from different machines)."
   echo "also parallel clients number"
   echo "also pass query id to execute (99 for random)"
   exit 1
fi


export testName=$1
export parallelClients=$2
export query2run=$3
export neoUrl=localhost
export nodeCount=2000000
export printResults=N
export countOrRes=R

date
echo Starting stress test
./neo4jStressTestRun_clientLimit.sh $testName  $neoUrl  $nodeCount  $printResults  $countOrRes  $parallelClients  $query2run
echo
date
