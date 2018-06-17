# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:59:47 2018

@author: Nicola
"""

import pydotplus as pdp
from tfg import Assistant
from django.db import connection


def cercaFills(dades):
    fill = []
    if dades['tipus'] == 'Batejat':
        consulta = "select eb.nom_llibre, eb.num_registre,data_inscripcio,data_event,eb.nom,eb.cognom1 from event_taula natural join" 
        consulta += " baptisme eb, participant p where p.nom_llibre = eb.nom_llibre and eb.num_registre = p.num_registre and p.tipus_part= "
        if dades['sexe']== 'M': 
            consulta += "\'Pare\' and "
        else:
            consulta += "\'Mare\' and "
        consulta += "p.nom = \'" + dades['nom']+"\' and p.cognom1 = \'"+dades['cognom']+"\' and eb.nom is not null and eb.cognom1 is not null"
        with connection.cursor() as cursor:
            cursor.execute(consulta)
            resultat = cursor.fetchall()
        for a in resultat:
            datafill = a[2]
            if datafill is None or not Assistant.checkData(datafill): datafill = a[3]
            if datafill is not None and Assistant.checkData(datafill):
                if int(datafill[0:4]) >= (int(dades['data'])+18) and int(datafill[0:4]) <= (int(dades['data'])+40):
                    consulta = "select nom, cognom1 from participant where nom_llibre=\'"+a[0]+"\' and num_registre = \'"+str(a[1])+"\' and tipus_part= "
                    if dades['sexe'] == 'M' : consulta += "\'Mare\'"
                    else:   consulta += "\'Pare\'"
                    with connection.cursor() as cursor:
                        cursor.execute(consulta)
                        resultatPM = cursor.fetchall()
                    if len(resultatPM) > 0:
                        nomPM = resultatPM[0][0]; cognomPM = resultatPM[0][1]  
                        fill.append({'nom':a[4],'cognom':a[5],'llibre':a[0],'num':a[1],'nomPM':nomPM,'cognomPM':cognomPM})
        return fill
    else:
        consulta = "select eb.nom_llibre,eb.num_registre,data_event,data_inscripcio,eb.nom, eb.cognom1 from event_taula natural"
        consulta += " join baptisme eb, participant p where p.nom_llibre = eb.nom_llibre and p.num_registre = eb.num_registre "
        consulta += "and ((p.tipus_part=\'Pare\' and p.nom =\'"+dades['nomMarit']+"\' and p.cognom1 LIKE \'%"+dades['cognomMarit'].strip()+"%\') "
        consulta += "or (p.tipus_part = \'Mare\' and p.nom= \'"+dades['nomMuller']+"\' and p.cognom1 LIKE \'%"+dades['cognomMuller'].strip()+"%\')) "
        consulta += " and eb.nom is not null and eb.cognom1 is not null group by eb.nom_llibre,eb.num_registre,data_event,data_inscripcio having count(eb.num_registre) >=2"
        with connection.cursor() as cursor:
            cursor.execute(consulta)
            resultat = cursor.fetchall()
        for a in resultat:
            datafill = a[2]
            if datafill is None or not Assistant.checkData(datafill): datafill = a[3]
            if datafill is not None and Assistant.checkData(datafill):
                if dades['tipus'] == 'Matrimoni' and int(datafill[0:4])>=int(dades['data']) and int(datafill[0:4]) <= (int(dades['data'])+30):
                    fill.append({'nom':a[4].strip(),'cognom':a[5].strip(),'llibre':a[0],'num':a[1]})
                if dades['tipus'] == 'Obituari' and int(datafill[0:4])<=int(dades['data']) and int(datafill[0:4]) >= (int(dades['data'])-50):
                    fill.append({'nom':a[4].strip(),'cognom':a[5].strip(),'llibre':a[0],'num':a[1]})
                if dades['tipus'] == 'GermansBatejat' and int(datafill[0:4]) <= (int(dades['data'])+15) and int(datafill[0:4]) >= (int(dades['data'])-15):
                    fill.append({'nom':a[4].strip(),'cognom':a[5].strip(),'llibre':a[0],'num':a[1]})
                if dades['tipus'] == 'TietsBatejat' and int(datafill[0:4]) <= int(dades['data']) and int(datafill[0:4]) >= (int(dades['data'])-40):
                    fill.append({'nom':a[4].strip(),'cognom':a[5].strip(),'llibre':a[0],'num':a[1]})
                if dades['tipus'] == 'CunyatsMatrimoni' and int(datafill[0:4]) <= (int(dades['data'])-20) and int(datafill[0:4]) >= (int(dades['data'])-60):
                    fill.append({'nom':a[4].strip(),'cognom':a[5].strip(),'llibre':a[0],'num':a[1]})
                if dades['tipus'] == 'GermansDifunt' and int(datafill[0:4]) <= (int(dades['data'])+10) and int(datafill[0:4]) >= (int(dades['data'])-60):
                    fill.append({'nom':a[4].strip(),'cognom':a[5].strip(),'llibre':a[0],'num':a[1]})
        return fill

#%%

def getGraph(protagonista, partable, tipus):
    graph = pdp.Dot(graph_type='graph')
    Avis = pdp.Subgraph();Pares = pdp.Subgraph();Gen = pdp.Subgraph()
    graph.add_subgraph(Avis); graph.add_subgraph(Pares); graph.add_subgraph(Gen)
    if tipus == 'Baptisme':
        nomProta = ''
        cercafillprota = True; cercagermansprota = True; cercatietsP = True; cercatietsM = True
        if protagonista[0]['Nom'] is not None: nomProta += protagonista[0]['Nom'].strip() +" "
        else: nomProta += "- ";cercafillprota = False
        if protagonista[0]['Cognom1'] is not None: nomProta+= protagonista[0]['Cognom1'].strip()
        else: nomProta += "-";cercafillprota = False
        nodeProta = pdp.Node("Prota",label=nomProta,style="filled",fillcolor="#55ffff")
        nodePare = pdp.Node("Pare",label='-');nodeMare = pdp.Node("Mare",label='-'); nodeMatrimoniPares = pdp.Node("MP",label="",shape='diamond',style='filled',height=.1,width=.1)
        nodeAviP = pdp.Node("AviP",label='-');nodeAviaP = pdp.Node("AviaP",label='-'); nodeMatrimoniAvisP = pdp.Node("MAP",label="",shape='diamond',style='filled',height=.1,width=.1)
        nodeAviM = pdp.Node("AviM",label='-');nodeAviaM = pdp.Node("AviaM",label='-'); nodeMatrimoniAvisM = pdp.Node("MAM",label="",shape='diamond',style='filled',height=.1,width=.1)
        Pare = [None,None];Mare = [None,None];AviP = [None,None];AviaP = [None,None];AviM = [None,None];AviaM = [None,None]
        
        for p in partable:
            nom = ''
            if p['Nom'] is not None: nom += p['Nom'].strip() +" "
            else: nom += "- "
            if p['Cognom1'] is not None: nom+= p['Cognom1'].strip()
            else: nom += "-"
            if p['Tip_part'] == 'Pare':   nodePare = pdp.Node("Pare",label=nom);Pare = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Mare':   nodeMare = pdp.Node("Mare",label=nom);Mare = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Avi Patern':   nodeAviP = pdp.Node("AviP",label=nom);AviP = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Avia Paterna':   nodeAviaP = pdp.Node("AviaP",label=nom);AviaP = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Avi Matern':   nodeAviM = pdp.Node("AviM",label=nom);AviM = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Avia Materna':   nodeAviaM = pdp.Node("AviaM",label=nom);AviaM = [p['Nom'],p['Cognom1']]
        
        Avis.add_node(nodeAviP);Avis.add_node(nodeMatrimoniAvisP);Avis.add_node(nodeAviaP)
        Avis.add_node(nodeAviM);Avis.add_node(nodeMatrimoniAvisM);Avis.add_node(nodeAviaM)
        Avis.add_edge(pdp.Edge(nodeAviP,nodeMatrimoniAvisP))
        Avis.add_edge(pdp.Edge(nodeAviaP,nodeMatrimoniAvisP))
        Avis.add_edge(pdp.Edge(nodeAviM,nodeMatrimoniAvisM))
        Avis.add_edge(pdp.Edge(nodeAviaM,nodeMatrimoniAvisM))
        
        
        data = protagonista[0]['Data']
        if data is None or not Assistant.checkData(data):
            data = protagonista[0]['Data_Naix']
            if data is None or not Assistant.checkData(data): 
                cercafillprota = False; cercagermansprota = False; cercatietsP = False; cercatietsM = False
    
        #busquem tiets Paternts del protagonista
        if None in AviP or None in AviaP: cercatietsP = False
        if cercatietsP:
            cerca = {'nomMarit':AviP[0],'cognomMarit':AviP[1],'data':data[0:4],
                     'nomMuller':AviaP[0],'cognomMuller':AviaP[1],'tipus':'TietsBatejat'}
            TietsP = cercaFills(cerca)
            listoftietsP = []
            for t in TietsP:
                if t['nom'] not in listoftietsP and not(Pare[0] is not None and t['nom'] == Pare[0].strip()):
                    listoftietsP.append(t['nom'])
                    nodeTietP = pdp.Node("tietP "+t['nom'],label = t['nom']+" "+t['cognom'])
                    Pares.add_node(nodeTietP)
                    graph.add_edge(pdp.Edge(nodeMatrimoniAvisP,nodeTietP))
                    

        
        Pares.add_node(nodePare);Pares.add_node(nodeMatrimoniPares);Pares.add_node(nodeMare)
        Pares.add_edge(pdp.Edge(nodePare,nodeMatrimoniPares))
        Pares.add_edge(pdp.Edge(nodeMare,nodeMatrimoniPares))
        
        #busquem tiets Materns del protagonista
        if None in AviM or None in AviaM: cercatietsM = False
        if cercatietsM:
            cerca = {'nomMarit':AviM[0],'cognomMarit':AviM[1],'data':data[0:4],
                     'nomMuller':AviaM[0],'cognomMuller':AviaM[1],'tipus':'TietsBatejat'}
            TietsM = cercaFills(cerca)
            listoftietsM = []
            for t in TietsM:
                if t['nom'] not in listoftietsM and not(Mare[0] is not None and t['nom'] == Mare[0].strip()):
                    listoftietsM.append(t['nom'])
                    nodeTietM = pdp.Node("tietM "+t['nom'],label= t['nom']+" "+t['cognom'])
                    Pares.add_node(nodeTietM)
                    graph.add_edge(pdp.Edge(nodeMatrimoniAvisM,nodeTietM))
        
        
        
        graph.add_edge(pdp.Edge(nodeMatrimoniAvisM,nodeMare))
        graph.add_edge(pdp.Edge(nodeMatrimoniAvisP,nodePare))
        graph.add_edge(pdp.Edge(nodeMatrimoniPares,nodeProta))      
        
        # busquem germans del protagonista
        if None in Pare or None in Mare: cercagermansprota = False
        if cercagermansprota:
            cerca = {'nomMarit':Pare[0],'cognomMarit':Pare[1],'data':data[0:4],
                     'nomMuller':Mare[0],'cognomMuller':Mare[1],'tipus':'GermansBatejat'}
            GermansProta = cercaFills(cerca)
            listofgermans = []
            for g in GermansProta:
                if not (protagonista[0]['Nom'] is not None and protagonista[0]['Nom'].strip() == g['nom']) and g['nom'] not in listofgermans:
                    listofgermans.append(g['nom'])
                    nodeGerma = pdp.Node("germa "+g['nom']+g['cognom'],label = g['nom']+" "+g['cognom'])
                    Gen.add_node(nodeGerma)
                    graph.add_edge(pdp.Edge(nodeMatrimoniPares,nodeGerma))
        
        Gen.add_node(nodeProta)
        # fem expansions buscant fills del protagonista
        
        if protagonista[0]['Sexe'] is None or (protagonista[0]['Sexe']!= 'M' and protagonista[0]['Sexe']!= 'F') : cercafillprota = False 
        if cercafillprota:
            cerca = {'nom':protagonista[0]['Nom'],'cognom':protagonista[0]['Cognom1'],'data':data[0:4],
                     'sexe':protagonista[0]['Sexe'],'tipus':'Batejat'}
            fillsProta = cercaFills(cerca)
            ParentCreat = False
            idParents = []
            idMatrimonifills = []
            Fills = pdp.Subgraph()
            for f in fillsProta:
                nomParent = "-"
                cognomParent = "-"
                idPM = ""
                if not ParentCreat:
                    if f['nomPM'] is not None: nomParent = f['nomPM'].strip()
                    if f['cognomPM'] is not None: cognomParent = f['cognomPM'].strip()
                    idPM = nomParent+" "+cognomParent
                    idParents.append([nomParent,cognomParent,idPM])
                    ParentCreat = True
                else:
                    if f['nomPM'] is not None: nomParent = f['nomPM'].strip()
                    if f['cognomPM'] is not None: cognomParent = f['cognomPM'].strip()
                    idTrobat = False
                    for i in idParents:
                        if nomParent == i[0] or cognomParent == i[1]:
                            nomParent = i[0]; cognomParent = i[1]
                            idPM = nomParent+" "+cognomParent
                            idTrobat = True;
                            break
                    if not idTrobat:
                        idPM = nomParent+" "+cognomParent
                        idParents.append([nomParent,cognomParent,idPM])
                noufill = [f['nom'].strip()+" "+f['cognom'].strip(),idPM]
                if noufill not in idMatrimonifills: idMatrimonifills.append(noufill)
            for p in idParents:
                nodeParella = pdp.Node("Parella"+p[2],label=p[2])
                nodeMatrimoniParella = pdp.Node("MP"+p[2],label="",shape='diamond',style='filled',height=.1,width=.1)
                Gen.add_node(nodeParella); Gen.add_node(nodeMatrimoniParella)
                Gen.add_edge(pdp.Edge(nodeParella,nodeMatrimoniParella))
                Gen.add_edge(pdp.Edge(nodeProta,nodeMatrimoniParella))
                for f in idMatrimonifills:
                    if f[1] == p[2]:
                        nodeFill = pdp.Node("fill "+f[0],label = f[0])
                        Fills.add_node(nodeFill)
                        Fills.add_edge(pdp.Edge(nodeMatrimoniParella,nodeFill))
            graph.add_subgraph(Fills)    
            
        
        
        
    elif tipus == 'Matrimoni':
        nomMarit = ''
        cercafills = True; cercaCunyatsMarit= True; cercaCunyatsMuller = True
        if protagonista[0]['Nom_Marit'] is not None: nomMarit += protagonista[0]['Nom_Marit'].strip() +" "
        else: nomMarit += "- ";cercafills = False
        if protagonista[0]['Cognom1_Marit'] is not None: nomMarit+= protagonista[0]['Cognom1_Marit'].strip()
        else: nomMarit += "-";cercafills = False
        nomMuller = ''
        if protagonista[0]['Nom_Muller'] is not None: nomMuller += protagonista[0]['Nom_Muller'].strip() +" "
        else: nomMuller += "- ";cercafills = False
        if protagonista[0]['Cognom1_Muller'] is not None: nomMuller+= protagonista[0]['Cognom1_Muller'].strip()
        else: nomMuller += "-";cercafills = False
        nodeMarit = pdp.Node("Marit",label=nomMarit,style="filled",fillcolor="#55ffff")
        nodeMuller =  pdp.Node("Muller",label=nomMuller,style="filled",fillcolor="#55ffff")
        nodeMatrimoni= pdp.Node("P",label="",shape='diamond',style='filled',height=.1,width=.1)
        nodePareMarit = pdp.Node("PMarit",label='-');nodeMareMarit = pdp.Node("MMarit",label='-');nodeMatrimoniPMarit = pdp.Node("MPMarit",label="",shape='diamond',style='filled',height=.1,width=.1)
        nodePareMuller = pdp.Node("PMuller",label='-');nodeMareMuller = pdp.Node("MMuller",label='-');nodeMatrimoniPMuller = pdp.Node("MPMuller",label="",shape='diamond',style='filled',height=.1,width=.1)
        PareMarit = [None,None];MareMarit = [None,None];PareMuller = [None,None];MareMuller = [None,None]
        
        for p in partable:
            nom = ''
            if p['Nom'] is not None: nom += p['Nom'].strip() +" "
            else: nom += "- "
            if p['Cognom1'] is not None: nom+= p['Cognom1'].strip()
            else: nom += "-"
            if p['Tip_part'] == 'Pare Marit':   nodePareMarit = pdp.Node("PMarit",label=nom); PareMarit = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Mare Marit':   nodeMareMarit = pdp.Node("MMarit",label=nom); MareMarit = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Pare Muller':   nodePareMuller = pdp.Node("PMuller",label=nom); PareMuller = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Mare Muller':   nodeMareMuller = pdp.Node("MMuller",label=nom); MareMuller = [p['Nom'],p['Cognom1']]
        Pares.add_node(nodePareMarit);Pares.add_node(nodeMareMarit);Pares.add_node(nodePareMuller);Pares.add_node(nodeMareMuller);
        Pares.add_node(nodeMatrimoniPMarit);Pares.add_node(nodeMatrimoniPMuller)
        graph.add_edge(pdp.Edge(nodePareMarit,nodeMatrimoniPMarit))
        graph.add_edge(pdp.Edge(nodeMareMarit,nodeMatrimoniPMarit))
        graph.add_edge(pdp.Edge(nodePareMuller,nodeMatrimoniPMuller))
        graph.add_edge(pdp.Edge(nodeMareMuller,nodeMatrimoniPMuller))
        Gen.add_node(nodeMarit);Gen.add_node(nodeMuller);Gen.add_node(nodeMatrimoni)
        graph.add_edge(pdp.Edge(nodeMarit,nodeMatrimoni))
        graph.add_edge(pdp.Edge(nodeMuller,nodeMatrimoni))
        graph.add_edge(pdp.Edge(nodeMatrimoniPMarit,nodeMarit))
        graph.add_edge(pdp.Edge(nodeMatrimoniPMuller,nodeMuller))
        
        #un cop tenim l'arbre bàsic fem expansions buscant fills dels protagonistes
        data = protagonista[0]['Data']
        if data is None or not Assistant.checkData(data):
            data = protagonista[0]['Data_Ins']
            if data is None or not Assistant.checkData(data): cercafills = cercaCunyatsMarit = cercaCunyatsMuller = False
        if cercafills:
            cerca = {'nomMarit':protagonista[0]['Nom_Marit'],'cognomMarit':protagonista[0]['Cognom1_Marit'],'data':data[0:4],
                     'nomMuller':protagonista[0]['Nom_Muller'],'cognomMuller':protagonista[0]['Cognom1_Muller'],'tipus':'Matrimoni'}
            fillsProta = cercaFills(cerca)
            Fills = pdp.Subgraph()
            graph.add_subgraph(Fills)
            listoffills = []
            for f in fillsProta:
                if ("fill "+f['nom']+f['cognom']) not in listoffills:
                    listoffills.append("fill "+f['nom']+f['cognom'])
                    nodeFill = pdp.Node("fill "+f['nom']+f['cognom'],label = f['nom']+" "+f['cognom'])
                    Fills.add_node(nodeFill)
                    graph.add_edge(pdp.Edge(nodeMatrimoni,nodeFill))
                    
        #Procedim a buscar els cunyats
        if None in PareMarit or None in MareMarit: cercaCunyatsMarit = False
        if cercaCunyatsMarit:
            cerca = {'nomMarit':PareMarit[0],'cognomMarit':PareMarit[1],'data':data[0:4],
                     'nomMuller':MareMarit[0],'cognomMuller':MareMarit[1],'tipus':'CunyatsMatrimoni'}
            nodeCunyatsMarit = cercaFills(cerca)
            listofCunyatsMarit = []
            for t in nodeCunyatsMarit:
                if not (protagonista[0]['Nom_Marit'] is not None and protagonista[0]['Nom_Marit'].strip()==t['nom']) and  t['nom'] not in listofCunyatsMarit:
                    listofCunyatsMarit.append(t['nom'])
                    nodeCunyatsMarit = pdp.Node("CunyatMarit "+t['nom'],label= t['nom']+" "+t['cognom'])
                    Gen.add_node(nodeCunyatsMarit)
                    graph.add_edge(pdp.Edge(nodeMatrimoniPMarit,nodeCunyatsMarit))
            
        if None in PareMuller or None in MareMuller: cercaCunyatsMuller = False
        if cercaCunyatsMuller:
            cerca = {'nomMarit':PareMuller[0],'cognomMarit':PareMuller[1],'data':data[0:4],
                     'nomMuller':MareMuller[0],'cognomMuller':MareMuller[1],'tipus':'CunyatsMatrimoni'}
            nodeCunyatsMuller = cercaFills(cerca)
            listofCunyatsMuller = []
            for t in nodeCunyatsMuller:
                if  not (protagonista[0]['Nom_Muller'] is not None and protagonista[0]['Nom_Muller'].strip()==t['nom']) and   t['nom'] not in listofCunyatsMuller:
                    listofCunyatsMuller.append(t['nom'])
                    nodeCunyatsMuller = pdp.Node("CunyatMuller "+t['nom'],label= t['nom']+" "+t['cognom'])
                    Gen.add_node(nodeCunyatsMuller)
                    graph.add_edge(pdp.Edge(nodeMatrimoniPMuller,nodeCunyatsMuller))
        
    elif tipus == 'Obituari':
        nomProta = ''
        cercafills = True; cercaGermans = True
        
        if protagonista[0]['Nom'] is not None: nomProta += protagonista[0]['Nom'].strip() +" "
        else: nomProta += "- ";cercafills = False
        if protagonista[0]['Cognom1'] is not None: nomProta+= protagonista[0]['Cognom1'].strip()
        else: nomProta += "-"; cercafills = False
        nodeProta = pdp.Node("Prota",label=nomProta,style="filled",fillcolor="#55ffff")
        Gen.add_node(nodeProta)
        nodePareD = pdp.Node("PD",label='-');nodeMareD = pdp.Node("MD",label='-');nodeMatrimoniPDifunt=pdp.Node("MPDifunt",label="",shape='diamond',style='filled',height=.1,width=.1)
        teConjugue = False
        nomParella = []; PareD = MareD = [None,None]
        for p in partable:
            nom = ''
            if p['Nom'] is not None: nom += p['Nom'].strip() +" "
            else: nom += "- "
            if p['Cognom1'] is not None: nom+= p['Cognom1'].strip()
            else: nom += "-"
            if p['Tip_part'] == 'Pare Difunt':   nodePareD = pdp.Node("PD",label=nom); PareD = [p['Nom'],p['Cognom1']]
            if p['Tip_part'] == 'Mare Difunt':   nodeMareD = pdp.Node("MD",label=nom); MareD = [p['Nom'],p['Cognom1']]
            
            if p['Tip_part'] == 'Conjugue Difunt':
                teConjugue = True
                nomParella = [p['Nom'],p['Cognom1']]
                nodeConjugueDifunt = pdp.Node("ConjugeDifunt",label=nom)
                nodeMatrimoniDifunt = pdp.Node("MDifunt",label="",shape='diamond',style='filled',height=.1,width=.1)
                Gen.add_node(nodeConjugueDifunt);Gen.add_node(nodeMatrimoniDifunt)
                Gen.add_edge(pdp.Edge(nodeProta,nodeMatrimoniDifunt))
                Gen.add_edge(pdp.Edge(nodeConjugueDifunt,nodeMatrimoniDifunt))
                
        if not teConjugue or None in nomParella: cercafills = False
        
        Pares.add_node(nodePareD);Pares.add_node(nodeMareD);Pares.add_node(nodeMatrimoniPDifunt)
        graph.add_edge(pdp.Edge(nodePareD,nodeMatrimoniPDifunt))
        graph.add_edge(pdp.Edge(nodeMareD,nodeMatrimoniPDifunt))   
        graph.add_edge(pdp.Edge(nodeMatrimoniPDifunt,nodeProta))
        
        # Un cop tenim l arbre original l'expandim amb fills del protagonista
        sexe = protagonista[0]['Sexe']
        if sexe is None or (sexe!= 'M' and sexe!= 'F') : cercafills = False
        data = protagonista[0]['Data']
        if data is None or not Assistant.checkData(data):
            data = protagonista[0]['Data_Ins']
            if data is None or not Assistant.checkData(data): cercafills = False;cercaGermans = False
        if cercafills:
            if sexe == 'M':
                cerca = {'nomMarit':protagonista[0]['Nom'],'cognomMarit':protagonista[0]['Cognom1'],'data':data[0:4],
                         'nomMuller':nomParella[0],'cognomMuller':nomParella[1],'tipus':'Obituari'}
            else: cerca = {'nomMarit':nomParella[0],'cognomMarit':nomParella[1],'data':data[0:4],
                         'nomMuller':protagonista[0]['Nom'],'cognomMuller':protagonista[0]['Cognom1'],'tipus':'Obituari'}
            fillsProta = cercaFills(cerca)
            fillsProta = cercaFills(cerca)
            Fills = pdp.Subgraph()
            graph.add_subgraph(Fills)
            listoffills = []
            for f in fillsProta:
                if ("fill "+f['nom']+f['cognom']) not in listoffills:
                    listoffills.append("fill "+f['nom']+f['cognom'])
                    nodeFill = pdp.Node("fill "+f['nom']+f['cognom'],label = f['nom']+" "+f['cognom'])
                    Fills.add_node(nodeFill)
                    graph.add_edge(pdp.Edge(nodeMatrimoniDifunt,nodeFill))
        if None in PareD or None in MareD: cercaGermans = False
        if cercaGermans:
            cerca = {'nomMarit':PareD[0],'cognomMarit':PareD[1],'data':data[0:4],
                     'nomMuller':MareD[0],'cognomMuller':MareD[1],'tipus':'GermansDifunt'}
            GermansProta = cercaFills(cerca)
            listofgermans = []
            for g in GermansProta:
                if not (protagonista[0]['Nom'] is not None and protagonista[0]['Nom'].strip() == g['nom']) and g['nom'] not in listofgermans:
                    listofgermans.append(g['nom'])
                    nodeGerma = pdp.Node("germa "+g['nom']+g['cognom'],label = g['nom']+" "+g['cognom'])
                    Gen.add_node(nodeGerma)
                    graph.add_edge(pdp.Edge(nodeMatrimoniPDifunt,nodeGerma))    
        
    graph.write_png("tfg/static/images/arbre.png")
    
    return True
