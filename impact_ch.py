import csv
from py2neo import Graph
import os
import shutil
import pandas as pd 
graph = Graph(password="BPIC-VIS")


def Q1(CI_ID):
    ent_name=[]
    ent_ID=[]
    ch_list=[]
    list_ent=[]
    list_ent_ID=[]
    prev=pd.DataFrame(columns=['CI','Change', 'prev_int'])
    post=pd.DataFrame(columns=['CI','Change', 'post_int'])
    file=pd.read_csv(CI_ID+".csv")
    list_ent=file.ent.tolist()
    list_ent_ID=file.en_ID.tolist()
    if 'Interaction' in list_ent and 'Change' in list_ent:
        index= list_ent.index('Interaction')     
        for row in range(index, len(list_ent)):
                ent_name.append(list_ent[row])
                ent_ID.append(list_ent_ID[row])
        for i in range (len(ent_name)):
                if ent_name[i] == "Change":
                      ch_list.append(ent_ID[i])  

        first=0
        second=1
        for i in range (len(ch_list)-1):

                if first==0:
                        index_first=ent_ID.index(ch_list[first])
                        index_sec=ent_ID.index(ch_list[second])
                        cnt_int=index_sec-index_first
                        prev=prev.append({'CI':CI_ID,'Change':ch_list[first], 'prev_int':index_first},ignore_index=True)
                        post=post.append({'CI':CI_ID,'Change':ch_list[first],'post_int':cnt_int-1},ignore_index=True)
                        #df=df.append({'CI':ch_list[first], 'post_int':cnt_int-1},ignore_index=True)
                        prev=prev.append({'CI':CI_ID,'Change':ch_list[second], 'prev_int':cnt_int-1},ignore_index=True)
                        
        ##                print( 'Change:',ch_list[first],"prev_int:",index_first)
        ##                print( 'Change:',ch_list[first],"post_int:",cnt_int-1)
        ##                print( 'Change:',ch_list[second],"prev_int:",cnt_int-1)
                        first=second
                        second=second+1

                elif second<len(ch_list)-1:
                        
                        index_first=ent_ID.index(ch_list[first])
                        index_sec=ent_ID.index(ch_list[second])
                        cnt_int=index_sec-index_first
                        if cnt_int > 1:
                                post=post.append({'CI':CI_ID,'Change':ch_list[first], 'post_int':cnt_int-1},ignore_index=True)
                                prev=prev.append({'CI':CI_ID,'Change':ch_list[second], 'prev_int':cnt_int-1},ignore_index=True)
                                #print( 'Change:',ch_list[first],"post_int:",cnt_int-1)
                                #print( 'Change:',ch_list[second],"prev_int:",cnt_int-1)
                        else:
                                post=post.append({'CI':CI_ID,'Change':ch_list[first], 'post_int':0},ignore_index=True)
                                prev=prev.append({'CI':CI_ID,'Change':ch_list[second], 'prev_int':0},ignore_index=True)
                                #print( 'Change:',ch_list[first],"post_int:",0)
                                #print( 'Change:',ch_list[second],"prev_int:",0)
                        first=second
                        second=second+1
                else:
                        
                        index_first=ent_ID.index(ch_list[first])
                        index_sec=ent_ID.index(ch_list[second])
                        cnt_int=index_sec-index_first
                        post=post.append({'CI':CI_ID,'Change':ch_list[first], 'post_int':cnt_int-1},ignore_index=True)
                        prev=prev.append({'CI':CI_ID,'Change':ch_list[second], 'prev_int':cnt_int-1},ignore_index=True)
                        post=post.append({'CI':CI_ID,'Change':ch_list[second], 'post_int':len(ent_ID)-index_sec-1},ignore_index=True)
                        
        ##                print( 'Change:',ch_list[first],"post_int:",cnt_int-1)
        ##                print( 'Change:',ch_list[second],"prev_int:",cnt_int-1)
        ##                print( 'Change:',ch_list[second],"post_int:",len(ent_ID)-index_sec-1)
                        
        else:

                #print (prev)
                #print(post)
                result=prev.merge(post,on =['CI', 'Change'], how='right')
                print(result)
                result.to_csv("results.csv", mode='a', header=False)
                
    else:
        print(" There is no interaction or change")

##    except:
##        print(CI_ID,"can not found")
    

def fun_query(CI_ID):
    
    query="""  
          
                    CALL apoc.export.csv.query("match (n:CI{id:'%s'})--(en:Entity)
                    where en.Name='Interaction' or en.Name='Change'
                    return en.Name as ent, en.id as en_ID, en.Completed as d
                    order by d", "results_impact.csv",{stream:true})
                """
    query = query % (CI_ID)
    graph.run(query)
    
    #os.rename("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\results_impact.csv",
            #  "C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\"+CI_ID+".csv")
    if os.stat("D:\\neo4jDatabases\\database-dfe763ee-3433-417f-9dad-04c2bbaba7bd\\installation-3.5.14\\import\\results_impact.csv").st_size>18:
        
        print("file is not empty:", CI_ID)
    
        shutil.move("D:\\neo4jDatabases\\database-dfe763ee-3433-417f-9dad-04c2bbaba7bd\\installation-3.5.14\\import\\results_impact.csv",
                "D:\\BPIC-Q1\\Interaction_Change\\"+CI_ID+".csv")

        Q1(CI_ID)
        
    else:
        print("file is empty:", CI_ID)
        os.remove("D:\\neo4jDatabases\\database-dfe763ee-3433-417f-9dad-04c2bbaba7bd\\installation-3.5.14\\import\\results_impact.csv")
    
##
    #print ("CI:", CI_ID)

def get_CI():
##    CI_query="""CALL apoc.export.csv.query("MATCH (n:Configuration_Item) RETURN distinct n.ID", "CI.csv",{stream:true})"""
##    graph.run(CI_query)
##    shutil.move("C:\\Users\\Pinar\\.Neo4jDesktop\\neo4jDatabases\\database-612a2166-8561-460d-85a0-36cc98a990ce\\installation-3.5.14\\import\\CI.csv",
##                "D:\\TUE\\master\\BPIC14-Q1\\CI_ID.csv")
    with open ('CI_list.csv','r') as first_file:
        csv_f = csv.DictReader(first_file)
        for row in csv_f:
                fun_query(row["CI_ID"])
##
get_CI()
