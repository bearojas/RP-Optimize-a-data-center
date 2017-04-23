# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:34:31 2017

@author: 3206957
"""

from toolsRP import *
from exercice1 import *
import random
from copy import deepcopy

POURCENTAGE =100
"""question 1"""


#solution_glouton: [rangée, slot, pool] si serveur affecte
#                   ['x','x','x']       sinon                    
def stochastique(filename, maxIter):

    dataCenter, pools, servers, availableSlots = read_perc(filename,POURCENTAGE)
    solution_glouton, score_glouton, gloutonCenter = glouton_2(dataCenter, pools, servers, availableSlots )
    print("Score initial ", score_glouton)
    print("Solution initiale")
    displaySolution(solution_glouton,dataCenter,servers)
    #recuperation des id des serveurs non affectes
    unused_servers = getUnusedServers(solution_glouton) 
    
    solution_voisine = []    
    score_voisin = 0
    cpt = 0 
    
    while cpt < maxIter:
        cpt+=1
        alea = random.random()
        
        #voisinage : enlever un serveur
        if alea < 0.3:
            #print("A")
        
            #tirage aleatoire du serveur a enlever : s'il n'était pas utilisé, en prendre un autre
            index = random.randint(0, len(servers)-1)
            while solution_glouton[index] == ['x','x','x']:
                index = random.randint(0,len(servers)-1)
            
            ##print ("A: serveur a enlever: ", index)
            solution_voisine = deepcopy(solution_glouton)                   
            #on enleve le serveur
            r, s = solution_voisine[index][0], solution_voisine[index][1]
            solution_voisine[index] = ['x','x','x']
            score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))
            
            
        #voisinage : placer un serveur non affecte    
        elif alea < 0.6:

            #print("B")               
            ##print ("B: unused_servers: ", unused_servers)     
            if len(unused_servers)!=0 :
                #tirage aleatoire du serveur a affecter
                rd = random.randint(0,len(unused_servers)-1)
                index = unused_servers[rd]
                #tirage alea d'un pool
                pool = random.randint(0, pools-1)
                ##print ("B: serveur a affecte: ", index)
                
                #tirage aleatoire de l'emplacement libre
                appliantSlots = possible_slots(gloutonCenter, servers[index])
                ##print ("B: slots possibles: ", appliantSlots)
                if len(appliantSlots) != 0:
                    indexSlot = random.randint(0, len(appliantSlots)-1)
                    slot = appliantSlots[indexSlot]
                    #on affecte le serveur
                    ##print ("slot choisi: ", slot)
                    solution_voisine = deepcopy(solution_glouton)
                    solution_voisine[index] = [slot[0], slot[1], pool]
                    score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))
                else:
                    continue
            else:
                continue
            
        #voisinage : changer le pool d'un serveur deja affecte
        else:
            #print("C")
            #tirage aleatoire d'un serveur deja affecte
            index = random.randint(0, len(solution_glouton)-1)
            chosenOne = solution_glouton[index]
            
            while chosenOne == ['x','x','x']:
                index = random.randint(0, len(solution_glouton)-1)
                chosenOne = solution_glouton[index] 
                
            #tirage alea d'un pool
            pool = random.randint(0, pools-1)
            
            while pool == chosenOne[2]:
                pool = random.randint(0, pools-1)                
            
            solution_voisine = deepcopy(solution_glouton)
            solution_voisine[index][2] = pool
            
            score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))

        #si on a trouve une meilleure solution
        if score_voisin >= score_glouton:
            #print("Meilleur score", score_voisin)
            solution_glouton, score_glouton = solution_voisine, score_voisin

            #mise a jour des serveurs non affectes et du centre     
            if alea < 0.3:      
                unused_servers.append(index)
                for i in range(servers[index][1]):
                    gloutonCenter[r][s+i] = '_'
                    
            elif alea < 0.6:
                unused_servers.pop(rd)
                for i in range(servers[index][1]):
                    gloutonCenter[slot[0]][slot[1]+i] = 'X'
                    
            if score_voisin > score_glouton:
                cpt = 0
                
        
    return solution_glouton, score_glouton 
        
#dataCenter, pools, servers, availableSlots = read_perc('dc.in',POURCENTAGE)        
#solution_glouton, score_glouton = stochastique('dc.in', 800)         
#displaySolution(solution_glouton, dataCenter, servers)
#print("Score final ",score_glouton)

#dataCenter, pools, servers, availableSlots = read_perc('test1.txt',POURCENTAGE)        
#solution_glouton, score_glouton = stochastique('test1.txt', 0)         
#displaySolution(solution_glouton, dataCenter, servers)
#print("Score final ",score_glouton)



"""question 2"""
# ????????????
#voisinage : échanger deux serveurs sur la ligne la plus forte et ligne plus faible
# sur ligne a la plus grande capacité garantie pour le groupe à la plus petite garantie
# on prend le serveur à la plus grande capacité
# sur la ligne de plus faible capacité garantie pour ce meme groupe on prend 
#un serveur de meme taille que précédemment
# et on swap
# ??????????????

""" alternative au voisinage b (on garde les deux autres)
lors du calcul du score
- on determine aussi la rangee et le pool responsables de ce score 
- on choisit le serveur de plus grande capacite dans cette rangee, de ce pool
- on l'affecte autre part """


def stochastique_2(filename, maxIter):

    dataCenter, pools, servers, availableSlots = read_perc(filename,POURCENTAGE)
    solution_glouton, score_glouton, gloutonCenter = glouton_2(dataCenter, pools, servers, availableSlots )
    print("Score initial ", score_glouton)
    print("Solution initiale")
    displaySolution(solution_glouton,dataCenter,servers)
    #recuperation des id des serveurs non affectes
    unused_servers = getUnusedServers(solution_glouton) 
    
    dico_alloc = servers_per_pool(solution_glouton, pools)
    solution_voisine = []    
    score_voisin = 0
    cpt = 0 
    
    while cpt < maxIter:
        cpt+=1
        alea = random.random()
        
        #voisinage : enlever un serveur
        if alea < 0.4:
            #print("A")
        
            #tirage aleatoire du serveur a enlever : s'il n'était pas utilisé, en prendre un autre
            index = random.randint(0, len(servers)-1)
            while solution_glouton[index] == ['x','x','x']:
                index = random.randint(0,len(servers)-1)
            
            #print ("A: serveur a enlever: ", index)
            solution_voisine = deepcopy(solution_glouton)                   
            #on enleve le serveur
            r, s, p = solution_voisine[index]
            solution_voisine[index] = ['x','x','x']
            score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))
            
        else:
            #print("B") 

            #lorsque le dernier parametre vaut 1, on retourne aussi 
            #le pool et la rangee responsable du score   
                      
            score, badPool, badRow = calculScore(solution_glouton, servers, pools, len(dataCenter), 1)

            #on cherche le serveur non alloue de meilleure capacité
            best_cap = 0
            for serv in unused_servers:
                if servers[serv][2] > best_cap:
                    best_cap = servers[serv][2]
                    best_serv = servers[serv]
            
            ##print ("B: serveur a alloue", best_serv[0])
            appliantSlots = possible_slots(gloutonCenter, best_serv)
            ##print("B: slots possibles", appliantSlots)
            if len(appliantSlots)!=0:
                for x in appliantSlots:
                    if x[0] == badRow:
                        appliantSlots.remove(x)
                        
                if  len(appliantSlots)!=0:
                    continue
                
                indexSlot = random.randint(0, len(appliantSlots)-1)
                slot = appliantSlots[indexSlot]
                ##print("B:slot choisi", slot)
                #on affecte le serveur
                solution_voisine = deepcopy(solution_glouton)
                solution_voisine[best_serv[0]] = [slot[0], slot[1], badPool]
                score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))                
            else:
                continue
            
        #voisinage : placer un serveur du pool et de la rangee responsables 
        #du score autre part
#        else:
#            #print("B") 
#
#            #lorsque le dernier parametre vaut 1, on retourne aussi 
#            #le pool et la rangee responsable du score   
#                      
#            score, badPool, badRow = calculScore(solution_glouton, servers, pools, len(dataCenter), 1)
#
#            best_cap = 0
#            #pour chaque serveur [id, row, slot] de ce pool
#            for serv in dico_alloc[badPool]:
#                if serv[1] == badRow: #le serveur est dans la rangee concernee
#                    #si ce serveur a une meilleure capacite                    
#                    if servers[serv[0]][2] > best_cap:
#                        best_serv = serv
#                        best_cap = servers[best_serv[0]][2]
#            ##print ("B: serveur a alloue", best_serv[0])
#            appliantSlots = possible_slots(gloutonCenter, servers[best_serv[0]])
#            ##print("B: slots possibles", appliantSlots)
#            if(len(appliantSlots)!=0):
#                indexSlot = random.randint(0, len(appliantSlots)-1)
#                slot = appliantSlots[indexSlot]
#                ##print("B:slot choisi", slot)
#                #on affecte le serveur
#                solution_voisine = deepcopy(solution_glouton)
#                solution_voisine[best_serv[0]] = [slot[0], slot[1], badPool]
#                score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))                
#            else:
#                continue
            
        #voisinage : changer le pool d'un serveur deja affecte
#        else:
#            #print("C")
#            #tirage aleatoire d'un serveur deja affecte
#            index = random.randint(0, len(solution_glouton)-1)
#            chosenOne = solution_glouton[index]
#            
#            while chosenOne == ['x','x','x']:
#                index = random.randint(0, len(solution_glouton)-1)
#                chosenOne = solution_glouton[index] 
#                
#            #tirage alea d'un pool
#            pool = random.randint(0, pools-1)
#            
#            while pool == chosenOne[2]:
#                pool = random.randint(0, pools-1)                
#            
#            solution_voisine = deepcopy(solution_glouton)
#            solution_voisine[index][2] = pool
#            
#            score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))
#
        #si on a trouve une meilleure solution
        if score_voisin >= score_glouton:
            #print("Meilleur score", score_voisin)
            solution_glouton, score_glouton = solution_voisine, score_voisin
            
            #mise a jour des serveurs non affectes et du centre     
            if alea < 0.4:
                unused_servers.append(index)
                #dico_alloc[p].remove([index, r, s])            
                for i in range(servers[index][1]):
                    gloutonCenter[r][s+i] = '_'
            else:
                unused_servers.remove(best_serv[0])
                for i in range(best_serv[1]):
                    gloutonCenter[slot[0]][slot[1]+i] = 'X'
#            else:
#                for i in range(servers[best_serv[0]][1]):
#                    gloutonCenter[best_serv[1]][best_serv[2]+i] = '_'
#                dico_alloc[badPool].remove(best_serv)
#                    
#                for i in range(servers[best_serv[0]][1]):
#                    gloutonCenter[slot[0]][slot[1]+i] = 'X'
#                dico_alloc[badPool].append([best_serv[0], slot[0], slot[1]])
#            else:
#                dico_alloc[chosenOne[2]].remove([index, chosenOne[0], chosenOne[1]])
#                dico_alloc[pool].append([index, chosenOne[0], chosenOne[1]])
                    
            if score_voisin > score_glouton:
                cpt = 0   
        
    return solution_glouton, score_glouton 
    
#dataCenter, pools, servers, availableSlots = read_perc('dc.in',POURCENTAGE)        
#solution_glouton, score_glouton = stochastique_2('dc.in', 100)         
#displaySolution(solution_glouton, dataCenter, servers)
#print("Score final ",score_glouton)
    
#dataCenter, pools, servers, availableSlots = read_perc('test1.txt',POURCENTAGE)        
#solution_glouton, score_glouton, gloutonCenter = glouton_2(dataCenter, pools, servers, availableSlots )
#print servers_per_pool(solution_glouton, pools)