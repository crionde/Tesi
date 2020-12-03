''' FUNZIONI PER LA GENERAZIONE DEI GRAFI BASE '''
''' La lettera iniziale identifica il contenuto della riga:
    'g' -> informazioni sul grafo: numero di nodi e numero di archi
    'n' -> indice di un nodo
    'e' -> estremi di un arco, valore del costo
'''

import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from collections import deque

''' GRAFI DALLE ISTANZE DI SOLOMON '''
''' Crea un file contenente il grafo a partire da un csv contentente un'istanza di Solomon.
Input:
    csvFile = stringa del file csv contenente l'istanza
    graphFile = stringa del nome del file prodotto.
'''
def createFileSolomon(csvFile,graphFile):
    dati=pd.read_csv(csvFile)
    n=len(dati)
    
    F=open(graphFile,'w')

    ''' Numero di nodi '''
    F.write('g %d ' % n + '%d\n' % (n*n-n))
    
    ''' Nodi '''
    for i in range(n):
        F.write('n %d\n' % (i+1))

    ''' Archi e costo '''
    #Calcola i costi come distanza euclidea per difetto tra i nodi
    dist=distance_matrix(dati[['XCOORD.','YCOORD.']].values,\
                         dati[['XCOORD.','YCOORD.']].values)
    dist=np.floor(dist)

    for i in range(n):
        for j in range(n):
            if j!=i:
                F.write('e %d ' % (i+1) + '%d ' % (j+1) + '%d\n' % dist[i][j])

    F.close()
    return


''' SOTTOGRAFI DALLA RETE STRADALE AMERICANA '''
''' Crea un sottografo di p nodi a partire da un grafo di n nodi definito
tramite archi, costi e liste di adiacenza. Restituisce i nodi selezionati,
gli archi e i relativi costi. Viene effettuata una BFS a partire da s
Input:
    s = indice del nodo da cui parte la ricerca
    n = numero di nodi del grafo
    costs = dizionario dei costi
    adj = dizionario delle liste di adiacenza (chiave: nodo, valore: lista dei nodi adiacenti)
    visited = dizionario per marcare lo stato del nodo
              nodo: 0 [non visitato], nodo: 1 [raggiunto], nodo: 2 [visita completata]
    p = numero di nodi del sottografo che si vuole ottenere
Output:
    sub_nodes = lista dei nodi scelti
    sub_edges = lista degli archi scelti
    sub_costs = dizionario dei costi degli archi scelti
    sub_m = numero di archi scelti
'''
def createSubgraph(s, n, costs, adj, visited, p):
    sub_m=0 #numero di archi
    sub_nodes=[]
    sub_edges=[]
    sub_costs={}
    q=deque()
    q.append(s)
    visited[s]=1
    sub_nodes.append(s) #aggiungo s al sottografo
    
    cont=1
    while (cont < p) & (cont < n): #quando raggiungo p o n mi fermo        
        node=q.popleft()  #estraggo il primo nodo dalla coda
        
        for i in adj[node]: #scorro la lista di adiacenza
            if visited[i] != 0:
                sub_edges.append((node,i))  #aggiungo l'arco
                sub_costs[(node,i)]=costs[(node,i)]
                sub_m+=1
                
            elif visited[i]==0 & cont<p: #se il nodo i non è ancora stato raggiunto e non ho raggiunto il limite di nodi
                sub_edges.append((node,i))  #aggiungo l'arco
                sub_costs[(node,i)]=costs[(node,i)]
                sub_m+=1
                sub_nodes.append(i) #aggiungo il nodo
                cont+=1
                q.append(i)
                visited[i]=1
        
        visited[node]=2 #marco il nodo come visitato
        
    #svuoto eventualmente la coda aggiungendo gli archi mancanti al sottografo
    while len(q)!=0:
        node=q.popleft()
        for i in adj[node]:
            if visited[i] != 0: # NOTA: NON DEVO AGGIUNGERE NUOVI NODI
                sub_edges.append((node,i))
                sub_costs[(node,i)]=costs[(node,i)]
                sub_m+=1
    
    # rimetto a 0 visited dei nodi toccati
    for i in sub_nodes:
        visited[i]=0
    
    return sub_nodes, sub_edges, sub_costs, sub_m


''' Crea un file contenente il grafo a partire dai nodi, archi, costi ricavati
Input:
    n = numero di nodi
    m = numero di archi
    nodes = lista dei nodi
    edges = lista degli archi
    costs = dizionario dei costi
    graphFile = stringa con il nome del file da produrre '''
def createFileBasic(n,m,nodes,edges,costs,graphFile):
    F=open(graphFile,'w')

    ''' Numero di nodi e archi '''
    F.write('g %d ' % n)
    F.write('%d\n' % m)
    
    ''' Nodi '''
    for i in nodes:
        F.write('n %d\n' % i)

    ''' Archi e costo '''
    #Calcola i costi come distanza euclidea per difetto tra i nodi
    for e in edges:
        F.write('e %d ' % e[0] + '%d ' % e[1] + '%d\n' % costs[e])

    F.close()
    return



''' FUNZIONI PER LA GENERAZIONE DEI GRAFI CON RISORSE '''
''' La lettera iniziale identifica il contenuto della riga:
    'g' -> informazioni sul grafo: numero di nodi e numero di archi
    'n' -> indice di un nodo
    'e' -> estremi di un arco, valore del costo, valore della risorsa
'''

import random

''' Creazione di un grafo con risorse casuali scelte in un intervallo,
a partire da un grafo base.
Input:
    basicGraphFile = stringa con il nome del grafo base
    graphFile = stringa con il nome del file che si vuole produrre
    inf = estremo inferiore dell'intervallo
    sup = estremo superiore dell'intervallo
'''
def createFileGraph(basicGraphFile,graphFile,inf,sup):
    res={} #dizionario che tiene traccia degli archi già aggiunti perché il grafo sia simmetrico
    with open(basicGraphFile) as F1:
        F2=open(graphFile,'w')
        for line in F1:
            if line[0]=='g': #se è il numero di nodi o un nodo, copio
                F2.write(line)
            elif line[0]=='n': #se è un nodo, copio
                F2.write(line)
            elif line[0]=='e':
                e, e1, e2, c=line.split()
                if (e2,e1) in res: #se ho già aggiunto l'arco (e2,e1), assegno la stessa risorsa
                    w=res[(e2,e1)]
                else: #altrimenti è casuale
                    w=random.randint(inf,sup)
                    res[(e1,e2)]=w
                F2.write(e + ' ' + e1 + ' ' + e2 + ' ' + c + ' %d\n' % w)
        F2.close()
        return




