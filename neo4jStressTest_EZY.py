#!/usr/bin/python

import json, sys
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
    print 'EZY'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999888')+',KILLED'
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
query[1] = "MATCH (n:Company) RETURN n LIMIT 2"
query[2] = "MATCH (n:Drug{drugName:'Drg_1'}) RETURN n"
query[3] = "MATCH (n:Company{companyName:'Cmp_1'}) RETURN n"
query[4] = "MATCH n RETURN n LIMIT 25"
query[5] = "MATCH n RETURN n LIMIT 2"
query[6] = "MATCH (n:Drug) RETURN n LIMIT 1"
query[7] = "MATCH (n:Disease) RETURN n LIMIT 1"

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
      print 'EZY'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999999')+','+str(detail)
   else:
      print 'EZY'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(time.time() - startTime)

   sys.stdout.flush()


   graph = ""
if debug==1: print "DBG-END"
sys.stdout.flush()
