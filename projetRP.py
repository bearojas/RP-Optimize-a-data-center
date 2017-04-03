# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:18:18 2017

@author: 3306788
"""

#def read_file(filename):
#    
#    #lecture du nombre de rangees, slots par rangee, slots indisponibles, pools et servers
#    infile = open ( filename, "r" )
#    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split() ]    
#
#    print rows, slots, unavailable, pools, servers
#    infile.close()

#lecture de p % des lignes sur les slots non disponibles
def read_p_rows(filename, p):
    infile = open ( filename, "r" )    
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split()]    
    
    r = int(p*rows/100.)
    print r

    #la case correspondante au slot vaut 1 s'il est disponible, 0 sinon
    prows = [[1]*slots for i in range(rows)]   
    
    #lecture des r premieres lignes sur les slots indisponibles
    for i in range(r):
        row, slot = [ int(x) for x in infile.readline().split() ]
        prows[row][slot] = 0

    infile.close()
    return prows
    
#lecture de p % des lignes portant sur les serveurs
def read_p_servers(filename, p):
    infile = open ( filename, "r" )    
    rows, slots, unavailable, pools, servers = [ int(x) for x in infile.readline().split()]    
    
    for i in range(unavailable):
        infile.readline()
    
    s = int(p*servers/100.)
    print s

    #s premiers serveurs avec leurs taille et capacite respectives 
    pservers = []   
    
    #lecture des s premieres lignes sur les serveurs
    for i in range(s):
        size, cap = [ int(x) for x in infile.readline().split() ]
        pservers.append([size, cap])
        print pservers[-1]

    infile.close()
    return pservers
    
    
#read_file('dc.in')
#print read_p_rows('dc.in', 20)
read_p_servers('dc.in', 10)