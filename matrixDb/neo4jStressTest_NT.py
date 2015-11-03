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
try:
   showResult   =sys.argv[5]
except IndexError:
   showResult ="N"

############################################################
def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    print 'NT'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999888')+',KILLED'
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)
############################################################

if debug==1: print "DBG-START"

outConnectTo = connectTo

if connectTo == 'localhost':
   outConnectTo = connectTo+'-'+str(instanceType)
   if debug==1: print "DBG-outConnectTo="+str(outConnectTo)

randEntity = random.randint(1, 200000000)
query={}
query[0] = "MATCH (z:entityC{id:#})-[x:ENTC2ENTB]->()-[r:ENTB2ENTA]->() RETURN r,x LIMIT 250"
query[1] = "MATCH (z)-[x:ENTC2ENTB]->(y:entityB{id:#})-[r:ENTB2ENTD]->(w) RETURN z,x,y,w LIMIT 250"
query[2] = "MATCH (z:entityC{id:#})-[x:ENTC2ENTB]->(y)-[r:ENTB2ENTD]->(w) where y.id > 99 RETURN z,x,y,w LIMIT 250"
query[3] = "MATCH (ee:entityE{id:#})-[red:ENTE2ENTD]->(ed)-[rdb:ENTD2ENTB]->(eb)-[rbd:ENTB2ENTD]->(ed2)-[rdc:ENTD2ENTC]->(ec) RETURN ee, red, ed, rdb, eb, ed2, ec LIMIT 250"
query[4] = "MATCH (eb1:entityB{id:#})-[rbd1:ENTB2ENTD]->(ed1)-[rdb1:ENTD2ENTB]->(eb2)-[rbd2:ENTB2ENTD]->(ed2)-[rdc:ENTD2ENTC]->(ec2) RETURN eb1, rbd1, ed1, rdb1, eb2, ed2, ec2 LIMIT 250"
query[5] = "MATCH (ee:entityE{id:#})-[red:ENTE2ENTD]->(ed)-[rdb:ENTD2ENTB]->(eb)-[rbd:ENTB2ENTD]->(ed2)-[rdc:ENTD2ENTC{relationType:'Relation'}]->(ec) RETURN ee, red, ed, rdb, eb, ed2, ec LIMIT 250"
query[6] = "MATCH (eb:entityB{id:#})-[rbd:ENTB2ENTD]->(ed)-[rdb:ENTD2ENTB]->(ed2) RETURN eb, rbd, ed,rdb,ed2 LIMIT 250"
query[7] = "MATCH (ed:entityD{id:#})-[rdc:ENTD2ENTC]->(ec)-[rcb:ENTC2ENTB]->(eb) RETURN ed, rdc, ec,rcb,eb LIMIT 250"
query[8] = "MATCH (ed:entityD{id:#})-[rdc:ENTD2ENTC]->(ec)-[rcb:ENTC2ENTB]->(eb)-[rba:ENTB2ENTA]->(ea) RETURN ed, rdc, ec,rcb,eb,rba,ea LIMIT 250"
query[9] = "MATCH (ed:entityD{id:#})-[rdc:ENTD2ENTC]->(ec)-[rcb:ENTC2ENTB]->(eb)-[rbd:ENTB2ENTD]->(ed2)-[rdb:ENTD2ENTB]->(eb2) RETURN ed, rdc, ec,rcb,eb,rbd,ed2,rdb,eb2 LIMIT 250"

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
      rndQueryVal=random.randint(0, 200000000)
      queryToRun = query[rndQuery].replace('#',str(rndQueryVal))
      rndQueryVal=random.randint(0, 200000000)
      queryToRun = queryToRun.replace('%',str(rndQueryVal))

      if debug==1: print "DBG-executing... " + str(queryToRun)
      results = graph.cypher.execute(queryToRun)
      if debug==1: print "DBG-executed"
   except Exception as detail:
      print 'NT'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999999999')+','+str(detail)
   else:
      if showResult == "N": print 'NT'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(time.time() - startTime)
      else: print 'NT'+str(parallelGrp)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(time.time() - startTime)+',,,"'+str(results).replace('"','""')+'"'

   sys.stdout.flush()


   graph = ""
if debug==1: print "DBG-END"
sys.stdout.flush()
