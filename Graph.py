import csv
from py2neo import Graph
from neo4j import GraphDatabase
from collections import defaultdict
import shutil
import pandas as pd
import os
inter=0
change=0
uri = "bolt://localhost:7687"
#driver = GraphDatabase.driver(uri, auth=("neo4j", "BPI14"))
#authenticate("localhost:7474", "neo4j", "<pass>")
graph = Graph(password="BPI14") #connect to local Neo4j DB with password
columns = defaultdict(list)

def counter(ID):
    print("ID:", ID)
    inter=0
    change=0
    with open(ID+'.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)  
        for row in reader:
                if row["ent"]=="Interaction":
                        inter=inter+1
                        if change > 0:
                            print("Change", change)
                            change=0
                elif row["ent"]=="Change":
                        change=change+1
                        if inter > 0:
                            print("Interaction",inter)               
                            inter=0
        else:
                if inter > 0:
                    print("Interaction",inter)
                elif change > 0:
                    print ("Change", change)
                else:
                    print("There is no action")

                
def holosko(CI_name):
    #print("holosko opened:",CI_name)
    #driver = GraphDatabase.driver(uri, auth=("neo4j", "BPI14"))
    query="""  
          
                CALL apoc.export.csv.query("MATCH  (n:Entity{EntityType:'Configuration_Item', Name:'%s'}) --(ev:Event)--(c:Common) 
                optional match (c)--(ev_c:Event)--(en:Entity)
                where en.EntityType='Change' or en.EntityType='Interaction' 
                with  en.EntityType as ent,ev_c.Activity as act, en.IDraw as ID, ev.End as date
                order by date
                with ID, date, act, ent
                where not ent='null'
                return ent, max(date),ID, collect(act) order by max(date)", "/results_test.csv",{stream:true})
                """
    query = query % (CI_name)
    graph.run(query)
    shutil.move("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\results_test.csv",
                "D:\\TUE\\master\\Counter\\"+CI_name+".csv")
    #print ("query is done")
    counter(CI_name)

def get_CI():
    CI_query="""CALL apoc.export.csv.query("MATCH (n:Configuration_Item) RETURN n.Name", "CI.csv",{stream:true})"""
    graph.run(CI_query)
    shutil.move("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\CI.csv",
                "D:\\TUE\\master\\Counter\\CI.csv")
    with open ('CI.csv','r') as first_file:
        csv_f = csv.DictReader(first_file)
        for row in csv_f:
            #print (len(row["n.Name"]))
            if len(row["n.Name"])>5:
                holosko(row["n.Name"])

get_CI()
