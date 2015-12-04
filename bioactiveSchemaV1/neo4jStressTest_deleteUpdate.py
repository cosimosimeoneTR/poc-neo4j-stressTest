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
    print ',,'+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndNode)+str(',99999998888')+',KILLED'
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
node[4] = "biomarkeruse"   # IT'S A TRAP!!! :D
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
#node[15] = "toxicity"

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

for myIndex in range(1,loopNum):

   rndNodeVal=-1
   rndNode=-1
   rndNodeVal=-1


   while rndNodeVal < 0:
      try:
         graph = Graph()

         # Get something to work on...
         rndNode=node[random.randint(0, len(node)-1)]
         rndNodeVal=random.randint(0, collectionNodeNumber)

         queryToRun = "match (a:"  +str(rndNode)+  "{id:"   +str(rndNodeVal)+  "})-[r]->(b) return a.id,type(r),id(r) limit 1"

         if debug==1: print "Running investigation query "+str(queryToRun)
         results = graph.cypher.execute(queryToRun)
         if debug==1: print "Running investigation query DONE"

         rndNodeVal=results.one[0]
         relToBeDeleted=results.one[1]
         relIdToBeDeleted=results.one[2]

      except Exception as detail:
         rndNodeVal=-1


   #... and work on it
   if deleteOrUpdate == 'D':
      queryToRun = "MATCH (x:"  +str(rndNode)+  " {id:#}) detach delete x"

   elif deleteOrUpdate == 'U':
      queryToRun = "MATCH (x:"  +str(rndNode)+  " {id:#}) set x.attr"+  str(random.randint(0, 4))   +"='"   +str(datetime.utcnow().strftime('%Y%m%d-%H%M'))+   "', x.updated='"   +str(datetime.utcnow().strftime('%Y%m%d-%H%M'))+   "'"

   elif deleteOrUpdate == 'DR':
      queryToRun = "MATCH (x:"  +str(rndNode)+  " {id:"   +str(rndNodeVal)+   "})-[r:"  +str(relToBeDeleted)+  "]->() where id(r)="  +str(relIdToBeDeleted)+   " delete r"


   # Make it happen!
   try:
      graph = Graph()

      queryToRun = queryToRun.replace('#',str(rndNodeVal))

      startTime = time.time()

      if debug==1: print "DBG-executing... " + str(queryToRun)
      results = graph.cypher.execute(queryToRun)
      if debug==1: print "DBG-executed"

      endTime = time.time()

   except Exception as detail:
      print str(testName)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndNode)+str(',9999999999')+','+str(detail)+','+str(deleteOrUpdate)+str(rndNodeVal)
   else:
      print str(testName)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndNode)+','+str(endTime - startTime)+',,'+str(deleteOrUpdate)+str(rndNodeVal)

   sys.stdout.flush()


   graph = ""
if debug==1: print "DBG-END"
sys.stdout.flush()
