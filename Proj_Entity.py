import csv
from py2neo import Graph
import os
import shutil
import pandas as pd
graph = Graph(password="BPIC14_cor")



def Visualizer(ID):
    or_file=pd.read_csv(ID+".csv")
    en_ID=or_file.en_ID.tolist()
    ent=or_file.ent.tolist()
    max_date=or_file.m_date.tolist()
    if len(en_ID) == 1 :
        print("This file has only 1 ent", ID)
        or_file.insert(7,'en_DF','EOF')
        or_file.insert(8,'en_name','EOF')
        or_file.insert(9,'en_DF_date','EOF')
        or_file.to_csv(ID+".csv", index=False)
        
    else:
        print("This file has more than 1 ent", ID)
        en_name_list=[]
        en_DF_list=[]
        date_list=[]
        for row in range(1, len(or_file)):
            en_DF_list.append(en_ID[row])
            en_name_list.append(ent[row])
            date_list.append(max_date[row])
        
        or_file = or_file[:-1]    
        or_file.insert(7,'en_DF',en_DF_list)
        or_file.insert(8,'en_name',en_name_list)
        or_file.insert(9,'en_DF_date',date_list)
        or_file.to_csv(ID+".csv", index=False)

    
   
    #print ("Counter:", count)

def fun_query(CI_ID):
    query="""  
          
                    CALL apoc.export.csv.query("MATCH  (n:Entity{EntityType:'Configuration_Item', ID:'%s'}) --(ev:Event)--(c:Common) 
                    optional match (c)--(ev_c:Event)--(en:Entity)
                    where en.EntityType='Change' or en.EntityType='Interaction' or en.EntityType='Incident'
                    with  en.EntityType as ent,ev_c.Activity as act, en.IDraw as en_ID, ev.End as date, n.Name as CI_name, n.Service_Component as SC, n.Type as CI_type, n.ID as CI_ID
                    order by date
                    with en_ID, date, act, ent, CI_name, SC, CI_type, CI_ID
                    where not ent='null'
                    return ent,en_ID, CI_name, CI_ID, SC, CI_type, max(date) as m_date order by m_date", "results_impact.csv",{stream:true})
                """
    query = query % (CI_ID)
    graph.run(query)
    
    #os.rename("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\results_impact.csv",
            #  "C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\"+CI_ID+".csv")
    if os.stat("D:\\neo4jDatabases\\database-68383d29-b7c9-44dc-a4a8-4bb020d45c5b\installation-3.5.14\\import\\results_impact.csv").st_size>59:
        
        print("file is not empty:", CI_ID)
    
        shutil.move("D:\\neo4jDatabases\\database-68383d29-b7c9-44dc-a4a8-4bb020d45c5b\installation-3.5.14\\import\\results_impact.csv",
                "D:\\VIS\\"+CI_ID+".csv")

        Visualizer(CI_ID)
        
    else:
        print("file is empty:", CI_ID)
        os.remove("D:\\neo4jDatabases\\database-68383d29-b7c9-44dc-a4a8-4bb020d45c5b\installation-3.5.14\\import\\results_impact.csv")
    

    #print ("CI:", CI_ID)

def get_CI():
    CI_query="""CALL apoc.export.csv.query("MATCH (n:Configuration_Item) RETURN distinct n.ID as CI_ID", "CI.csv",{stream:true})"""
    graph.run(CI_query)
    shutil.move("D:\\neo4jDatabases\\database-68383d29-b7c9-44dc-a4a8-4bb020d45c5b\installation-3.5.14\\import\\CI.csv",
                "D:\\VIS\\CI_list.csv")
    with open ('CI_list.csv','r') as first_file:
        csv_f = csv.DictReader(first_file)
        for row in csv_f:
            #if len(row["n.ID"])>5:
                fun_query(row["CI_ID"])

get_CI()

