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
try:
   showResult   =sys.argv[4]
except IndexError:
   showResult ="N"
try:
   collectionNodeNumber   =int(sys.argv[5])
except IndexError:
   collectionNodeNumber = 200000000
try:
   queryResOrCount   =sys.argv[6]
except IndexError:
   queryResOrCount = 'C'
try:
   testName   =sys.argv[7]
except IndexError:
   testName = 'C'
try:
   query2run   =int(sys.argv[8])
except IndexError:
   query2run = 99


############################################################
def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    print ',,,'+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',99998888')+',KILLED'
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)
############################################################

if debug==1: print "DBG-START"

outConnectTo = connectTo

if connectTo == 'localhost':
   outConnectTo = connectTo+'-'+str(instanceType)
   if debug==1: print "DBG-outConnectTo="+str(outConnectTo)

#randEntity = random.randint(1, collectionNodeNumber)
query={}
query[0] = "MATCH (organization:organization{id:#})-[x:organization2patent]->(patent)-[r:patent2bioactive]->(bioactive)-[z:bioactive2target]->(target) RETURN count(*) LIMIT 1000"
query[1] = "MATCH (biomarker1:biomarker{id:#})-[zz:biomarker2biomarker]->(biomarker2:biomarker)-[r:biomarker2biomarkeruse]->(biomarkeruse1:biomarkeruse)-[rr:biomarkeruse2biomarkeruse]->(biomarkeruse2:biomarkeruse) RETURN count(*) LIMIT 1000"
query[2] = "MATCH (protein:protein{id:#})-[protein2gene]->(gene)-[gene2genevariant]->(genevariant)-[genevariant2bioactive]-(bioactive)-[bioactive2bioactive]->(bioactive2) return count(*) limit 1000"
query[3] = "MATCH (a:biomarker{id:#})-[b:biomarker2biomarker]->(c:biomarker)-[d:biomarker2gene]->(e:gene)-[f:gene2gene]->(g:gene)-[h:gene2genevariant]->(i:genevariant)-[j:genevariant2bioactive]->(k:bioactive)-[l:bioactive2bioactive]->(m:bioactive)-[n:bioactive2target]->(o:target)-[p:target2target]->(q:target) RETURN count(*) LIMIT 1000"
query[4] = "MATCH (a:experimentalpharmacology{id:#})-[b:experimentalpharmacology2experimentalmodel]->(c:experimentalmodel)-[d:experimentalmodel2conditiondesease]->(e:conditiondesease) return count(*) limit 1000"
query[5] = "MATCH (a:organization:organization{id:#})-[b:organization2patent]->(c:patent)-[d:patent2bioactive]->(e:bioactive)-[f:bioactive2bioactive]-(g:bioactive)-[h:bioactive2drugdruginteraction]->(i:drugdruginteraction)-[j:drugdruginteraction2bioactive]->(k:bioactive)-[l:bioactive2bioactive]-(m:bioactive)-[n:bioactive2conditiondesease]-(o:conditiondesease)   RETURN count(*) LIMIT 1000"
query[6] = "MATCH (a:bioactive{id:#})-[r:bioactive2bioactive*1..9]->() RETURN count(*) LIMIT 10000"
query[7] = "MATCH (a:protein{id:#})-[b:protein2gene]->(c:gene)-[d:gene2genevariant]->(e:genevariant)-[f:genevariant2conditiondesease]->(g:conditiondesease) RETURN count(*) LIMIT 10000"
query[8] = "MATCH (a:gene{id:#})-[b:gene2protein*1..9]->(c:protein)-[d:protein2gene]-(e:gene) RETURN count(*) LIMIT 100"
query[9] = "MATCH (a:biomarker{id:#})-[b:biomarker2biomarkeruse*1..9]->(c:biomarkeruse)-[d:biomarkeruse2biomarkeruse]-(e:biomarkeruse) RETURN count(*) LIMIT 10000"

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

if debug==1: print "query2run="+str(query2run)
# and run the queries
for myIndex in range(0,int(numParallel)):

   try:
      graph = Graph()

      if query2run == 99:
         rndQuery=random.randint(0, len(query)-1)
      else:
         rndQuery=query2run

      rndQueryVal=random.randint(0, collectionNodeNumber)
      queryToRun = query[rndQuery].replace('#',str(rndQueryVal))
      rndQueryVal=random.randint(0, collectionNodeNumber)
      queryToRun = queryToRun.replace('%',str(rndQueryVal))

      if queryResOrCount != 'C': queryToRun = queryToRun.replace('count(*)','*')

      startTime = time.time()

      if debug==1: print "DBG-executing... " + str(queryToRun)
      results = graph.cypher.execute(queryToRun)
      if debug==1: print "DBG-executed"

      endTime = time.time()

   except Exception as detail:
      print str(testName)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+str(',9999')+','+str(detail)+','+str(rndQueryVal)
   else:
      if showResult == "N": 
         print str(testName)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(endTime - startTime)+',,'+str(rndQueryVal)
      else: 
         print str(testName)+','+str(numParallel)+','+datetime.utcnow().strftime('%Y%m%d-%H%M')+','+str(outConnectTo)+','+str(rndQuery)+','+str(endTime - startTime)+',,'+str(rndQueryVal)+',"'+str(results).replace('"','""')+'"'

   sys.stdout.flush()


   graph = ""
if debug==1: print "DBG-END"
sys.stdout.flush()
