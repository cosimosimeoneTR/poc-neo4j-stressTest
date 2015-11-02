mkdir log 2>/dev/null
##### PAR1=test name PAR2=server location (localhost, 123.456.789.123, ec2-52-91-32-28.compute-1.amazonaws.com, whatever)
date
echo Starting stress test
./neo4jStressTestRun_NT.sh $1 $2
date
