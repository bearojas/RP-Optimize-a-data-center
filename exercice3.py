# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:10:54 2017

@author: clair
"""

from toolsRP import *
from gurobipy import * 

POURCENTAGE = 100

class Server :
    
    def __init__(self, num, taille, cap, dc) :
        self.numero = num
        self.size = taille
        self.capacite = cap
        # Lm = ensemble des slots a partir duquel le serveur peut etre localise
        self.Lm = possible_slots(dc,[num,taille,cap])
        # pour un serveur, conserver les variables le concernant : Zrsi
        # un dico ? de la forme { (r,s,i) : k} ie. pour un slot, k€{0,1} i le groupe
        # pour réduire le nombre de variables : on peut ne conserver que les variables correspondant à Lm
        self.Zrsi = dict()



def initServers(servers, dc) :
    
    l_servers=[]
    
    for s in servers :
        l_servers.append(Server(s[0], s[1], s[2], dc))
    
    return l_servers


def initVariables(servers, rows, slots, pools) :
    
    for serv in servers :
        for rs in serv.Lm :
            for p in range(pools):
                serv.Zrsi[(rs[0],rs[1],p)] = m.addVar(vtype=GRB.BINARY, lb=0, name="z%d,%d,%d,%d" % (serv.numero,rs[0],rs[1],p))




def uniqueAffectationContrainte(servers):
    
    for serv in servers :
        m.addConstr(quicksum(serv.Zrsi[(r,s,i)] for (r,s,i) in serv.Zrsi ) <= 1, "Contrainte_%d" % serv.numero)



def uniqueServeurParSlotContrainte(servers, R, S) :
    
    for r in range(R):
        for s in range(S) :
            


def bestAffectation(filename) :  
    # F = slots disponibles
    # P = nombre de pools à créer
    # M = serveur à positionner
    dataCenter, P, M, F = read_perc(filename,POURCENTAGE)
    # R = nombre de rangées
    R = len(dataCenter)
    # S = nombre de slots par rangée
    S = len(dataCenter[0])
    # U = slots indisponibles
    U = getUaSlots(filename)
    
    """variables"""
    l_servers = initServers(M, dataCenter)
    initVariables(l_servers, R, S, P)
    
    m.update()

    """fonction objective"""
    obj= LinExpr()
    obj = 0
    #TODO
    m.setObjective(obj,GRB.MAXIMIZE)
    
    """contraintes"""
    uniqueAffectationContrainte(l_servers)
    uniqueServeurParSlotContrainte(l_servers, R, S)    
    
    m.optimize()
    
#    print("NUMERO ",l.numero)
#    print("Nombre de variables : ", len(l.Zrsi) )
 
    
m = Model("mogplex")
bestAffectation('test0.txt')