import csv
from py2neo import Graph
from neo4j import GraphDatabase
from collections import defaultdict
import shutil
import pandas as pd
import os
inter=0
change=0
graph = Graph(password="BPI14") #connect to local Neo4j DB with password




def counter (ID):
    inter=0
    change=0
    
    text_file = open("results_counter.txt", "a+")
    text_file.write('ID:'+ID)
    with open(ID+'.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            if row["ent"]=="Interaction":
                inter=inter+1
                if change > 0:
                    text_file.write('\nChange:%d \n'%change)
                    #text_file.write(change)
                    change=0
            elif row["ent"]=="Change":
                
                change=change+1
                if inter > 0:
                    text_file.write('\nInteraction:%d \n'%inter)
                    #text_file.write(inter)
                    inter=0
        else:
                if inter > 0:
                    text_file.write('\nInteraction:%d \n'%inter)
                    #text_file.write(inter)
                elif change > 0:
                    text_file.write ('\nChange:%d \n'%change)
                    #text_file.write(change)
                else:
                    text_file.write("\nThere is no action")
    #text_file.close()
    #print('text file closed')
    #csvfile.close()
    #print('csv file closed')
    #os.remove(ID+'.csv')
    #print('csv file removed')

    
def empty_file_inter_check(ID):
    
    
    if os.stat(ID+'.csv').st_size>38:
        
        with open(ID+'.csv', 'r') as csvfile:
            
            
            header=next(csvfile)
            first=next(csvfile)
            #print("header",header)
            #print("first line", first)
            #print(first[1])
            if first[1]=="I":
                counter(ID)
                #print("ID:", ID)
                
                #print (reader)
                

                
def fun_query(CI_name):
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
    
    empty_file_inter_check(CI_name)
    

def get_CI():
    CI_query="""CALL apoc.export.csv.query("MATCH (n:Configuration_Item) RETURN n.Name", "CI.csv",{stream:true})"""
    graph.run(CI_query)
    shutil.move("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\CI.csv",
                "D:\\TUE\\master\\Counter\\CI.csv")
    with open ('CI.csv','r') as first_file:
        csv_f = csv.DictReader(first_file)
        for row in csv_f:
            if len(row["n.Name"])>5:
                fun_query(row["n.Name"])

get_CI()
