# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:27:59 2017

@author: 3206957
"""
from toolsRP import *
from copy import deepcopy

POURCENTAGE = 100

def glouton_1(dc, pools, servers, availableSlots ) :
    
    dataCenter = deepcopy(dc)
    rows = len(dataCenter)
    slots = len(dataCenter[0])
    
    #allocation des serveurs
    
    #trier les serveurs par ordre décroissant de capacités
    servers.sort(key=lambda colonnes : colonnes[2], reverse=True )
    
    #creation d'un tableau de taille nbServers avec pour chaque case un petit tableau 
    #à 3 éléments [rangée, slot, pool] initialisé à x
    servers_alloc = [['x']*3 for i in range(len(servers))]    
    gr = 0 #pool
    
    #pour chaque serveur dans servers
    for i in range(len(servers)):
        # on regarde le nombre de slots nbSlot nécessaires
        nbSlot = servers[i][1] 
        numServ = servers[i][0]
        isAssigned = False
        
        #dans dataCenter, on parcourt et on regarde si il y a nbSlot emplacements consécutifs
        k = 0 #rangee
        j = 0 #slot
        #tant qu'on a pas affecté le serveur et qu'il reste des rangées
        while isAssigned == False and k < rows :
            cpt = 0
            #on compte le nombre de slots libres tant qu'il reste des slots sur la rangée
            while cpt < nbSlot and j+cpt < slots:
                if dataCenter[k][j+cpt] == 'X' :
                    j = j+cpt+1
                    cpt = 0
                else: 
                    cpt+=1
            #si on est arrivé au bout de la rangée et qu'on a pas placé le serveur, on change de rangée
            if j+cpt >= slots and cpt < nbSlot :
                j=0
                k+=1
            #si il y a assez de slots libres, le mettre et l'affecter au pool gr (on incrémente à chaque fois de 1)
            else:
                isAssigned = True
                servers_alloc[numServ] = [k,j, gr]
                gr = (gr+1)%pools
                for index in range(nbSlot) :
                    dataCenter[k][j+index]='X'

    
    score = calculScore(servers_alloc, servers, pools, rows)
    return servers_alloc, score

#tests glouton 1
#dc, pools, servers, availableSlots = read_perc('test0.txt', POURCENTAGE)
#solution_glouton, solution_score = glouton_1(dc, pools, servers, availableSlots )

#dc, pools, servers, availableSlots = read_perc('dc.in', POURCENTAGE)
#displayInstance(dc, pools, servers)
#solution_glouton, solution_score = glouton_1(dc, pools, servers, availableSlots)
#displaySolution(solution_glouton, dc, servers)
#print("Score de cette solution :", solution_score)



def glouton_2(dataCenter, pools, servers, availableSlots ):
    
    """allocation des serveurs"""
    #trier les serveurs par ordre décroissant de taille puis de capacités
    serversCopy = deepcopy(servers)
    serversCopy.sort(key=lambda colonnes : (colonnes[1], colonnes[2]), reverse=True )
    
    #creation d'un tableau de taille nbServers avec pour chaque case un petit tableau 
    #à 3 éléments [rangée, slot, pool] initialisé à x
    servers_alloc = [['x']*3 for i in range(len(serversCopy))]    
    gr = 0 #pool
    
    #parcours de tous les slots disponibles
    while len(availableSlots) != 0:
        slot = availableSlots[0]
        #ensemble des serveurs non alloues possibles pour ce slot, tries par ordre decroissant de taille et capacite
        appliantServers = possible_servers(dataCenter, serversCopy, slot)
        
        if len(appliantServers) != 0:
            #on choisit celui qui occupe plus de slots et a la meilleure capacite
            chosenOne = appliantServers[0]
            #le serveur est deja alloue
            serversCopy.remove(chosenOne)
            
            #mise a jour des slots disponibles
            size = chosenOne[1]
            for i in range(size):
                availableSlots.remove([slot[0], slot[1]+i])
            
            #allocation du serveur
            servers_alloc[chosenOne[0]] = [slot[0], slot[1], gr]
            gr = (gr+1)%pools
        #si on ne peut pas assigne de serveur a ce slot, on retire le slot
        else:
            availableSlots.remove(slot)
    
            
    return servers_alloc, calculScore(servers_alloc, servers, pools, len(dataCenter))


#tests glouton_2
#dc, pools, servers, availableSlots = read_perc('test0.txt', POURCENTAGE)
#solution_glouton, solution_score = glouton_2(dc, pools, servers, availableSlots)
#print solution_glouton
#print solution_score

#dc, pools, servers, availableSlots = read_perc('dc.in', POURCENTAGE)
#solution_glouton1, solution_score1 = glouton_2(dc, pools, servers, availableSlots)
#displaySolution(solution_glouton, dc, servers)
#print("Score de cette solution :", solution_score1)