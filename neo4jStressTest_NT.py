#!/usr/bin/python

import json
from py2neo import Graph, authenticate, Node
import time,random,sys,string
from datetime import datetime

connectTo = sys.argv[1]
outConnectTo = connectTo

if connectTo == 'localhost':
   outConnectTo = connectTo+'-'+str(sys.argv[3])

randCompany = random.randint(1, 1000)
query={}
query[0] = "MATCH (Company:Company{companyName:'Cmp_#'})-[x:CMP2DRG]->(Drug)<-[r:TRL2DRG1]-(Trial)-[z:TRL2DRG2]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[1] = "MATCH (Drug:Drug{drugName:'Drg_#'})<-[r:TRL2DRG1]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[2] = "MATCH (Company:Company{attr1:'asqwdasdasda'})-[x:CMP2DRG]->(Drug)<-[r:TRL2DRG2]-(Trial)-[z:TRL2DRG1]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[3] = "MATCH (Company:Company{attr9:'asqwdasdasda'})-[x:CMP2DRG]->(Drug)<-[r:TRL2DRG1]-(Trial)-[z:TRL2DRG2]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[4] = "MATCH (Drug:Drug{attr1:'asqwdasdasda'})<-[r:TRL2DRG2]-(Trial)-[z:TRL2DRG3]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[5] = "MATCH (Drug:Drug{attr9:'asqwdasdasda'})<-[r:TRL2DRG3]-(Trial)-[z:TRL2DRG1]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[6] = "MATCH (n:Company) RETURN n LIMIT 2"

# Not congestion it on connections...
# So, pone N seconds delay: wait x seconds, connect, wait N-x seconds, and run the query ;-)
# wait x seconds...
N=10
rndWait=random.randint(0, N)
time.sleep(rndWait)

# ... connect ...
authenticate(str(connectTo)+":7474", "neo4j", "neo4j123")
graph = Graph()

# ... wait N-x seconds ...
time.sleep(N-rndWait)

# and run the queries
for myIndex in range(0,int(sys.argv[2])):
   startTime = time.time()
   try:
      rndQuery=random.randint(0, len(query)-1)
      rndQueryVal=random.randint(0, 1000)
      queryToRun = query[rndQuery].replace('#',str(rndQueryVal))

      results = graph.cypher.execute(queryToRun)
   except Exception as detail:
      print 'NT'+str(sys.argv[2])+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999999')+','+str(detail)
   else:
      print 'NT'+str(sys.argv[2])+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(time.time() - startTime)
