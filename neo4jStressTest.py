#!/usr/bin/python

import json
from py2neo import Graph, authenticate, Node
import time,random,sys

randCompany = random.randint(1, 1000)

#startTime = datetime.now()
startTime = time.time()

print str(sys.argv[1])+":7474"
authenticate(str(sys.argv[1])+":7474", "neo4j", "neo4j123")
graph = Graph()


#results = graph.cypher.execute("MATCH (Company{companyName:'Cmp_1'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug LIMIT 60")
results = graph.cypher.execute("MATCH (Company{companyName:'Cmp_"+str(randCompany)+"'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug LIMIT 60")

#print results
#print datetime.now() - startTime
print  str(sys.argv[2])+' , '+str(time.time() - startTime)
