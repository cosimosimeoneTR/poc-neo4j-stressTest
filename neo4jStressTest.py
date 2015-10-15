#!/usr/bin/python

import json
from py2neo import Graph, authenticate, Node
import time,random,sys

randCompany = random.randint(1, 1000)

#startTime = datetime.now()
startTime = time.time()

connectTo = sys.argv[1]
outConnectTo = connectTo

if connectTo == 'localhost':
   outConnectTo = connectTo+'-'+str(sys.argv[3])

#print str(sys.argv[1])+":7474"
authenticate(str(connectTo)+":7474", "neo4j", "neo4j123")
graph = Graph()


#results = graph.cypher.execute("MATCH (Company{companyName:'Cmp_1'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug LIMIT 60")
try:
   results = graph.cypher.execute("MATCH (Company{companyName:'Cmp_"+str(randCompany)+"'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug LIMIT 60")
except Exception as detail:
   print str(sys.argv[2])+' , '+str(outConnectTo)+str(' , 9999999999')+' , '+str(detail)

#print results
#print datetime.now() - startTime
print  str(sys.argv[2])+' , '+str(outConnectTo)+' , '+str(time.time() - startTime)

