#!/usr/bin/python

import json
from py2neo import Graph, authenticate, Node
import time,random,sys,string
from datetime import datetime

randCompany = random.randint(1, 1000)
query={}
query[0] = "MATCH (Company{companyName:'Cmp_#'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[1] = "MATCH (Drug{drugName:'Drg_#'})<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[2] = "MATCH (Company{attr1:'asqwdasdasda'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[3] = "MATCH (Company{attr9:'asqwdasdasda'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[4] = "MATCH (Drug{attr1:'asqwdasdasda'})<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[5] = "MATCH (Drug{attr9:'asqwdasdasda'})<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
rndQuery=random.randint(0, len(query)-1)
rndQueryVal=random.randint(0, 1000)
queryToRun = query[rndQuery].replace('#',str(rndQueryVal))

connectTo = sys.argv[1]
outConnectTo = connectTo

if connectTo == 'localhost':
   outConnectTo = connectTo+'-'+str(sys.argv[3])


startTime = time.time()
authenticate(str(connectTo)+":7474", "neo4j", "neo4j123")
graph = Graph()

try:
   results = graph.cypher.execute(queryToRun)
except Exception as detail:
   print str(sys.argv[2])+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999999')+','+str(detail)

print  str(sys.argv[2])+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(time.time() - startTime)
