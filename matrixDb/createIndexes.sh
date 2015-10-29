set -x
echo;echo;echo;
date
echo;echo;
neo4j-shell -c "create constraint on (e:entityA) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityB) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityC) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityD) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityE) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityF) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityG) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityH) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityI) assert e.id is unique;"
neo4j-shell -c "create constraint on (e:entityJ) assert e.id is unique;"

#watch 'date;neo4j-shell -c "schema ls"'
