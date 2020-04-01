import csv
inter=0
change=0  
with open('results.csv', 'r') as csvfile:
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
                
            
