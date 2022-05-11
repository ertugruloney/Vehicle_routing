import pandas as pd
import numpy as np
import gurobipy as gp
from gurobipy import GRB
model = gp.Model("hvehicle")

DATASET = "INSTANCE_11"
f = open("Instance_11.txt", mode='r')
data=f.read()
DAYS = 20
TRUCK_CAPACITY = 120
TRUCK_MAX_DISTANCE = 1000
VAN_CAPACITY = 30
VAN_MAX_DISTANCE = 1000

TRUCK_DISTANCE_COST = 20
TRUCK_DAY_COST = 200
TRUCK_COST = 0
VAN_DISTANCE_COST = 10
VAN_DAY_COST = 100
VAN_COST = 0

DELIVER_EARLY_PENALTY = 5

#read parth of PRODUCTS
indes1=data.find("PRODUCTS")+len("PRODUCTS")
indes2=data.find("HUBS")

prod=data[indes1+5:indes2-2].split(" ")

products=np.zeros( int( len(prod)/2)) 


for i in range(1,int( len(prod)/2),2):
 products[i-1]=int(prod[i])

#read parth of Hubs
indes1=data.find("HUBS")+len("HUBS")
indes2=data.find("LOCATIONS")

hubsc=data[indes1+5:indes2-2].split(" ")
hubscost=[]
for i in range(1,len(hubsc),2):
    hubscost.append(int(hubsc[i]))

hubsre=[]
for i in range(2,len(hubsc),2):
    hubsre.append(hubsc[i].split(","))
for i in range(len(hubsre)):
   
    hubsre[i][len(hubsre[1])-1]=hubsre[i][len(hubsre[1])-1].split()[0]

#read parth of LOCATIONS   
indes1=data.find("LOCATIONS")+len("LOCATIONS")
indes2=data.find("REQUESTS")
locations=[]
locationsd=data[indes1+5:indes2-2].split()
for i in range(2,len(locationsd),3):
    locations.append([int(locationsd[i-1]),int(locationsd[i])])

d=np.zeros([len(locations),len(locations)])
for i in range(len(locations)):
    for j in range(len(locations)):
        d[i][j]=((locations[i][0]-locations[j][0])**2+(locations[i][1]-locations[j][1])**2)**(1/2)
#read parth of REQUESTS        
indes1=data.find("REQUESTS")+len("REQUESTS")
indes2=data.find("REQUESTS")

requetsd=data[indes1+5:].split()
requets=[]
for i in range(3+len(products)-1,len(requetsd),3+len(products)):
    requets.append([int(requetsd[i-2]),int(requetsd[i-1]),int(requetsd[i])])
    
import gurobipy as gp
from gurobipy import GRB
model = gp.Model("Vehicle")  
Z = model.addVars(len(hubscost),DAYS,vtype=GRB.BINARY, name="Z")#1 if h hub  uses d days, other 0
X = model.addVars(len(hubscost),DAYS,20,vtype=GRB.BINARY, name="Z")#1 if h hub  uses d days with Truck, other 0
WareHubs = model.addVars(len(hubscost),DAYS,len(products),vtype=GRB.CONTINUOUS, name="Z")
WareLocation = model.addVars(DAYS,len(products),len(locations),vtype=GRB.CONTINUOUS, name="Z")
TR= model.addVars(len(hubscost),DAYS,20,len(locations),vtype=GRB.BINARY, name="Z")

