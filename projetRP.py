# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:18:18 2017

@author: 3306788
"""

def read_pct(filename, p):
    
    infile = open ( filename, "r" )    
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split()] 
    #print rows, slots, unavailable, pools, servers 
        
    #nombre de rangees a conserver
    nbRows = int(p*rows/100.)

    #nombre de pools
    nbPools = int(p*pools/100.)
    
    #on cree une instance de data center 
    #la case correspondante au slot vaut 1 s'il est disponible, 0 sinon    
    dataCenter = [[1]*slots for i in range(nbRows)] 

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
            dataCenter[r][s] = 0
    
    
    #nombre de serveurs a allouer
    s = int(p*servers/100.)

    #on remplit pservers, liste  des s premiers serveurs
    #avec leurs taille et capacite respectives 
    pservers = []   
    for i in range(s):
        size, cap = [ int(x) for x in infile.readline().split() ]
        pservers.append([size, cap])    
        #print pservers[-1]

    infile.close()
    return dataCenter, nbPools, pservers
    

dc, pools, servers = read_pct('dc.in', 10)

        


