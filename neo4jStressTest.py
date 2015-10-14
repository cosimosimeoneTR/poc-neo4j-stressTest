#!/usr/bin/python

import json
from py2neo import Graph, authenticate, Node

authenticate("localhost:7474", "neo4j", "neo4j123")
graph = Graph()


results = graph.cypher.execute("MATCH (Company{companyName:'Cmp_1'})-[x:PRODUCES]->(Drug)<-[r:RELATED_TO]-(Trial)-[z:RELATED_TO]->(anotherDrug) RETURN Company,Drug,Trial,anotherDrug LIMIT 60")

#print results