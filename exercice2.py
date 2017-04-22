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
    solution = []    
    score_voisin = 0
    cpt = 0
    updatedCenter = deepcopy(gloutonCenter)
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

            solution_voisine = deepcopy(solution_glouton)
            updatedCenter = deepcopy(gloutonCenter)            
            
            #on enleve le serveur
            r, s = solution_voisine[index][0], solution_voisine[index][1]
            solution_voisine[index] = ['x','x','x']
            for i in range(servers[index][1]):
                updatedCenter[r][s+i] = '_'
                
            score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))
            
            
        #voisinage : placer un serveur non affecte    
        elif alea < 0.6:
            #print("B")
            #tirage aleatoire du serveur a affecte
            # !!!!! BOUCLE : il peut ne pas y avoir de serveurs non affectes -> faire ce qui suit plutôt : getUnusedServers
#            index = random.randint(0, len(servers)-1)
#            while solution_glouton[index] != ['x','x','x']:
#                index = random.randint(0,len(servers)-1)
                    
            #recuperation des serveurs non affectes
            unused_servers = getUnusedServers(solution_glouton)   
                 
            if len(unused_servers)!=0 :
                #tirage aleatoire du serveur a affecter
                index = random.randint(0,len(unused_servers)-1)
                #tirage alea d'un pool
                pool = random.randint(0, pools-1)
                
                #tirage aleatoire de l'emplacement libre
                appliantSlots = possible_slots(gloutonCenter, servers[index])
                
                if len(appliantSlots) != 0:
                    indexSlot = random.randint(0, len(appliantSlots)-1)
                    slot = appliantSlots[indexSlot]
                    
                    updatedCenter = deepcopy(gloutonCenter)
                    for i in range(servers[index][1]):
                        updatedCenter[slot[0]][slot[1]] = 'X'
                    
                    solution_voisine = deepcopy(solution_glouton)
                    solution_voisine[index] = [slot[0], slot[1], pool]
                    score_voisin = calculScore(solution_voisine, servers, pools, len(dataCenter))            
            
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
        if score_voisin > score_glouton:
            print("Meilleur score", score_voisin)
            solution_glouton, score_glouton = solution_voisine, score_voisin
            gloutonCenter=updatedCenter
            cpt = 0
        elif score_voisin == score_glouton:
            solution_glouton, score_glouton = solution_voisine, score_voisin
            gloutonCenter = updatedCenter
        
    return solution_glouton, score_glouton 
        
dataCenter, pools, servers, availableSlots = read_perc('dc.in',POURCENTAGE)        
solution_glouton, score_glouton = stochastique('dc.in', 400)         
displaySolution(solution_glouton, dataCenter, servers)
print("Score final ",score_glouton)






"""question 2"""
# ????????????
#voisinage : échanger deux serveurs sur la ligne la plus forte et ligne plus faible
# sur ligne a la plus grande capacité garantie pour le groupe à la plus petite garantie
# on prend le serveur à la plus grande capacité
# sur la ligne de plus faible capacité garantie pour ce meme groupe on prend un serveur de meme taille que précédemment
# et on swap
# ??????????????