''' CREAZIONE DI 10.000 ISTANZE '''

import random
import grafi
import lettura

random.seed(27)

''' 1. CREAZIONE DI 20 GRAFI BASE '''
sub_n=5500 #fisso il numero di nodi

''' 10 sottografi della rete di New York '''
[n,costs,adj]=lettura.readGraphDIMACS('Dati/USA-road-d.NY.gr')
visited={} #dizionario che marca lo stato del nodo nel BFS
for i in adj:
    visited[i]=0
for i in range(10):
    s=random.randint(1,n)    
    [sub_nodes,sub_edges,sub_costs,sub_m]=grafi.createSubgraph(s,n,costs,adj,visited,sub_n)
    file='Grafi_base/grafo%02d.gr' % (i+1)
    grafi.createFileBasic(sub_n,sub_m,sub_nodes,sub_edges,sub_costs,file)

''' 10 sottografi della rete di Los Angeles '''
[n,costs,adj]=lettura.readGraphDIMACS('Dati/USA-road-d.BAY.gr')
for i in adj:
    visited[i]=0
for i in range(10):
    s=random.randint(1,n)
    [sub_nodes,sub_edges,sub_costs,sub_m]=grafi.createSubgraph(s,n,costs,adj,visited,sub_n)
    file='Grafi_base/grafo%02d.gr' % (i+11)
    grafi.createFileBasic(sub_n,sub_m,sub_nodes,sub_edges,sub_costs,file)
    


''' 2. CREAZIONE DI 200 GRAFI CON RISORSE (10 PER OGNI GRAFO BASE) '''
for i in range(20):
    for j in range(10):
        f1='Grafi_base/grafo%02d.gr' % (i+1)
        f2='Grafi/grafo%03d.gr' % (i*10+j+1)
        grafi.createFileGraph(f1,f2,100,2000)
        


''' 3. CREAZIONE DELLE ISTANZE
(PER OGNI GRAFO 10 COPPIE s-t, PER OGNI COPPIA 5 LIMITE RISORSA)'''
F=open('istanze.csv','w')
F.write('id,file,s,t,C,W\n')
cont=1 #indice istanza corrente

for i in range(200): #ciclo sui grafi
    n,_,nodes,*_=lettura.readGraph('Grafi/grafo%03d.gr' % (i+1))
    
    for j in range(10): #per ogni grafo creo 10 coppie s-t
        s=nodes[random.randint(0,n-1)]
        t=s
        while t==s:
            t=nodes[random.randint(0,n-1)]
        
        inf_W=40000
        sup_W=45000
        for k in range(5): #per ogni coppia s-t creo 5 limite risorsa
            W=random.randint(inf_W,sup_W)
            C=random.randint(70000,105000)
            F.write('%d,' % cont + 'Grafi/grafo%03d.gr,' % (i+1) + '%d,' %s + '%d,' %t + '%d,' %C + '%d\n' % W)
            cont+=1
            inf_W+=5000
            sup_W+=5000
            
    
F.close()

















