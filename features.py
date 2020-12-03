''' FUNZIONI PER IL CALCOLO DELLE FEATURES '''

import priority_queue as prq
import itertools
from collections import deque


''' Implementazione dell'algoritmo di Dijkstra per il calcolo del cammino minimo.
Input:
    adj = dizionario delle liste di adiacenza (chiave: nodo, valore: lista dei nodi adiacenti)
    costs = dizionario dei costi sugli archi
    s = indice del nodo sorgente
Output:
    pred = dizionario dei predecessori nell'albero prodotto dall'algoritmo
    key = dizionario {nodo : costo minimo di un cammino da s al nodo}
 '''
def dijkstra(adj,costs,s):
    pred={}
    key={}
    
    for i in adj: #inizializzo a infinito le chiavi
        key[i]=float('inf')
    key[s]=0
    
    '''Creo la coda con priorità. Uso il modulo heapq con l'aggiunta di un dizionario
    per marcare la posizione di una task nell'heap. heapq non supporta la modifica 
    delle priorità, quindi quando cambio la priorità aggiungo una nuova task e marco
    come rimossa la precedente'''
    REMOVED = '<removed-task>'
    counter = itertools.count()
    entry_finder={}
    pq=[]
    
    prq.add_task(pq,s,key[s],entry_finder,counter,REMOVED) #aggiungo s alla coda
    pred[s]=-1
    
    while prq.empty(pq,REMOVED)==False:
        u=prq.pop_task(pq,entry_finder,REMOVED)
        for v in adj[u]:
            if (key[u]+costs[(u,v)]) < key[v]:
                pred[v]=u
                key[v]=key[u]+costs[(u,v)]
                prq.add_task(pq,v,key[v],entry_finder,counter,REMOVED)
    
    return pred, key

''' Calcolo del cammino minimo da s a t a partire dal risultato di Dijkstra.
Input:
    s = intero (nodo sorgente)
    t = intero (nodo destinazione)
    pred = dizionario dei predecessori prodotto da Dijkstra
Output:
    path_nodes = lista dei nodi toccati dal cammino di costo minimo
    path_edges = lista degli archi toccati dal cammino di costo minimo
'''
def minCostPath(s,t,pred):
    path_nodes=[] #lista dei nodi del cammino minimo
    path_edges=[] #lista degli archi del cammino minimo
    
    i=t
    while i!=s:
        path_nodes.append(i)
        path_edges.append((pred[i],i))
        i=pred[i]
    
    path_nodes.append(s)
    
    return path_nodes, path_edges

''' Calcola il consumo della risorsa di un insieme di archi.
Input:
    path_edges = lista di archi
    res = dizionario delle risorse
Output:
    res_tot = totale di risorsa consumato
'''
def consume(path_edges,res):
    res_tot=0
    for e in path_edges:
        res_tot+=res[e]
    
    return res_tot


''' Per i nodi del cammino di costo minimo, calcolo il costo ridotto dell'arco uscente
di costo ridotto minimo non scelto. Quindi restituisce la media dei valori trovati.
Input:
    path_edges = lista degli archi del cammino di costo minimo
    adj = liste di adiacenza
    costs = dizionario dei costi
    key = costo del cammino minimo fino a ogni nodo restituito da Dijkstra
Output:
    mean = media dei costi ridotti degli archi di costo ridotto minimo non scelti
'''
def reducedCosts(path_edges,adj,costs,key):
    mean=0
    zero_nodes=0 #numero di nodi con zero archi uscenti oltre a quello del cammino
    
    for e in path_edges: #ciclo sugli archi del cammino minimo
        rc_min=float('inf') #costo ridotto minimo tra gli archi uscenti da e[0]
        k=key[e[0]] #costo del cammino di costo minimo fino a e[0]
        for i in adj[e[0]]: #scorro le adiacenze di e[0]
            if i != e[1]: #se l'arco (e[0],i) NON è quello del cammino minimo
                rc=costs[(e[0],i)]-(key[i]-k)
                if(rc<rc_min):
                    rc_min=rc
        if rc_min != float('inf'):        
            mean+=rc_min
        else:
            zero_nodes+=1
        
    mean/=len(path_edges)-zero_nodes
    
    return mean

''' Calcolo il grado massimo, minimo e medio di una lista di nodi.
Inpunt:
    nodes = lista di nodi
    adj = liste di adiacenza
Output:
    max_degree = grado massimo
    min_degree = grado minimo
    mean_degree = grado medio
'''
def degree(nodes,adj):
    mean_degree=0
    min_degree=float('inf')
    max_degree=-1
    
    for i in nodes:
        l=len(adj[i])
        mean_degree += l
        if l<min_degree:
            min_degree = l
        if l>max_degree:
            max_degree = l
    
    mean_degree /= len(nodes)
    
    return max_degree, min_degree, mean_degree

''' Calcolo il costo medio degli archi non del cammino, che siano in un intorno
(intorno := sottografo indotto dai nodi a distanza <= d dal cammino
distanza := minimo numero di archi dal nodo a un nodo del cammino)
Input:
    path_nodes = lista di nodi nel cammino
    path_edges = lista di archi del cammino
    adj = dizionario delle liste di adiacenza
    costs = dizionario dei costi sugli archi
    d_max = distanza massimo dei nodi scelti dai nodi del cammino
Output:
    mean_cost = costo medio degli archi nell'intorno non nel cammino
'''
def neighbourhood(path_nodes,path_edges,adj,costs,d_max):
    dist={}
    for i in adj:
        dist[i]=-1
    
    # inizializzo la coda aggiungendoci i nodi del cammino
    q = deque()
    for i in path_nodes:
        q.append(i)
        dist[i]=0
    
    selected=[] #lista degli archi selezionati
    mean_cost = 0 #costo medio degli archi scelti

    while len(q)!=0:    
        k=q.popleft() #estraggo il primo elemento
        for j in adj[k]: #scorro le adiacenze
            if (dist[j]==-1) & (dist[k]<d_max): #se non è visitato e non è troppo distante
                #metto il nodo in coda, incrementando il numero di nodi messi in coda
                q.append(j)
                dist[j]=dist[k]+1
                #aggiungo l'arco ai selezionati
                selected.append((k,j))
                mean_cost += costs[(k,j)]
            elif (dist[j]!=-1) & ((k,j) not in path_edges): #se il nodo è visitato e l'arco non è nel cammino
                #aggiungo l'arco ai selezionati
                selected.append((k,j))
                mean_cost += costs[(k,j)]
    
    return mean_cost

''' Funzione per il calcolo del diametro.
Input:
    adj = liste di adiacenza
Output:
    d_max = diametro del grafo
'''
def diametro(adj):
    dist={}
    q=deque()
    d_max=-1
    for node in adj:
        for i in adj:
            dist[i]=-1
        dist[node]=0
        q.append(node)
        while len(q)!=0:
            s=q.popleft()
            ds=dist[s]
            if ds>d_max:
                d_max=ds
            for k in adj[s]:
                if dist[k]==-1:
                    q.append(k)
                    dist[k]=ds+1
       
    return d_max














