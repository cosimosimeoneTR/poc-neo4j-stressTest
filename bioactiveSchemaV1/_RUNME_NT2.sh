mkdir log 2>/dev/null
date
echo Starting stress test
echo
echo
./neo4jStressTestRun_NT2sh $1 $2
echo
echo
echo
date
