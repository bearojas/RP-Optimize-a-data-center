# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:18:18 2017

@author: 3306788
"""

#import math

POURCENTAGE = 100

def read_perc(filename, perc):
    
    infile = open ( filename, "r" )    
    #lecture du nombre de rangees, slots par rangee, slots indisponibles, pools et servers
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split()] 
    #print rows, slots, unavailable, pools, servers 
        
    #nombre de rangees a conserver
    nbRows = int(perc*rows/100.)
    
    #nombre de pools
    nbPools = int(perc*pools/100.)
    
    #on cree une instance de data center 
    #la case correspondante au slot vaut '_' s'il est disponible, X sinon    
    dataCenter = [['_']*slots for i in range(nbRows)] 

    #liste des slots indisponibles
    uaSlots = []   
    for i in range(unavailable):
        row, slot = [ int(x) for x in infile.readline().split() ]
        uaSlots.append([row, slot])
        #print uaSlots[-1]
    
    #mise a jour des slots indisponible dans dataCenter          
    for r, s in uaSlots:
        #si ce slot est dans les rangees conservees
        if r < nbRows: 
            dataCenter[r][s] = 'X'
    
    
    #nombre de serveurs a allouer
    s = int(perc*servers/100.)

    #on remplit pservers, liste  des s premiers serveurs
    #avec leurs numero, taille et capacite respectives 
    pservers = []   
    for i in range(s):
        size, cap = [ int(x) for x in infile.readline().split() ]
        pservers.append([i, size, cap])    
    
    infile.close()
    return dataCenter, nbPools, pservers
    


#affichage de l'instance du problème
def displayInstance (dataCenter, pools, servers) :
    print ("Pourcentage à lire : ", POURCENTAGE)  
    print ("Nombre de rangees :", len(dataCenter))
    print ("Nombre de slots par rangee :", len(dataCenter[0]))
    #print "Nombre de slots indisponibles  :", unavailable
    print( "Nombre de serveurs :", len(servers))
    print ("Nombre de pools :", pools)
    print ("*************INSTANCE INITIALE****************")
    for x in dataCenter:
        print (x)
        
        
#affichage d'une instance solution
def displaySolution(tab_solution, dataCenter, pservers):
    print("************SOLUTION***************")
    for i in range(len(tab_solution)):
        if tab_solution[i][0] != 'X' :
            row = int(tab_solution[i][0])
            slot = int(tab_solution[i][1])
            pool = tab_solution[i][2]
            for j in range(pservers[i][1]):
                #numero du serveur_numero groupe
                dataCenter[row][slot+j] = str(i)+"_"+str(pool)
    for x in dataCenter :
        print(x)
    


def glouton_1(filename) :
      
    dataCenter, pools, servers = read_perc(filename,POURCENTAGE)
    rows = len(dataCenter)
    slots = len(dataCenter[0])
    
    """allocation des serveurs"""
    #trier les serveurs par ordre décroissant de capacités
    servers.sort(key=lambda colonnes : colonnes[2], reverse=True )
    
    #creation d'un tableau de taille nbServers avec pour chaque case un petit tableau 
    #à 3 éléments [rangée, slot, pool] initialisé à x
    servers_alloc = [['X']*3 for i in range(len(servers))]    
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


    """calcul du score"""
    #tableau des scores indexé par les groupes
    pools_score = [0]*pools    
    #pour chaque pool, on récupère la somme minimum assurée par chaque rangée - 1
    for p in range(pools) :
        #récuperer l'ensemble des serveurs de ce groupe
        sum_rows = [0]*rows
        for j in range(len(servers_alloc)) :
            if(servers_alloc[j][2] == p):
                #puis pour chaque rangée, faire la somme des capacités des serveurs(stockées dans un tableau ?)
                sum_rows[servers_alloc[j][0]] += servers[j][2]
        # on fait la somme de toutes les lignes minus une ligne a chaque fois et on garde le min
        min_sum = 9999999
        for r in range(rows): 
            somme = sum(sum_rows)
            somme-=sum_rows[r]
            if somme < min_sum:
                min_sum = somme
        pools_score[p] = min_sum
        
    score = min(pools_score)
    return servers_alloc, score

 
#tests
solution_glouton, solution_score = glouton_1('test0.txt')
dc, pools, servers = read_perc('test0.txt', POURCENTAGE)
#dc, pools, servers = read_perc('dc.in', POURCENTAGE)
displayInstance(dc, pools, servers)
#solution_glouton, solution_score = glouton_1('dc.in')
#solution_glouton = glouton_1('dc.in')
print (solution_glouton)
print (solution_score)

displaySolution(solution_glouton, dc, servers)
#print("Score de cette solution :", solution_score)