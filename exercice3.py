# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:10:54 2017

@author: clair
"""
#!/usr/bin/python
from toolsRP import *
from gurobipy import * 

POURCENTAGE = 20

class Server :
    
    def __init__(self, num, taille, cap, dc) :
        self.numero = num
        self.size = taille
        self.capacite = cap
        # Lm = ensemble des slots a partir duquel le serveur peut etre localise
        self.Lm = possible_slots(dc,[num,taille,cap])
        # pour un serveur, conserver les variables le concernant : Zrsi
        # un dico de la forme { (r,s,i) : k} ie. pour un slot, k€{0,1} i le groupe
        # pour réduire le nombre de variables : on peut ne conserver que les variables correspondant à Lm
        self.Zrsi = dict()


#creation des objets servers
def initServers(servers, dc) :
    
    l_servers=[]
    
    for s in servers :
        l_servers.append(Server(s[0], s[1], s[2], dc))
    
    return l_servers


#creation des variables
def initVariables(servers, rows, slots, pools) :
    # variables Zmrsi
    for serv in servers :
        for rs in serv.Lm :
            for p in range(pools):
                serv.Zrsi[(rs[0],rs[1],p)] = m.addVar(vtype=GRB.BINARY, lb=0, name="z%d,%d,%d,%d" % (serv.numero,rs[0],rs[1],p))
    
    # variables pour le minimum de chaque groupe
    t = []
    for i in range(pools) :
        t.append(m.addVar(vtype=GRB.INTEGER, lb=0, name="t%d" %i))
    
    return t



#un serveur est affecté une seule fois
def uniqueAffectationContrainte(servers):
    
    for serv in servers :
        m.addConstr(quicksum(serv.Zrsi[(r,s,i)] for (r,s,i) in serv.Zrsi ) <= 1, "Contrainte_%d" % serv.numero)



#chaque slot contient au plus un serveur
def uniqueServeurParSlotContrainte(servers, R, S, P) :
    
    for r in range(R):
        for s in range(S) :
            m.addConstr( quicksum(serv.Zrsi[(r,s,p)] for serv in servers if [r,s] in serv.Lm for p in range(P)) <= 1, "Contrainte_%d_%d" %(r,s))



# un serveur ne peut pas avoir comme slot initial un slot occupé par un autre serveur
def aucunServeurSurSlotOccupeContrainte(servers, P) :

    for serv in servers :
        for (r,s,i) in serv.Zrsi :
            m.addConstr(serv.Zrsi[(r,s,i)] + quicksum(otherServ.Zrsi[(r,s+k,p)] for otherServ in servers if otherServ != serv for k in range(serv.size) for p in range(P) if(r,s+k,p) in otherServ.Zrsi) <=1, "Contrainte_k_%d_%d_%d_%d" %(serv.numero,r,s,i))


 
# variable t (minimum pour un groupe) 
# sous contrainte : t <= à chaque min de somme des rangées minus une
def tInferieurAuMinSommeRangeesContrainte(servers, t, R) :
    
    for i in range(len(t)) :
        for k in range(R) :
            m.addConstr( t[i] <= quicksum( serv.Zrsi[(r,s,i)] * serv.capacite for serv in servers for [r,s] in serv.Lm ) - quicksum(serv.Zrsi[(k,s,i)] * serv.capacite for serv in servers for [r,s] in serv.Lm if r==k), "Contrainte_t%d_%d" %(i, k) )
 
 
 
# variable x  : max x
# sous contrainte : x <= à chaque min de groupe (donc a chaque t)
def xInferieurAuMinPoolsContrainte(x,t) : 

    for i in range(len(t)) :
        m.addConstr( x <= t[i], "Contrainte_x%d" %i)



# cree le tableau d'affectation des serveurs obtenu
# permet d'appeler displaySolution apres
def createServersAlloc(servers) :
    
    servers_alloc = [['x']*3 for i in range(len(servers))]

    for serv in servers :
        for (r,s,i) in serv.Zrsi :
            if serv.Zrsi[(r,s,i)].x == 1 :
                servers_alloc[serv.numero] = [r,s,i]
                break ;
    
    return servers_alloc
    



def bestAffectation(filename) :  
    # F = slots disponibles
    # P = nombre de pools à créer
    # M = serveur à positionner
    dataCenter, P, M, F = read_perc(filename,POURCENTAGE)
    # R = nombre de rangées
    R = len(dataCenter)
    # S = nombre de slots par rangée
    S = len(dataCenter[0])
    
    """variables"""
    x = m.addVar(vtype=GRB.INTEGER, lb=0, name ="x")
    l_servers = initServers(M, dataCenter)
    # on peut faire un liste de t : variable pour chaque groupe
    t = initVariables(l_servers, R, S, P)

    m.update()

    """fonction objective"""
    obj= LinExpr()
    obj = 1*x
    
    m.setObjective(obj,GRB.MAXIMIZE)
    
    """contraintes"""
    uniqueAffectationContrainte(l_servers)
    uniqueServeurParSlotContrainte(l_servers, R, S, P) 
    aucunServeurSurSlotOccupeContrainte(l_servers,P)
    tInferieurAuMinSommeRangeesContrainte(l_servers, t, R)
    xInferieurAuMinPoolsContrainte(x ,t)    
    
    #timeout de 5 min
    m.setParam('TimeLimit',5*60)
    m.optimize()
    
    servers_alloc = createServersAlloc(l_servers);   

    displaySolution(servers_alloc, dataCenter, M)
    print("Valeur de la solution :", m.objVal)
 
    
    
    
m = Model("mogplex")
bestAffectation('dc.in')