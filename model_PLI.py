''' MODELLO PLI '''

import pyomo.environ as pyopt
import pandas as pd
import time
import lettura

''' 1. COSTRUZIONE DEL MODELLO ASTRATTO PER CAMMINO MINIMO CON RISORSE VINCOLATE '''

model = pyopt.AbstractModel()

''' ELEMENTI '''
model.nodes = pyopt.Set()
model.edges = pyopt.Set()

''' PARAMETRI '''
model.c = pyopt.Param(model.edges) #costi
model.w = pyopt.Param(model.edges) #risorse
model.s = pyopt.Param() #sorgente
model.t = pyopt.Param() #destinazione
model.W = pyopt.Param() # limite risorsa
model.C = pyopt.Param() #limite costo

''' VARIABILI '''
model.x = pyopt.Var(model.edges,within=pyopt.Binary)

''' FUNZIONE OBIETTIVO '''
def obj_function(model):
    return pyopt.summation(model.c,model.x)
model.z = pyopt.Objective(rule=obj_function, sense=pyopt.minimize)

''' VINCOLI '''
def cons_flow(model,node): # Flusso
    flow=sum(model.x[(i,j)] for (i,j) in model.edges if i==node)-\
        sum(model.x[(j,i)] for (j,i) in model.edges if i==node)
        
    if node==model.s:
        return flow == 1
    
    elif node==model.t:
        return flow == -1
    
    else:
        return flow == 0
model.cons_flow = pyopt.Constraint(model.nodes,rule=cons_flow)

def cons_resource(model): # Risorsa
    return sum(model.w[(i,j)]*model.x[(i,j)] for (i,j) in model.edges) <= model.W
model.cons_resource = pyopt.Constraint(rule=cons_resource)

def cons_cost(model): # Costi
    return sum(model.c[(i,j)]*model.x[(i,j)] for (i,j) in model.edges) <= model.C
model.cons_cost = pyopt.Constraint(rule=cons_cost)

solver = pyopt.SolverFactory('glpk')

''' 2. SOLUZIONE '''

mean=0 #tempo medio di soluzione

I=pd.read_csv('istanze.csv')
I=I.to_numpy() #trasformo in una matrice

G=open('MIP_solution.csv','w')
G.write('id,feasibility,time\n')

for ist in I:
    start=time.time()
    ID,graphFile,s,t,C,W=ist
    n,m,nodes,edges,adj,costs,res=lettura.readGraph(graphFile)
    
    ist={None : {}} # dizionario contenente l'istanza
    ist[None]['nodes']={None : nodes}
    ist[None]['edges']={None : edges}
    ist[None]['c']=costs
    ist[None]['w']=res
    ist[None]['s']={None : int(s)}
    ist[None]['t']={None : int(t)}
    ist[None]['C']={None : int(C)}
    ist[None]['W']={None : int(W)}
    
    instance = model.create_instance(ist)
    results = solver.solve(instance)
    
    if results.Solver._list[0]['Termination condition'] == 'infeasible':
        G.write('%d,' % ID + 'I,%g\n' % (time.time()-start))
    else:
        G.write('%d,' % ID + 'F,%g\n' % (time.time()-start))
    mean+=time.time()-start

G.close()

print(mean/len(I)) #stampa tempo medio














