''' FUNZIONI PER LA LETTURA DA FILE '''

''' Lettura di un file contenente un grafo dalle istanze DIMACS. La lettera iniziale
identifica il contenuto della riga:
    'c' -> commento
    'p' -> informazioni sul problema: 'sp', numero di nodi, numero di archi
    'a' -> estremi di un arco, costo
Input:
    fileName = stringa contenente il nome del file
Output:
    n = numero di nodi
    costs = dizionario dei costi
    adj = dizionario delle liste di adiacenza (chiave: nodo, valore: lista dei nodi adiacenti)
'''
def readGraphDIMACS(fileName):
    costs={} #costi
    adj={} #dizionario per le liste di adiacenza. chiave = nodo, 
            #valore = insieme dei nodi adiacenti
            #NOTA: uso la struttura INSIEME perché ci sono alcuni archi doppi nel file
    with open(fileName) as F:
        for line in F:
            if line[0]=='p':
                a, b, n, m = line.split()
                n=int(n) #numero di vertici
            elif line[0]=='a':
                a, v1, v2, c = line.split()
                v1=int(v1)
                v2=int(v2)
                costs[(v1,v2)]=int(c) #aggiungo al dizionario dei costi
                #costruisco le liste di adiacenza
                if v1 in adj: #se ho già v1 aggiungo v2 alle adiacenze
                    adj[v1].add(v2)
                else: #se non ho ancora v1, creo la lista con v2
                    adj[v1]={v2}
    return n,costs,adj

''' Lettura di un file contenente un grafo con costi e risorse. La lettera iniziale
identifica il contenuto della riga:
    'g' -> informazioni sul grafo: numero di nodi e numero di archi
    'n' -> indice di un nodo
    'e' -> estremi di un arco, valore del costo, valore della risorsa
Input:
    fileName = stringa contenente il nome del file
Output:
    n = numero di nodi
    m = numero di archi
    nodes = lista di interi (nodi)
    edges = lista di coppie di interi (archi)
    adj = dizionario le cui chiavi sono i nodi, i valori sono la lista dei nodi adiacenti
    costs = dizionario {arco: costo}
    res = dizionario {arco: risorsa}
'''
def readGraph(fileName):
    nodes=[] #lista di nodi
    edges=[] #lista degli archi
    adj={} #liste di adiacenza
    costs={} #dizionario dei costi sugli archi
    res={} #dizionario delle risorse sugli archi
    
    with open(fileName) as F:
        for line in F:
            if line[0]=='g': #numero di nodi e archi
                a,n,m=line.split()
                n=int(n)
                m=int(m)
            elif line[0]=='n': #nodi
                a,node=line.split()
                nodes.append(int(node))
            elif line[0]=='e': #archi, costi, risorse
                a,v1,v2,c,w=line.split()
                v1=int(v1)
                v2=int(v2)
                edges.append((v1,v2))
                costs[(v1,v2)]=int(c)
                res[(v1,v2)]=int(w)
                if v1 in adj: #se ho già v1 aggiungo v2 alle adiacenze
                    adj[v1].append(v2)
                else: #se non ho ancora v1, creo la lista con v2
                    adj[v1]=[v2]

    return n,m,nodes,edges,adj,costs,res
