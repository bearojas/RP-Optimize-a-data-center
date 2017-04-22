# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:27:59 2017

@author: 3206957
"""
from toolsRP import *
from copy import deepcopy

POURCENTAGE =100


def new_glouton_1(dc, pools, serv, availableSlots ) :    
    dataCenter = deepcopy(dc)
    servers = deepcopy(serv)
    #trier les serveurs par ordre décroissant de capacités
    servers.sort(key=lambda colonnes : colonnes[2], reverse=True )
    
    #tableau contenant pour chaque serveur une liste [rangée, slot, pool]
    #initialisé à 'x x x'
    affectation = [['x']*3 for i in range(len(servers))]    
    gr = 0 #pool
    
    #pour chaque serveur
    for server in servers:
        numServ = server[0] # id du serveur
        nbSlot = server[1] # nombre de slots nécessaires
        
        #ensemble des slots à partir desquels le serveur peut être localisé
        # 1 = on ne retourne que le premier slot
        appliantSlot = possible_slots(dataCenter, server, 1)
        
        if len(appliantSlot) != 0:
            #on chosit le premier slot disponible
            chosenOne = appliantSlot[0]
            
            affectation[numServ] = [chosenOne[0], chosenOne[1], gr]
            gr = (gr+1)%pools
            
            #mise a jour des slots disponibles dans dataCenter
            for index in range(nbSlot) :
                dataCenter[chosenOne[0]][chosenOne[1]+index]='X'

    score = calculScore(affectation, servers, pools, len(dataCenter))
    return affectation, score


def glouton_1(dc, pools, serv, availableSlots ) :
    
    dataCenter = deepcopy(dc)
    rows = len(dataCenter)
    slots = len(dataCenter[0])
    servers = deepcopy(serv)
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
#displaySolution(solution_glouton, dc, servers)
#saveSolution('test0.txt', solution_glouton)

#dc, pools, servers, availableSlots = read_perc('dc.in', POURCENTAGE)
#displayInstance(dc, pools, servers)
#solution_glouton, solution_score = glouton_1(dc, pools, servers, availableSlots)
#displaySolution(solution_glouton, dc, servers)
#print("Score de cette solution :", solution_score)



def glouton_2(dataCenter, pools, servers, availableSlots ):
    serversCopy = deepcopy(servers)
    centerCopy = deepcopy(dataCenter)

    #trier les serveurs par ordre décroissant de capacites et ordre croissant de taille  
    serversCopy.sort(key=lambda colonnes : (colonnes[2], -colonnes[1]), reverse=True )
    
    #tableau contenant pour chaque serveur une liste [rangée, slot, pool]
    #initialisé à 'x x x'
    servers_alloc = [['x']*3 for i in range(len(serversCopy))]    
    gr = 0 #pool
    
    #parcours de tous les slots disponibles
    while len(availableSlots) != 0:
        slot = availableSlots[0]
        #premier serveur de la liste triee de serveurs non alloues possibles pour ce slot
        appliantServer = possible_servers(dataCenter, serversCopy, slot, 1)
        
        if len(appliantServer) != 0:
            #serveur qui occupe moins de slots et a la meilleure capacite
            chosenOne = appliantServer[0]
            #le serveur est deja alloue
            serversCopy.remove(chosenOne)
            
            #mise a jour des slots disponibles
            size = chosenOne[1]
            for index in range(size):
                availableSlots.remove([slot[0], slot[1]+index])
                centerCopy[slot[0]][slot[1]+index]='X'
            
            #allocation du serveur
            servers_alloc[chosenOne[0]] = [slot[0], slot[1], gr]
            gr = (gr+1)%pools
        #si on ne peut pas assigne de serveur a ce slot, on retire le slot
        else:
            availableSlots.remove(slot)
    
    return servers_alloc, calculScore(servers_alloc, servers, pools, len(dataCenter)), centerCopy


#tests glouton_2
#dc, pools, servers, availableSlots = read_perc('test0.txt', POURCENTAGE)
#solution_glouton, solution_score, center = glouton_2(dc, pools, servers, availableSlots)
#print solution_glouton
#print solution_score
#saveSolution('test0.txt', solution_glouton)
#
#dc, pools, servers, availableSlots = read_perc('dc.in', POURCENTAGE)
#solution_glouton1, solution_score1, center = glouton_2(dc, pools, servers, availableSlots)
#displaySolution(solution_glouton1, dc, servers)
#print("Score de cette solution :", solution_score1)
#displayInstance(center, pools, servers)