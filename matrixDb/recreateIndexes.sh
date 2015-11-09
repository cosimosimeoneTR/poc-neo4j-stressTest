export databaseDir=$1

if [ $# -ne 1 ]; then
   echo "Please pass database dir as parameter"
   exit 1
fi

set -x
echo;echo;echo;
date
echo;echo;
./dropIndexes.sh $1
neo4j-shell -c "schema ls"
./createIndexes.sh $1
