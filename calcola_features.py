''' CALCOLO DELLE FEATURES PER LE ISTANZE '''

import features as ft
import lettura
import pandas as pd

I=pd.read_csv('istanze.csv')
I=I.to_numpy() #trasformo in una matrice

F=open('features.csv','w')
F.write('f1_1,f1_2,f1_3,f1_4,f2_1,f2_2,f3_1,f3_2,f4_1,f4_2,f4_3,f4_4,,f6,f7_1,f7_2,f7_3,f7_4,f7_5,f7_6,f7_7,f7_8,f7_9\n')

for ist in range(30):

    ''' IMPORTO L'ISTANZA '''
    graphFile,s,t,C,W=I[ist]
    n,m,nodes,edges,adj,costs,res=lettura.readGraph(graphFile)
    
    ''' CALCOLO CAMMINO MINIMO RISPETTO AI COSTI '''
    minCost_pred, minCost_keys = ft.dijkstra(adj,costs,s)
    minCost_nodes, minCost_edges = ft.minCostPath(s,t,minCost_pred)

    ''' CALCOLO CAMMINO MINIMO RISPETTO ALLE RISORSE ''' 
    minRes_pred, minRes_keys = ft.dijkstra(adj,res,s) #cammino minimo rispetto alle risorse
    minRes_nodes, minRes_edges = ft.minCostPath(s,t,minRes_pred)
    
    ''' CALCOLO FEATURES '''
    ''' 1. Valore relativo consumo risorsa / costo '''
    minCost_res = ft.consume(minCost_edges,res) #consumo risorsa nel cammino di costo minimo
    f1_1 = minCost_res/W
    f1_2 = minCost_keys[t]/C
    
    minRes_cost = ft.consume(minRes_edges,costs) #costo cammino a risorsa minima
    f1_3 = minRes_cost/C
    f1_4 = minRes_keys[t]/W
    
    F.write('%g,' % f1_1 + '%g,' % f1_2 + '%g,' % f1_3 + '%g,' % f1_4)
    
    ''' 2. Percentuale archi usati '''
    f2_1 = len(minCost_edges)/m
    f2_2 = len(minRes_edges)/m
    
    F.write('%g,' % f2_1 + '%g,' % f2_2)
    
    ''' 3. Costi ridotti '''
    f3_1 = ft.reducedCosts(minCost_edges,adj,costs,minCost_keys)
    f3_2 = ft.reducedCosts(minRes_edges,adj,res,minRes_keys)
    
    F.write('%g,' % f3_1 + '%g,' % f3_2)
    
    ''' 4. Differenza tra il costo medio di un arco del cammino ed il
    costo medio di un arco in un intorno del cammino ma non nel cammino '''
    d_max=2 #massima ampiezza dell'intorno
    f4_1 = (minCost_keys[t]/len(minCost_edges))/ft.neighbourhood(minCost_nodes,minCost_edges,adj,costs,d_max)
    f4_2 = (minRes_keys[t]/len(minRes_edges))/ft.neighbourhood(minRes_nodes,minRes_edges,adj,res,d_max)
    d_max=3
    f4_3 = (minCost_keys[t]/len(minCost_edges))/ft.neighbourhood(minCost_nodes,minCost_edges,adj,costs,d_max)
    f4_4 = (minRes_keys[t]/len(minRes_edges))/ft.neighbourhood(minRes_nodes,minRes_edges,adj,res,d_max)
    
    F.write('%g,' % f4_1 + '%g,' % f4_2 + '%g,' % f4_3 + '%g,' % f4_4)
    
    ''' 5. ??? '''
    F.write(',')
    
    ''' 6. Rapporto tra minimo numero di step e diametro del grafo '''
    #utilizzo dijkstra con costi unitari sugli archi
    # step={}
    # for i in edges:
    #     step[i]=1
    # minStep_pred, _ = ft.dijkstra(adj,step,s) #cammino minimo rispetto alle risorse
    # _, minStep_edges = ft.minCostPath(s,t,minRes_pred)
    # diam=ft.diametro(adj)
    # f6 = len(minStep_edges)/diam
    
    # F.write('%g,' % f6)
    F.write(',')
    
    ''' 7. Gradio max, min, medio dei nodi dei cammini minimi e del grafo'''
    f7_1, f7_2, f7_3 = ft.degree(minCost_nodes,adj)
    f7_4, f7_5, f7_6 = ft.degree(minRes_nodes,adj)
    f7_7, f7_8, f7_9 = ft.degree(nodes,adj)
    
    F.write('%d,' % f7_1 + '%d,' % f7_2 + '%d,' % f7_3 + '%d,' % f7_4)
    F.write('%d,' % f7_5 + '%d,' % f7_6 + '%d,' % f7_7 + '%d,' % f7_8 + '%d\n' % f7_9)
    
    
F.close()   

    
    
    
    