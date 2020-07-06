import matplotlib.pyplot as plt
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "V2"))


green = "#008000"
salmon="#fdab9f"
red = "#ff0000"

def scatter_plot(tx):
    i=0
    q = '''
        match (en:Entity{Name:"Change"}) where toInteger(en.post_inc)<toInteger(en.prev_inc) 
        return toInteger(en.prev_inc) as prev_inc,toInteger(en.post_inc) as post_inc, en.id as chg
        order by prev_inc desc
        '''
    x_list=[]
    y_list=[]
    g_chg_list=[]
    g_CI_list = []
    b_chg_list=[]
    b_CI_list = []
    g_dict={}
    for record in tx.run(q):

        x_list.append(record["prev_inc"])
        y_list.append(record["post_inc"])
    plt.scatter(x_list, y_list)


    q1 = ''' match (en:Entity{Name:"Change"}) where toInteger(en.post_inc)<toInteger(en.prev_inc)
        return en.id as chg, collect(en.CI_ID) as good
    '''
 

    g_dict={}
    for record in tx.run(q1):
        g_dict[record["chg"]]=record["good"]



    q2 =''' match (en:Entity{Name:"Change"}) where toInteger(en.post_inc)>toInteger(en.prev_inc)
        return en.id as chg, collect(en.CI_ID) as bad
    '''
 

    b_dict={}
    prev=[]
    post=[]
    for record in tx.run(q2):
        b_dict[record["chg"]]=record["bad"]
    colors={}
    for key in g_dict:
        if key in b_dict.keys():
            if len(g_dict[key])==len(b_dict[key]):
                colors[key]=salmon
            elif len(g_dict[key])>len(b_dict[key]):
                colors[key]=green
            else:
                colors[key]=red

    print(colors)
    g_prev=[]
    g_post=[]
    c_list=[]
    
    for key in colors:
        
        q3 = '''
                match (en:Entity{id:"%s"}) where toInteger(en.prev_inc)>toInteger(en.post_inc) return toInteger(en.prev_inc) as prev, toInteger(en.post_inc) as post order by prev desc
            '''

        q3=q3%(key)
        for record in tx.run(q3):
            plt.scatter(record["prev"], record["post"], c=colors[key])

   
    plt.xlabel("Number of Previous Incidents")
    plt.ylabel("Number of Next Incidents")
  
    plt.axis("square")
    plt.show()  


with driver.session() as session:
    
    session.read_transaction(scatter_plot)
