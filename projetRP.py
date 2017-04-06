# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:18:18 2017

@author: 3306788
"""
#j'ai separé la lecture du fichier en plusieurs fonctions car c'etait demandé dans l'énoncé
#mais pour moi c'est plus logique de tout faire dans une seule fonction de lecture
#je trouve que la partie 2 de l'énoncé est bizarrement faite...


#lecture de p % des lignes concernant les slots indisponibles
def read_p_rows(filename, p):
    infile = open ( filename, "r" )    
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split()]    
    
    r = int(p*rows/100.)
    print( r)
    #on calcule le nb de lignes a lire
    r = int(p*unavailable/100.)

    #on remplit uaSlots, liste des r premiers slots indisponibles
    uaSlots = []   
    for i in range(r):
        row, slot = [ int(x) for x in infile.readline().split() ]
        uaSlots.append([row, slot])
        #print uaSlots[-1]
        

    infile.close()
    return uaSlots
    
#lecture de p % des lignes concernant les serveurs
def read_p_servers(filename, p):
    infile = open ( filename, "r" )    
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split()]    
    
    #on saute les lignes concernant les slots 
    for i in range(unavailable):
        infile.readline()
    
    s = int(p*servers/100.)

    print (s)

    #on remplit pservers, liste  des s premiers serveurs
    #avec leurs taille et capacite respectives 
    pservers = []   
    for i in range(s):
        size, cap = [ int(x) for x in infile.readline().split() ]
        pservers.append([size, cap])
        print (pservers[-1])

        #print pservers[-1]

    infile.close()
    return pservers
    

#read_p_rows('dc.in', 20)
#read_p_servers('dc.in', 10)

def display(filename):
    
    #lecture du nombre de rangees, slots par rangee, slots indisponibles, pools et servers
    infile = open ( filename, "r" )
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split() ]    
    infile.close()
    
    uaSlots = read_p_rows(filename, 100)
    #servers = read_p_servers(filename, 100)

    #la case correspondante au slot vaut 1 s'il est disponible, 0 sinon    
    dataCenter = [[1]*slots for i in range(rows)] 
    
    for r, s in uaSlots:
        dataCenter[r][s] = 0
        
    
    for x in dataCenter:
        print (x)
        
#display('dc.in')
        
    
    
    
    

#read_file('dc.in')
print (read_p_rows('dc.in', 20))
read_p_servers('dc.in', 10)

