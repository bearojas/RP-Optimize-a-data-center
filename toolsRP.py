# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:18:18 2017

@author: 3306788
"""

POURCENTAGE = 100

def read_perc(filename, perc):
    
    infile = open ( filename, "r" )    
    #lecture du nombre de rangees, slots par rangee, slots indisponibles, pools et servers
    rows, slots, unavailable, pools, servers = \
    [ int(x) for x in infile.readline().split()] 
        
    #nombre de rangees a conserver
    nbRows = int(perc*rows/100.)
    
    #nombre de pools a conserver 
    nbPools = int(perc*pools/100.)
    
    #on cree une instance de data center 
    #la case correspondante au slot vaut '_' s'il est disponible, X sinon    
    dataCenter = [['_']*slots for i in range(nbRows)] 

    #listes de slots disponibles    
    availableSlots = [[i, j] for i in range(nbRows) for j in range(slots)]
    
    #mise a jour des slots disponibles
    for i in range(unavailable):
        row, slot = [ int(x) for x in infile.readline().split() ]
        
        #si ce slot est dans les rangees conservees
        if row < nbRows:
            availableSlots.remove([row, slot])
            dataCenter[row][slot] = 'X'

    #nombre de serveurs a allouer
    s = int(perc*servers/100.)

    #on remplit pservers, liste  des s premiers serveurs
    #avec leurs numero, taille et capacite respectives 
    pservers = []   
    for i in range(s):
        size, cap = [ int(x) for x in infile.readline().split() ]
        pservers.append([i, size, cap])    
    
    infile.close()
    return dataCenter, nbPools, pservers, availableSlots
    
#sauvegarde de l'instance
def saveSolution(filename, tab_solution):
    solution = open(filename[:-4]+"_sol.txt","w")
    for i in range(len(tab_solution)):
        if tab_solution[i][0] != 'x' :
            row = str(tab_solution[i][0])
            slot = str(tab_solution[i][1])
            pool = str(tab_solution[i][2])
            solution.write(row+" "+slot+" "+pool+"\r\n")
        else:
            solution.write("x \r\n")
    solution.close()
    
    
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
        if tab_solution[i][0] != 'x' :
            row = int(tab_solution[i][0])
            slot = int(tab_solution[i][1])
            pool = tab_solution[i][2]
            for j in range(pservers[i][1]):
                #numero du serveur_numero groupe
                dataCenter[row][slot+j] = str(i)+"_"+str(pool)
    for x in dataCenter :
        print(x)
    

""" server = [numero, taille, capacite]
renvoie l'ensemble Lm des slots a partir desquels le serveur peut etre localise """
def possible_slots(dataCenter, server, first = 0):
    nbRows = len(dataCenter)
    nbSlots = len(dataCenter[0])
    size = server[1]    
    Lm = []
    
    #pour chaque slot de chaque rangee
    #on regarde si on peut placer le serveur de taille "size"
    for row in range(nbRows):
        for slot in range(nbSlots):
            for s in range(size):
                if slot+s >= nbSlots or dataCenter[row][slot+s] == 'X':
                    s = -1
                    break
            #s'il y a assez de place
            if s == size - 1:
                Lm.append([row, slot])
                if(first):
                    return Lm
    
    return Lm

#TEST de possible_slots
#dc, pools, servers, availableSlots = read_perc('test0.txt', POURCENTAGE)
#print (possible_slots(dc, servers[0]))


""" un server = [numero, taille, capacite]
slot = [row, slot]
renvoie l'ensemble Krs des serveurs pouvant être localisé à ce slot"""
def possible_servers(dataCenter, servers, slot, first = 0):
    row = dataCenter[slot[0]] #rangee entiere de ce slot
    s = slot[1]
    Krs = []
    
    dispo = 0
    while s+dispo < len(row) and row[s+dispo] != 'X':
        dispo+=1
        
    if dispo == 0:
        return Krs
        
    for server in servers:
        if server[1] <= dispo:
            Krs.append(server)
            if(first):
                return Krs
    return Krs

#TEST de possible_servers        
#dc, pools, servers, availableSlots = read_perc('test0.txt', POURCENTAGE)
#print (possible_servers(dc, servers, [1, 3]))      
#print (availableSlots)


"""calcul du score"""
def calculScore(servers_alloc, servers, pools, rows):
    
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
        
    return min(pools_score)
    

# retourne les numeros des serveurs inutilises
def getUnusedServers(servers_alloc) :
    
    un_servers =[]
    for i in range(len(servers_alloc)) :
        if servers_alloc[i][0]=='x':
            un_servers.append(i)
    return un_servers
    

