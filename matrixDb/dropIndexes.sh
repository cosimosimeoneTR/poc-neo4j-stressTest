export databaseDir=$1

if [ $# -ne 1 ]; then
   echo "Please pass database dir as parameter"
   exit 1
fi

set -x
echo;echo;echo;
date
echo;echo;
neo4j-shell  -path $1  -c "drop constraint on (e:entityA) assert e.id is unique;"
neo4j-shell  -path $1  -c "drop constraint on (e:entityB) assert e.id is unique;"
neo4j-shell  -path $1  -c "drop constraint on (e:entityC) assert e.id is unique;"
neo4j-shell  -path $1  -c "drop constraint on (e:entityD) assert e.id is unique;"
neo4j-shell  -path $1  -c "drop constraint on (e:entityE) assert e.id is unique;"
###neo4j-shell  -path $1  -c "drop constraint on (e:entityF) assert e.id is unique;"
###neo4j-shell  -path $1  -c "drop constraint on (e:entityG) assert e.id is unique;"
###neo4j-shell  -path $1  -c "drop constraint on (e:entityH) assert e.id is unique;"
###neo4j-shell  -path $1  -c "drop constraint on (e:entityI) assert e.id is unique;"
###neo4j-shell  -path $1  -c "drop constraint on (e:entityJ) assert e.id is unique;"

date
neo4j-shell  -path $1  -c "schema ls"

#watch 'date;neo4j-shell -c "schema ls"'
