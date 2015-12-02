#!/usr/bin/python

import json, sys
from py2neo import Graph, authenticate, Node
import time,random,sys,string
from datetime import datetime
import signal

debug=0
loopNum=25

connectTo    =sys.argv[1]
numParallel  =sys.argv[2]
instanceType =sys.argv[3]
try:
   testName   =sys.argv[4]
except IndexError:
   testName = 'C'
try:
   collectionNodeNumber   =int(sys.argv[5])
except IndexError:
   collectionNodeNumber = 200000000
try:
   deleteOrUpdate   =sys.argv[6]
except IndexError:
   deleteOrUpdate = 'U'



############################################################
def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    print ',,'+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndNode)+str(',99998888')+',KILLED'
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)
############################################################

if debug==1: print "DBG-START"

outConnectTo = connectTo

if connectTo == 'localhost':
   outConnectTo = connectTo+'-'+str(instanceType)
   if debug==1: print "DBG-outConnectTo="+str(outConnectTo)

#randEntity = random.randint(1, collectionNodeNumber)
node={}
node[0] = "bioactive"
node[1] = "biomarker"
node[2] = "biomarkeruse"
node[3] = "clinicalstudies"
node[4] = "conditiondesease"
node[5] = "drugdruginteraction"
node[6] = "experimentalmodel"
node[7] = "experimentalpharmacology"
node[8] = "gene"
node[9] = "genevariant"
node[10] = "organization"
node[11] = "patent"
node[12] = "pharmacokinetics"
node[13] = "protein"
node[14] = "target"
node[15] = "toxicity"

# Not congestion it on connections...
# So, pone N seconds delay: wait x seconds, connect, wait N-x seconds, and run the node ;-)
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

for myIndex in range(1,25):

   try:
      graph = Graph()

      rndNode=node[random.randint(0, len(node)-1)]
      rndNodeVal=random.randint(0, collectionNodeNumber)

      if deleteOrUpdate == 'D':
         queryToRun = "MATCH (x:"  +str(rndNode)+  " {id:#}) detach delete x"
      elif deleteOrUpdate == 'DR':
         rndNodeVal=random.randint(0, collectionNodeNumber)
         queryToRun = "match (a:"  +str(rndNode)+  " )-[r]->(b) return labels(a),a.id,type(r),id(r) limit 1"

	 results = graph.cypher.execute(queryToRun)

	 rndNodeVal=results.one[1]
	 relToBeDeleted=results.one[2]
	 relIdToBeDeleted=results.one[3]
	 queryToRun = "MATCH (x:"  +str(rndNode)+  " {id:"   +str(rndNodeVal)+   "})-[r:"  +str(relToBeDeleted)+  "]->() where id(r)="  +str(relIdToBeDeleted)+   " delete r"
	 #print queryToRun
	 exit
	 
      else:
         queryToRun = "MATCH (x:"  +str(rndNode)+  " {id:#}) set x.updated="   +str(datetime.utcnow().strftime('%Y%m%d-%H%M'))

      queryToRun = queryToRun.replace('#',str(rndNodeVal))

      startTime = time.time()

      if debug==1: print "DBG-executing... " + str(queryToRun)
      results = graph.cypher.execute(queryToRun)
      if debug==1: print "DBG-executed"

      endTime = time.time()

   except Exception as detail:
      print str(testName)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndNode)+str(',9999')+','+str(detail)+','+str(rndNodeVal)
   else:
      print str(testName)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndNode)+','+str(endTime - startTime)+',,'+str(rndNodeVal)

   sys.stdout.flush()


   graph = ""
if debug==1: print "DBG-END"
sys.stdout.flush()
