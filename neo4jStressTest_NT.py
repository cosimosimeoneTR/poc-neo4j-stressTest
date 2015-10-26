#!/usr/bin/python

import json
from py2neo import Graph, authenticate, Node
import time,random,sys,string
from datetime import datetime
import signal

debug=0

connectTo    =sys.argv[1]
numParallel  =sys.argv[2]
instanceType =sys.argv[3]
parallelGrp  =sys.argv[4]

############################################################
def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    print 'NT'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999888')+','+str(detail)
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)
############################################################

if debug==1: print "DBG-START"

outConnectTo = connectTo

if connectTo == 'localhost':
   outConnectTo = connectTo+'-'+str(instanceType)
   if debug==1: print "DBG-outConnectTo="+str(outConnectTo)

randCompany = random.randint(1, 1000)
query={}
query[0] = "MATCH (Company:Company{companyName:'Cmp_#'})-[x:CMP2DRG]->(Drug)<-[r:TRL2DRG1]-(Trial)-[z:TRL2DRG2]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[1] = "MATCH (Drug:Drug{drugName:'Drg_#'})<-[r:TRL2DRG1]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[2] = "MATCH (Company:Company{attr1:'asqwdasdasda'})-[x:CMP2DRG]->(Drug)<-[r:TRL2DRG2]-(Trial)-[z:TRL2DRG1]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[3] = "MATCH (Company:Company{attr9:'asqwdasdasda'})-[x:CMP2DRG]->(Drug)<-[r:TRL2DRG1]-(Trial)-[z:TRL2DRG2]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug "
query[4] = "MATCH (Drug:Drug{attr1:'asqwdasdasda'})<-[r:TRL2DRG2]-(Trial)-[z:TRL2DRG3]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[5] = "MATCH (Drug:Drug{attr9:'asqwdasdasda'})<-[r:TRL2DRG3]-(Trial)-[z:TRL2DRG1]->(anotherDrug) RETURN Drug,Trial,anotherDrug "
query[6] = "MATCH (n:Company) RETURN n LIMIT 2"
query[7] = "MATCH (n:Drug{drunName:'Drg_1'}) RETURN n"
query[8] = "MATCH (n:Company{companyName:'Cmp_1'}) RETURN n"
query[9] = "MATCH n RETURN n LIMIT 2"
#query[1] = "MATCH (n:Company) RETURN n LIMIT 2"
#query[2] = "MATCH (n:Drug{drunName:'Drg_1'}) RETURN n"
#query[3] = "MATCH (n:Company{companyName:'Cmp_1'}) RETURN n"
#query[4] = "MATCH n RETURN n LIMIT 25"

# Not congestion it on connections...
# So, pone N seconds delay: wait x seconds, connect, wait N-x seconds, and run the query ;-)
# wait x seconds...
N=5
rndWait=random.randint(0, N)
if debug==1: print "DBG-sleeping "+str(rndWait)
time.sleep(rndWait)

# ... connect ...
if debug==1: print "DBG-connecting to #"+str(connectTo)+"# ..."
authenticate(str(connectTo)+":7474", "neo4j", "neo4j123")
if debug==1: print "DBG-connected"

# ... wait N-x seconds ...
if debug==1: print "DBG-sleeping "+str((N-rndWait)+1)
time.sleep((N-rndWait)+1)

# and run the queries
for myIndex in range(0,int(numParallel)):
   startTime = time.time()

   try:
      graph = Graph()
      rndQuery=random.randint(0, len(query)-1)
      rndQueryVal=random.randint(0, 1000)
      queryToRun = query[rndQuery].replace('#',str(rndQueryVal))

      if debug==1: print "DBG-executing... " + str(queryToRun)
      results = graph.cypher.execute(queryToRun)
      if debug==1: print "DBG-executed"
   except Exception as detail:
      print 'NT'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999999')+','+str(detail)
   else:
      print 'NT'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(time.time() - startTime)

   graph = ""
if debug==1: print "DBG-END"
