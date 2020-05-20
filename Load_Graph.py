import csv
from py2neo import Graph
import os
import shutil
import pandas as pd
graph = Graph(password="BPIC-VIS")

CI_file=pd.read_csv("CI_list.csv")
CI_list=CI_file.CI_ID.tolist()
count=0
for id in range(len(CI_list)):
        count=count+1
        CI_ID=str(CI_list[id])
        try:
            

            if os.stat(CI_ID+'.csv').st_size>60:
                
                shutil.copy("D:\\VIS\\"+CI_ID+".csv",
                            "D:\\neo4jDatabases\\database-dfe763ee-3433-417f-9dad-04c2bbaba7bd\installation-3.5.14\\import\\file.csv")
                print(CI_ID)
                
                query="""
                                LOAD CSV WITH HEADERS FROM "file:///file.csv" AS csvLine
                                MERGE(CI:CI {id:csvLine.CI_ID, Name: csvLine.CI_name})
                                
                            """

                query_2="""
                                LOAD CSV WITH HEADERS FROM  "file:///file.csv"  AS csvLine
                                MERGE(Entity:Entity{id:csvLine.en_ID, Name:csvLine.ent,CI_ID:csvLine.CI_ID, Completed:csvLine.m_date})
                                
                            """
                    
                query_3="""
                                LOAD CSV WITH HEADERS FROM  "file:///file.csv"  AS csvLine
                                MERGE(Entity_DF:Entity{id:csvLine.en_DF, Name:csvLine.en_name, CI_ID:csvLine.CI_ID, Completed:csvLine.en_DF_date})

                            """
                    
                query_4="""
                                LOAD CSV WITH HEADERS FROM "file:///file.csv" AS csvLine
                                MATCH (CI:CI {id: csvLine.CI_ID, Name: csvLine.CI_name})
                                MATCH (Entity:Entity{id:csvLine.en_ID, Name:csvLine.ent, CI_ID:csvLine.CI_ID, Completed:csvLine.m_date})
                                MATCH (Entity_DF:Entity{id:csvLine.en_DF, Name:csvLine.en_name, CI_ID:csvLine.CI_ID, Completed:csvLine.en_DF_date})
                                with Entity, Entity_DF, CI
                                CREATE (CI)-[:has]->(Entity)
                                with Entity, Entity_DF
                                where not Entity_DF.id='EOF'
                                CREATE (Entity)-[:en_DF]- >(Entity_DF)
                            """
                graph.run(query)
                print("query 1 done")
                graph.run(query_2)
                print("query 2 is done")
                graph.run(query_3)
                print("query 3 is done")
                graph.run(query_4)
                print("query 4 is done")
                print("count", count)
            else:
                print ("this file is empty:", CI_ID)
                print("count", count)
        except:
            print ("couldnt find the file", CI_ID)
                
        #query = query % (CI_ID)
            
            
    #os.remove("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-77d16265-3be8-4194-aea6-2afd8b0f1f0f\\installation-3.5.14\\import\\file.csv")
    #print("csv file removed: ", CI_ID)
