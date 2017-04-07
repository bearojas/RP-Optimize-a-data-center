# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:18:18 2017

@author: 3306788
"""
POURCENTAGE = 20

#lecture du nombre de rangées, slots, slots indisponibles, pools et serveurs
def read_data(filename,perc):
    infile = open ( filename, "r" )    
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split()] 
    infile.close()
    return int(perc*rows/100.), slots,unavailable, int(perc*pools/100.), int(perc*servers/100.)
    
#lecture des lignes concernant les slots indisponibles
def read_p_rows(filename, rows, slots, unavailable):
    infile = open ( filename, "r" )    
    infile.readline()
    #on remplit uaSlots, liste des r premiers slots indisponibles
    uaSlots = []   
    for i in range(unavailable):
        row, slot = [ int(x) for x in infile.readline().split() ]
        if row < rows :
            uaSlots.append([row, slot])
        
    infile.close()
    return uaSlots
    
#lecture des lignes concernant les serveurs
def read_p_servers(filename, unavailable,servers, pools):
    infile = open ( filename, "r" )        
    #on saute les lignes concernant les slots + la premiere ligne
    infile.readline()
    for i in range(unavailable):
        infile.readline()
    #on remplit pservers, liste  des s premiers serveurs
    #avec leurs numero,  taille et capacite respectives 
    pservers = []   
    for i in range(servers):
        size, cap = [ int(x) for x in infile.readline().split() ]
        pservers.append([i, size, cap])

    infile.close()
    return pservers
    

#création de l'instance avec le pourcentage souhaité
def createInstance(filename, perc):
    #lecture du nombre de rangees, slots par rangee, slots indisponibles, pools et servers
    infile = open ( filename, "r" )
    rows, slots, unavailable, pools, servers = read_data(filename,perc)    
    infile.close()
    
    uaSlots = read_p_rows(filename, rows, slots, unavailable)
    pservers = read_p_servers(filename, unavailable, servers, pools)

    #la case correspondante au slot vaut '_' s'il est disponible, X sinon    
    dataCenter = [['_']*slots for i in range(rows)] 
    
    for r, s in uaSlots:
        dataCenter[r][s] ='X'
       
    return dataCenter, pservers, rows, slots, unavailable, pools, servers

#affichage de l'instance du problème
def displayInstance (dataCenter, rows, slots, unavailable, pools, servers) :
    print("Pourcentage à lire : ",POURCENTAGE)  
    print("Nombre de rangees :",rows)
    print("Nombre de slots par rangee :", slots)
    print("Nombre de slots indisponibles  :", unavailable) 
    print ("Nombre de serveurs :",servers)
    print("Nombre de pools :",pools)
    print("*************INSTANCE INITIALE****************")
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
    print (dataCenter)
    
    
#read_file('dc.in')
#print (read_p_rows('dc.in', 100))
#print(read_p_servers('dc.in', 10))
#displayInstance(createInstance('dc.in',10)[0])

def glouton_1(filename) :
      
    dataCenter, pservers, rows, slots, unavailable, pools, servers= createInstance(filename,POURCENTAGE)
    #trier les serveurs par ordre décroissant de capacités
    pservers.sort(key=lambda colonnes : colonnes[2], reverse=True )
    #creation d'un tableau de taille nbServers avec pour chaque case un petit tableau à 3 éléments [rangée, slot, pool] initialisé à XXX
    servers_affect = [['X']*3 for i in range(servers)]    
    gr = 0 #pool
    #pour chaque serveur dans pservers
    for i in range(len(pservers)):
        # on regarde le nombre de slots nbSlot nécessaires
        nbSlot = pservers[i][1] 
        numServ = pservers[i][0] 
        isAffected = False
        #dans dataCenter, on parcourt et on regarde si il y a nbSlot emplacements consécutifs
        k = 0 #rangee
        j=0
        #tant qu'on a pas affecté le serveur et qu'il reste des rangées
        while isAffected==False and k < len(dataCenter) :
            cpt = 0
            isAffected = True
            #on compte le nombre de slots libres tant qu'il reste des slots sur la rangée
            while cpt < nbSlot and j+cpt < slots:
                if dataCenter[k][j+cpt] == 'X' :
                    isAffected = False  
                    cpt+=1
                    break
                cpt+=1
            #si on est arrivé au bout de la rangée et qu'on a pas placé le serveur, on change de rangée
            if j+cpt >= slots and cpt < nbSlot :
                j=0
                k+=1
                isAffected = False
            #si il ya assez de slots libres, le mettre et l'affecter au pool gr (on incrémente à chaque fois de 1)
            if isAffected == True :
                servers_affect[numServ] = [k,j, gr]
                gr = (gr+1)%pools
                for index in range(nbSlot) :
                    dataCenter[k][j+index]='X'
            #sinon, serveur non utilisé [X,X,X]
            j+=cpt

    #calcul du score
    #tableau des scores indexé par les groupes
    pools_score = [0]*pools    
    #pour chaque pool, on récupère la somme minimum assurée par chaque rangée - 1
    #pour chaque pool
    for i in range(pools) :
        #récuperer l'ensemble des serveurs de ce groupe
        sum_rows = [0]*rows
        for j in range(len(servers_affect)) :
            if(servers_affect[j][2] == i):
                #puis pour chaque rangée, faire la somme des capacités des serveurs(stockées dans un tableau ?)
                sum_rows[servers_affect[j][0]] += pservers[j][2]
        # puis on fait la somme de toutes les lignes minus une ligne a chaque fois et on garde le min
        min_sum = 250000 
        for r in range(rows):
            somme = sum(sum_rows)
            somme-=sum_rows[r]
            if somme < min_sum:
                min_sum = somme
        pools_score[i] = min_sum
        
    score = min(pools_score)
    return servers_affect, score

dataCenter, pservers, rows, slots, unavailable, pools, servers = createInstance('dc.in',POURCENTAGE)
displayInstance(dataCenter, rows, slots, unavailable, pools, servers)
solution_glouton, solution_score = glouton_1('dc.in')
displaySolution(solution_glouton,dataCenter, pservers)
print("Score de cette solution :", solution_score)