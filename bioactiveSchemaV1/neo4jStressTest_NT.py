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
query[0] = "MATCH (organization:organization{id:#})-[x:organization2patent]->(patent)-[r:patent2bioactive]->(bioactive)-[z:bioactive2target]->(target) RETURN organization,patent,bioactive,target LIMIT 1000"
query[1] = "MATCH (biomarker1:biomarker{id:#})-[zz:biomarker2biomarker]->(biomarker2:biomarker)-[r:biomarker2biomarkeruse]->(biomarkeruse1:biomarkeruse)-[rr:biomarkeruse2biomarkeruse]->(biomarkeruse2:biomarkeruse) RETURN * LIMIT 1000"
query[2] = "MATCH (protein:protein{id:#})-[protein2gene]->(gene)-[gene2genevariant]->(genevariant)-[genevariant2bioactive]-(bioactive)-[bioactive2bioactive]->(bioactive2) return * limit 1000"
query[3] = "MATCH (a:biomarker{id:#})-[b:biomarker2biomarker]->(c:biomarker)-[d:biomarker2gene]->(e:gene)-[f:gene2gene]->(g:gene)-[h:gene2genevariant]->(i:genevariant)-[j:genevariant2bioactive]->(k:bioactive)-[l:bioactive2bioactive]->(m:bioactive)-[n:bioactive2target]->(o:target)-[p:target2target]->(q:target) RETURN * LIMIT 1000"
query[4] = "MATCH (a:experimentalpharmacology{id:#})-[b:experimentalpharmacology2experimentalmodel]->(c:experimentalmodel)-[d:experimentalmodel2conditiondesease]->(e:conditiondesease) return * limit 1000"
query[5] = "MATCH (a:organization:organization{id:#})-[b:organization2patent]->(c:patent)-[d:patent2bioactive]->(e:bioactive)-[f:bioactive2bioactive]-(g:bioactive)-[h:bioactive2drugdruginteraction]->(i:drugdruginteraction)-[j:drugdruginteraction2bioactive]->(k:bioactive)-[l:bioactive2bioactive]-(m:bioactive)-[n:bioactive2conditiondesease]-(o:conditiondesease)   RETURN * LIMIT 1000"
query[6] = "MATCH (a:bioactive{id:#})-[r:bioactive2bioactive*1..9]->() RETURN * LIMIT 10000"
query[7] = "MATCH (a:protein{id:#})-[b:protein2gene]->(c:gene)-[d:gene2genevariant]->(e:genevariant)-[f:genevariant2conditiondesease]->(g:conditiondesease) RETURN * LIMIT 10000"
query[8] = "MATCH (a:gene{id:#})-[b:gene2protein*1..9]->(c:protein)-[d:protein2gene]-(e:gene) RETURN * LIMIT 100"
query[9] = "MATCH (a:biomarker{id:#})-[b:biomarker2biomarkeruse*1..9]->(c:biomarkeruse)-[d:biomarkeruse2biomarkeruse]-(e:biomarkeruse) RETURN * LIMIT 10000"

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
