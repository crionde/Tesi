''' FUNZIONI PER IMPLEMENTARE UNA CODA CON PRIORITA' USANDO IL MODULO heapq
Per consentire la modifica delle priorità all'interno della coda, si utilizza
un dizionario per identificare nella coda la task con la priorità corretta.
La vecchia task viene marcata come REMOVED e ignorata quando estratta dalla coda. 
 [vedi python documentation]'''

import heapq

''' Add a new task or update the priority of an existing task '''
def add_task(pq,task,priority,entry_finder,counter,REMOVED):

    if task in entry_finder:
        remove_task(task,entry_finder,REMOVED)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heapq.heappush(pq, entry)

'''Mark an existing task as REMOVED.'''
def remove_task(task,entry_finder,REMOVED):
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

'''Remove and return the lowest priority task. Raise KeyError if empty.'''
def pop_task(pq,entry_finder,REMOVED):
    while pq:
        priority, count, task = heapq.heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')
  
''' Una coda e' vuota se non ha piu'elementi o se quelli rimasti sono tutti REMOVED '''
def empty(pq,REMOVED):
    if len(pq)==0:
        return True
    else:
        for i in pq:
            if i[2] is not REMOVED:
                return False
    return True