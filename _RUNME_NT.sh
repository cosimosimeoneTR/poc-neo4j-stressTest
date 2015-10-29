mkdir log 2>/dev/null
date
echo Starting stress test
./neo4jStressTestRun_NT.sh $1 $2
date
