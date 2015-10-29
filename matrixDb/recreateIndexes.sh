set -x
echo;echo;echo;
date
echo;echo;
./dropIndexes.sh
neo4j-shell -c "schema ls"
./createIndexes.sh
