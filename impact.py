import csv
from py2neo import Graph
import os
import shutil
prev_inter=0
post_inter=0
post_change=0
prev_change=0
new_index=0
graph = Graph(password="BPI14") #connect to local Neo4j DB with password

with open('impact_all_CI.csv', 'a+') as blah:
                writer = csv.writer(blah, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['ent','en_ID','CI_name', 'CI_ID', 'SC', 'CI_type','prev_int','prev_ch','post_int','post_ch'])
def impact(ID):
        
        with open('impact_all_CI.csv', 'a+') as blah:
                
                writer = csv.writer(blah, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)



                with open(ID+'.csv', 'r') as csvfile:
                        prev_inter=0
                        post_inter=0
                        post_change=0
                        prev_change=0
                        new_index=0
                        reader = csv.reader(csvfile)
                        data= [tuple(row) for row in reader]
                        #print (len(data))
                        #print (len(reader))
                        for row in range(len(data)):
                                #print(row)
                                if data[row][0]=="Interaction":
                                        prev_inter=prev_inter+1
                                elif data[row][0]=="Change":
                                        prev_change=prev_change+1
                                        new_index=row+1
                                        #print("new_index:",new_index)
                                        for index in range(new_index, len(data)):
                                                
                                                if data[index][0]=="Interaction":
                                                        post_inter=post_inter+1
                                                elif data[index][0]=="Change":
                                                        post_change=post_change+1
                                        else:
                                               
                                                        writer.writerow(['Change',data[row][1],data[row][2],data[row][3],data[row][4],data[row][5],prev_inter,prev_change-1,post_inter,post_change])
                                                        post_inter=0
                                                        post_change=0
                #os.remove(ID+'.csv')
                #print("csv file removed: ", ID)
                                
                        
def empty_file_inter_check(ID):
    
    
    if os.stat(ID+'.csv').st_size>59:
        
        with open(ID+'.csv', 'r') as csvfile:
            
            
            header=next(csvfile)
            first=next(csvfile)
            if first[1]=="I":
                impact(ID)
                                                
                        
def fun_query(CI_ID):
    query="""  
          
                    CALL apoc.export.csv.query("MATCH  (n:Entity{EntityType:'Configuration_Item', ID:'%s'}) --(ev:Event)--(c:Common) 
                    optional match (c)--(ev_c:Event)--(en:Entity)
                    where en.EntityType='Change' or en.EntityType='Interaction' 
                    with  en.EntityType as ent,ev_c.Activity as act, en.IDraw as en_ID, ev.End as date, n.Name as CI_name, n.Service_Component as SC, n.Type as CI_type, n.ID as CI_ID
                    order by date
                    with en_ID, date, act, ent, CI_name, SC, CI_type, CI_ID
                    where not ent='null'
                    return ent,en_ID, CI_name, CI_ID, SC, CI_type, max(date)order by max(date)", "results_impact.csv",{stream:true})
                """
    query = query % (CI_ID)
    graph.run(query)
    shutil.move("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\results_impact.csv",
                "D:\\TUE\\master\\Graph\\"+CI_ID+".csv")
    
    empty_file_inter_check(CI_ID)
    

def get_CI():
    CI_query="""CALL apoc.export.csv.query("MATCH (n:Configuration_Item) RETURN distinct n.ID", "CI.csv",{stream:true})"""
    graph.run(CI_query)
    shutil.move("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\CI.csv",
                "D:\\TUE\\master\\Graph\\CI_ID.csv")
    with open ('CI_ID.csv','r') as first_file:
        csv_f = csv.DictReader(first_file)
        for row in csv_f:
            #if len(row["n.ID"])>5:
                fun_query(row["n.ID"])

get_CI()                        
                       
