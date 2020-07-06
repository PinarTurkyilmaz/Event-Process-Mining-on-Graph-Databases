from graphviz import Digraph 
from neo4j import GraphDatabase
import random
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "V2"))

c2_cyan = "#318599"
c2_orange = "#ea700d"
c2_light_orange = "#f59d56"
c2_light_yellow = "#ffd965"
purple = "#9400D3"
green = "#008000"
c3_light_blue = "#5b9bd5"
c3_red = "#ff0000"
c3_green = "#70ad47"
c3_yellow = "#ffc000"

gray="#D3D3D3"
c4_red = '#d7191c'
c4_orange = '#fdae61'
c4_yellow = '#ffffbf'
c4_light_blue = '#abd9e9'
c4_dark_blue = '#2c7bb6'

c_white = "#ffffff"
c_black = "#000000"

c5_red = '#d73027'
c5_orange = '#fc8d59'
c5_yellow = '#fee090'
c5_light_blue = '#e0f3f8'
c5_medium_blue = '#91bfdb'
c5_dark_blue = '#4575b4'
salmon="#fdab9f"

def getNodeLabel_Event(name):
    return name


def getNodeLabel_CI(name):
    return name

cases = ['SD0031994',
         'SD0027164',
         'SD0035514',
         'SD0036110',
         'SD0036180',
         ]

def get_good_CI(tx, dot, fontcolor, edge_width, show_lifecycle):
     q = '''
        match (en:Entity{Name:"Change"}), (en2:Entity{Name:"Change"}) 
        where toInteger(en.post_inc)<toInteger(en.prev_inc)  and toInteger(en2.post_inc)>toInteger(en2.prev_inc) and en.id=en2.id
        with distinct en
        match (CI:CI{id:en.CI_ID})- [h:has]->(g_en:Entity) where g_en.Name='Change' with g_en,CI order by g_en.Completed
        with collect(distinct g_en) as nodeList, CI
        unwind range(0, size(nodeList)-2) as i
        with nodeList[i] as first, nodeList[i+1] as second, last(nodeList) as third, CI
        return distinct first, second, third, CI
        '''
     
     dot.attr("node",shape="circle",fixedsize="true", width="0.8", height="0.8", fontname="Helvetica", fontsize="10", margin="0")
     
     for record in tx.run(q):
         
        #print(record["first"]["Name"])
        #print(record["second"]["Name"])
        e1_name=getNodeLabel_Event(record["first"]["Name"])
        #e1_Comp=record["first"]["Completed"]
        # e1_comp=getNodeLabel_Event(record["g_en"]["Completed"])
        #CI_name=etNodeLabel_CI(record["g_CI"]["id"])
        #dot.node(str(record["g_CI"].id), CI_name, color=color, style="filled", fillcolor=c_white, fontcolor=c_black)
        if e1_name == "Interaction":
             color=green
        elif e1_name=='Change':
             color=gray
        else:
             color=purple
        
        edge_label = ""
        xlabel = ""
        pen_width = str(edge_width)
        edge_color =c_black
        dot.node(str(record["first"].id), e1_name, color=color, style="filled", fillcolor=c_white, fontcolor=c_black)
        node_id=str(record["first"].id)+str(1)
        #dot.edge(str(record["g_CI"].id),str(record["g_en"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",fontsize="8",fontcolor=edge_color, style="dashed")
        if record["first"]["prev_inc"] != "0" and record["first"]["prev_inc"] != None:
           
            inc_node="Incident"+":"+" "+record["first"]["prev_inc"]
            dot.node(node_id, inc_node, color=purple, style="filled", fillcolor=c_white, fontcolor=c_black)
            dot.edge(node_id,str(record["first"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                     fontsize="8",fontcolor=edge_color)
        if record["second"] != None and record["second"]["prev_inc"] != "0" and record["second"]["prev_inc"] != None:
            node_id2=str(record["second"].id)+str(1)
            inc_node2="Incident"+":"+" "+record["second"]["prev_inc"]
            edge_label = ""
            xlabel = ""
            pen_width = str(edge_width)

            edge_color = c_black
            e2_name = getNodeLabel_Event(record["second"]["Name"])
                #e2_Comp=record["second"]["Completed"]
            #e2_comp=getNodeLabel_Event(record["g_en2"]["Completed"])
            if(e2_name)== "Interaction":
                color=green
            elif e2_name=='Change':
                color=gray
            else:
                color=purple
            dot.node(node_id2, inc_node2, color=purple, style="filled", fillcolor=c_white, fontcolor=c_black)
            dot.node(str(record["second"].id), e2_name, color=color, style="filled", fillcolor=c_white, fontcolor=c_black)
            dot.edge(node_id2, str(record["second"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                         fontsize="8",fontcolor=edge_color)
            dot.edge(str(record["first"].id),node_id2,label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                     fontsize="8",fontcolor=edge_color)
        else:
            if record["second"] != None:
                edge_label = ""
                xlabel = ""
                pen_width = str(edge_width)
                edge_color = c_black
                e2_name = getNodeLabel_Event(record["second"]["Name"])
                #e2_Comp=record["second"]["Completed"]
            #e2_comp=getNodeLabel_Event(record["g_en2"]["Completed"]) 
                dot.node(str(record["second"].id), e2_name, color=c5_medium_blue, style="filled", fillcolor=c_white, fontcolor=c_black)
                dot.edge(str(record["first"].id), str(record["second"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                         fontsize="8",fontcolor=edge_color)
        if record["third"]["post_inc"] != None: 
                edge_label = ""
                xlabel = ""
                pen_width = str(edge_width)
                edge_color = c_black
                e3_name = "Incident"+":"+" "+record["third"]["post_inc"]
                node_id3=str(record["third"].id)+str(2)
                #e2_Comp=record["second"]["Completed"]
            #e2_comp=getNodeLabel_Event(record["g_en2"]["Completed"]) 
                dot.node(node_id3, e3_name, color=purple, style="filled", fillcolor=c_white, fontcolor=c_black)
                dot.edge(str(record["third"].id), node_id3,label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                         fontsize="8",fontcolor=edge_color)


                    
def get_bad_CI(tx, dot, fontcolor, edge_width, show_lifecycle):
     q = '''
        
         match (en:Entity{Name:"Change"}), (en2:Entity{Name:"Change"}) 
        where toInteger(en.post_inc)<toInteger(en.prev_inc)  and toInteger(en2.post_inc)>toInteger(en2.prev_inc) and en.id=en2.id
        with distinct en2
        match (CI:CI{id:en2.CI_ID})- [h:has]->(g_en:Entity) where g_en.Name='Change' with g_en,CI order by g_en.Completed
        with collect(distinct g_en) as nodeList, CI
        unwind range(0, size(nodeList)-2) as i
        with nodeList[i] as first, nodeList[i+1] as second, last(nodeList) as third, CI
        return distinct first, second, third, CI

        '''
     
     dot.attr("node",shape="circle",fixedsize="true", width="0.8", height="0.8", fontname="Helvetica", fontsize="10", margin="0")
     for record in tx.run(q):
             
        #print(record["first"]["Name"])
        #print(record["second"]["Name"])
        e1_name=getNodeLabel_Event(record["first"]["Name"])
        #e1_Comp=record["first"]["Completed"]
        # e1_comp=getNodeLabel_Event(record["g_en"]["Completed"])
        #CI_name=etNodeLabel_CI(record["g_CI"]["id"])
        #dot.node(str(record["g_CI"].id), CI_name, color=color, style="filled", fillcolor=c_white, fontcolor=c_black)
        if e1_name == "Interaction":
             color=green
        elif e1_name=='Change':
             color=gray   
        else:
             color=purple
        
        edge_label = ""
        xlabel = ""
        pen_width = str(edge_width)
        edge_color =c_black
        dot.node(str(record["first"].id), e1_name, color=color, style="filled", fillcolor=c_white, fontcolor=c_black)
        node_id=str(record["first"].id)+str(1)
        #dot.edge(str(record["g_CI"].id),str(record["g_en"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",fontsize="8",fontcolor=edge_color, style="dashed")
        if record["first"]["prev_inc"] != "0" and record["first"]["prev_inc"] != None:
           
            inc_node="Incident"+":"+" "+record["first"]["prev_inc"]
            dot.node(node_id, inc_node, color=purple, style="filled", fillcolor=c_white, fontcolor=c_black)
            dot.edge(node_id,str(record["first"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                     fontsize="8",fontcolor=edge_color)
        if record["second"] != None and record["second"]["prev_inc"] != "0" and record["second"]["prev_inc"] != None:
            node_id2=str(record["second"].id)+str(1)
            inc_node2="Incident"+":"+" "+record["second"]["prev_inc"]
            edge_label = ""
            xlabel = ""
            pen_width = str(edge_width)

            edge_color = c_black
            e2_name = getNodeLabel_Event(record["second"]["Name"])
                #e2_Comp=record["second"]["Completed"]
            #e2_comp=getNodeLabel_Event(record["g_en2"]["Completed"])
            if(e2_name)== "Interaction":
                color=green
            elif e2_name=='Change':
                color=c5_medium_blue
            else:
                color=purple
            dot.node(node_id2, inc_node2, color=color, style="filled", fillcolor=c_white, fontcolor=c_black)
            dot.node(str(record["second"].id), e2_name, color=color, style="filled", fillcolor=c_white, fontcolor=c_black)
            dot.edge(node_id2, str(record["second"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                         fontsize="8",fontcolor=edge_color)
            dot.edge(str(record["first"].id),node_id2,label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                     fontsize="8",fontcolor=edge_color)
        else:
            if record["second"] != None:
                edge_label = ""
                xlabel = ""
                pen_width = str(edge_width)
                edge_color = c_black
                e2_name = getNodeLabel_Event(record["second"]["Name"])
                #e2_Comp=record["second"]["Completed"]
            #e2_comp=getNodeLabel_Event(record["g_en2"]["Completed"]) 
                dot.node(str(record["second"].id), e2_name, color=c5_medium_blue, style="filled", fillcolor=c_white, fontcolor=c_black)
                dot.edge(str(record["first"].id), str(record["second"].id),label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                         fontsize="8",fontcolor=edge_color)
        if record["third"]["post_inc"] != None: 
                edge_label = ""
                xlabel = ""
                pen_width = str(edge_width)
                edge_color = c_black
                e3_name = "Incident"+":"+" "+record["third"]["post_inc"]
                node_id3=str(record["third"].id)+str(2)
                #e2_Comp=record["second"]["Completed"]
            #e2_comp=getNodeLabel_Event(record["g_en2"]["Completed"]) 
                dot.node(node_id3, e3_name, color=purple, style="filled", fillcolor=c_white, fontcolor=c_black)
                dot.edge(str(record["third"].id), node_id3,label=edge_label,color=edge_color,penwidth=pen_width,xlabel=xlabel,fontname="Helvetica",
                         fontsize="8",fontcolor=edge_color)
            
def get_good_FirstEntity(tx, dot, fontcolor, edge_width):
      q = '''
        match (en:Entity{Name:"Change"}), (en2:Entity{Name:"Change"}) 
        where toInteger(en.post_inc)<toInteger(en.prev_inc)  and toInteger(en2.post_inc)>toInteger(en2.prev_inc) and en.id=en2.id
        with distinct en
        match (g_CI:CI{id:en.CI_ID})-[h:has]->(g_en:Entity) where g_en.Name='Change' with g_en, g_CI
        order by g_en.Completed
        with g_CI, collect( distinct g_en) as entList
        return distinct g_CI, entList[0] as first

        '''
      dot.attr("node",shape="rectangle",fixedsize="true", width="0.8", height="0.8", fontname="Helvetica", fontsize="10", margin="0")
      for record in tx.run(q):
        e_id = str(record["first"].id)
        e_id2=str(record["first"].id)+str(1)
        #e_name = getNodeLabel_Event(record["e"]["Activity"])
        #entity_name = record["first"]["Name"]
        edge_color = c_black
        #entity_id = record["n"]["ID"]
        entity_uid = str(record["g_CI"].id)
        ent_name = record["g_CI"]["id"]
        #entity_label = entity_type+'\n'+entity_id
        dot.node(entity_uid,ent_name,color=green, style="filled", fillcolor=green, fontcolor=fontcolor)
        if record["first"]["prev_inc"] != "0" and record["first"]["prev_inc"] != None:
            
            dot.edge(entity_uid, e_id2, style="dashed", arrowhead="none",color=edge_color, penwidth=str(edge_width))
        else:
            dot.edge(entity_uid, e_id, style="dashed", arrowhead="none",color=edge_color, penwidth=str(edge_width) )
            
        
def get_bad_FirstEntity(tx, dot, fontcolor, edge_width):
      q = '''
        
        match (en:Entity{Name:"Change"}), (en2:Entity{Name:"Change"}) 
        where toInteger(en.post_inc)<toInteger(en.prev_inc)  and toInteger(en2.post_inc)>toInteger(en2.prev_inc) and en.id=en2.id
        with distinct en2
        match (g_CI:CI{id:en2.CI_ID})-[h:has]->(g_en:Entity) where g_en.Name='Change' with g_en, g_CI
        order by g_en.Completed
        with g_CI, collect( distinct g_en) as entList
        return distinct g_CI, entList[0] as first

        '''
      dot.attr("node",shape="rectangle",fixedsize="true", width="0.8", height="0.8", fontname="Helvetica", fontsize="10", margin="0")
      for record in tx.run(q):
        e_id = str(record["first"].id)
        e_id2=str(record["first"].id)+str(1)
        #e_name = getNodeLabel_Event(record["e"]["Activity"])
        #entity_name = record["first"]["Name"]
        edge_color = c_black
        #entity_id = record["n"]["ID"]
        entity_uid = str(record["g_CI"].id)
        ent_name=record["g_CI"]["id"]
        #entity_label = entity_type+'\n'+entity_id
        dot.node(entity_uid,ent_name,color=c3_red, style="filled", fillcolor=c3_red, fontcolor=fontcolor)
        if record["first"]["prev_inc"] != "0" and record["first"]["prev_inc"] != None:
            
            dot.edge(entity_uid, e_id2, style="dashed", arrowhead="none",color=edge_color, penwidth=str(edge_width))
        else:
            dot.edge(entity_uid, e_id, style="dashed", arrowhead="none",color=edge_color, penwidth=str(edge_width))

def color_changes(tx, dot, fontcolor, edge_width):
    q=  '''
        match (en:Entity{Name:"Change"}), (en2:Entity{Name:"Change"}) 
        where toInteger(en.post_inc)<toInteger(en.prev_inc)  and toInteger(en2.post_inc)>toInteger(en2.prev_inc) and en.id=en2.id
        return distinct en as first, en2 as second
            '''

    keyList_first=[]
    keyList_second=[]
    changeList =[]
    changeList2=[]
    lastList=[]

    for record in tx.run(q):
        keyList_first.append(str(record["first"].id))
        keyList_second.append(str(record["second"].id))
        changeList.append(record["first"]["id"])
        changeList2.append(record["second"]["id"])
        dot.node(str(record["first"].id),record["first"]["id"], color=green, penwidth=str(edge_width))
        dot.node(str(record["second"].id),record["second"]["id"], color=c3_red, penwidth=str(edge_width))
        dot.edge(str(record["first"].id), str(record["second"].id), style="dashed", arrowhead="none",color=c5_dark_blue, penwidth=str(edge_width))

    number_of_colors = len(changeList)
    print(keyList_first)
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    color_dict = dict(zip(changeList, color))
    #print(color_dict)
    first_dict = dict(zip(keyList_first, changeList))
    print(first_dict)
    sec_dict = dict(zip(keyList_second, changeList2))
    print(sec_dict)
    last_dict = {}
    for val in first_dict:
        
        for val2 in sec_dict:
            if first_dict[val] == sec_dict[val2]:
                #print(first_dict[val])
                #print(sec_dict[val2])
                
                col_val=color_dict.get(first_dict[val])
                
                print(col_val)
                
                last_dict[val]= col_val
                last_dict[val2]= col_val
    print(last_dict)           
            
    for x in last_dict:
        dot.node(x, style="filled", fillcolor=last_dict[x], fontcolor=fontcolor)


def color_CI (tx, dot, fontcolor, edge_width):
    q1= '''
        match (g_CI:CI)-- (en:Entity{Name:"Change"}), (g_CI2:CI)--(en2:Entity{Name:"Change"}) 
        where toInteger(en.post_inc)<toInteger(en.prev_inc)  and toInteger(en2.post_inc)>toInteger(en2.prev_inc) and en.id=en2.id
        return distinct g_CI, collect(distinct en.id) as good
        '''

    pos_items={}
    names_ids={}
    for record in tx.run(q1):
        
        p_name=record["g_CI"]["id"]
        ci_id=str(record["g_CI"].id)
        names_ids[ci_id]=p_name
        pos_items[ci_id]= {}
        pos_items[ci_id]["positive"]=len(record["good"])
        

    print(pos_items)
    
##    for key in my_items:
##        print(key)

    q2= '''
        match (g_CI:CI)-- (en:Entity{Name:"Change"}), (g_CI2:CI)--(en2:Entity{Name:"Change"}) 
        where toInteger(en.post_inc)<toInteger(en.prev_inc)  and toInteger(en2.post_inc)>toInteger(en2.prev_inc) and en.id=en2.id
        return distinct g_CI2, collect(distinct en2.id) as bad
        '''
    neg_items={}
    
     
    for record in tx.run(q2):
        
        ci_id=str(record["g_CI2"].id)
        n_name=record["g_CI2"]["id"]
        #print(ci_id)
        #ci_id=str(record["g_CI"].id)
        names_ids[ci_id]=n_name
        neg_items[ci_id]= {}
        neg_items[ci_id]["negative"]=len(record["bad"])

    print(neg_items)
    print(names_ids)    
    last_dict={}
    for key1 in pos_items:
        if key1 in neg_items.keys():
                print(key1)
                last_dict[key1]={}
                last_dict[key1]["positive"]= pos_items[key1]["positive"]
                last_dict[key1]["negative"]= neg_items[key1]["negative"]
               
        else:
            last_dict[key1]={}
            last_dict[key1]["positive"]=pos_items[key1]["positive"]
            last_dict[key1]["negative"]=0

    for key in neg_items:
        if not key in last_dict.keys():
            last_dict[key]={}
            last_dict[key]["negative"]=neg_items[key]["negative"]
            last_dict[key]["positive"]=0


            
    for key in last_dict:
        if last_dict[key]["positive"] > last_dict[key]["negative"]:
            dot.node(key,color=green, style="filled", fillcolor=green, fontcolor=fontcolor)
        elif last_dict[key]["positive"] < last_dict[key]["negative"]:
            dot.node(key,color=c3_red, style="filled", fillcolor=c3_red, fontcolor=fontcolor)
            
        else:
            dot.node(key,color=salmon, style="filled", fillcolor=salmon, fontcolor=fontcolor)

    
##    for key in range(len(color)):
##        my_colors={i:color[key] for i in keyList}
    #print(dictionary)
    

##def connect_changes(tx, dot, fontcolor, edge_width):
##    q=  '''
##        match (en:Entity{Name:"Change"}), (en2:Entity{Name:"Change"}) 
##        where toInteger(en.post_int)<toInteger(en.prev_int)  and toInteger(en2.post_int)>toInteger(en2.prev_int) and en.id=en2.id
##        return distinct en as first, en2 as second
##            '''
##    for record in tx.run(q):
##        e1_id = str(record["first"].id)
##        e2_id = str(record["second"].id)
####        e3_id = str(record["third"].id)
####        e4_id = str(record["fourth"].id)
##        #e_name = getNodeLabel_Event(record["e"]["Activity"])
##        entity_name1 = record["first"]["id"]
##        entity_name2 = record["second"]["id"]
##        
##        edge_color = c5_dark_blue
##        #entity_id = record["n"]["ID"]
##        #entity_uid = record["b_CI"]["id"]
##        #entity_label = entity_type+'\n'+entity_id
##        dot.node(e1_id,entity_name1,color=green, style="filled", fillcolor=green, fontcolor=fontcolor)
##        dot.node(e2_id,entity_name2,color=c3_red, style="filled", fillcolor=c3_red, fontcolor=fontcolor)
##        dot.edge(e1_id, e2_id, style="dashed", arrowhead="none",color=edge_color)
####        dot.edge(e3_id, e4_id, style="dashed", arrowhead="none",color=edge_color)

dot = Digraph(comment='Query Result', strict=True)
dot.attr("graph",rankdir="LR",margin="0",compound="true")
with driver.session() as session:
    
    session.read_transaction(get_good_CI, dot,  c_white, 8, False)
    session.read_transaction(get_good_FirstEntity, dot,  c_white, 8)
    session.read_transaction(get_bad_CI, dot,  c_white, 8, False)
    session.read_transaction(get_bad_FirstEntity, dot,  c_white, 8)
    session.read_transaction(color_changes, dot,  c_white, 8)
    session.read_transaction(color_CI, dot,  c_white, 8)
    
    

    
file = open("interactions.dot","w") 
file.write(dot.source)
file.close()
dot.render('test-output/col_inc_with_dashes_test_v2.gv', view=True)

