set -x
echo;echo;echo;
date
echo;echo;
neo4j-shell -c "drop index on :Drug(drugName)         ;"
neo4j-shell -c "drop index on :Drug(attr1)            ;"
neo4j-shell -c "drop index on :Drug(attr9)            ;"
neo4j-shell -c "drop index on :Drug(drugId)           ;"
neo4j-shell -c "drop index on :Company(companyName)   ;"
neo4j-shell -c "drop index on :Company(attr1)         ;"
neo4j-shell -c "drop index on :Company(attr9)         ;"
neo4j-shell -c "drop index on :Disease(diseaseId)     ;"
neo4j-shell -c "drop index on :Disease(id)            ;"
neo4j-shell -c "drop index on :Disease(attr1)         ;"
neo4j-shell -c "drop index on :Disease(diseaseName)   ;"
neo4j-shell -c "drop index on :trial(trialId)         ;"
neo4j-shell -c "drop index on :trial(trialName)       ;"
neo4j-shell -c "drop index on :trial(attr5)           ;"
watch 'date;neo4j-shell -c "schema ls"'
