# -*- coding: utf-8 -*-

from django.db import connection

def checkData(string):
    if len(string) < 4:
        return False
    else:
        for a in string[0:4]:
            if not a.isdigit():
                return False
        return True
    
def checkDataForm(string):
    for a in string:
        if not a.isdigit():
            return False
    return True

def AddDataParameters(fdict,consulta):
    newform = {}
    if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '') or ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != ''):
        auxEvent = " (substring(data_event,1,4) ~  \'^[0-9\.]+$\' "
        auxInscripcio = " (substring(data_inscripcio,1,4) ~  \'^[0-9\.]+$\' "
        auxEnterrament = " (substring(data_enterrament,1,4) ~  \'^[0-9\.]+$\' "
        if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '' and checkDataForm(fdict['dataini'])):
            auxEvent += " and cast(substring(data_event,1,4) AS int) >= "+fdict['dataini']
            auxInscripcio += " and cast(substring(data_inscripcio,1,4) AS int) >= "+fdict['dataini']
            auxEnterrament += " and cast(substring(data_enterrament,1,4) AS int) >= "+fdict['dataini']
            newform['dataini'] = fdict['dataini']
        else:
            newform['dataini'] = '-'
        if ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != '' and checkDataForm(fdict['datafi'])):
            auxEvent += " and cast(substring(data_event,1,4) AS int) <= "+fdict['datafi']
            auxInscripcio += " and cast(substring(data_inscripcio,1,4) AS int) <= "+fdict['datafi']
            auxEnterrament += " and cast(substring(data_enterrament,1,4) AS int) <= "+fdict['datafi']
            newform['datafi'] = fdict['datafi']
        else:
            newform['datafi'] = '-'
        auxEvent += ')';auxInscripcio += ')';auxEnterrament += ')'
        consulta += auxEvent + " or " + auxInscripcio + " or " + auxEnterrament
    else:
        newform['dataini'] = '-'; newform['datafi'] = '-'
    
    return consulta,newform
    

def AddParameters(fdict,consulta):
    newform = {}
    if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '') or ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != ''):
        consulta += " substring(data_event,1,4) ~  \'^[0-9\.]+$\' and"
        if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '' and checkDataForm(fdict['dataini'])):
            aux = " cast(substring(data_event,1,4) AS int) >= "+fdict['dataini']+" and"
            consulta += aux
            newform['dataini'] = fdict['dataini']
        else:
            newform['dataini'] = '-'
        if ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != '' and checkDataForm(fdict['datafi'])):
            aux = " cast(substring(data_event,1,4) AS int) <= "+fdict['datafi']+" and"
            consulta += aux
            newform['datafi'] = fdict['datafi']
        else:
            newform['datafi'] = '-'
    else:
        newform['dataini'] = '-'; newform['datafi'] = '-'
    if 'nom' in fdict and fdict['nom'] != '-' and fdict['nom'] != '':     # Anem afegint parametres al where
        consulta += " nom LIKE \'%" +fdict['nom']+"%\' and"    
        newform['nom']=fdict['nom']
    else: newform['nom']= '-'
    if 'cognom1' in fdict and fdict['cognom1'] != '-' and fdict['cognom1'] != '': 
        consulta += " cognom1 LIKE \'%" + fdict['cognom1']+"%\' and"
        newform['cognom1']=fdict['cognom1']
    else: newform['cognom1'] = '-'
    if 'cognom2' in fdict and fdict['cognom2'] != '-' and fdict['cognom2'] != '':
        consulta += " cognom2 LIKE \'%" + fdict['cognom2']+"%\'"
        newform['cognom2']=fdict['cognom2']
    else: newform['cognom2'] = '-'
    if consulta[len(consulta)-3:len(consulta)] == 'and': consulta = consulta[:len(consulta)-3]
    
    return consulta,newform

def AddParameters2(fdict,consulta):
    newform = {}
    if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '') or ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != ''):
        consulta += " substring(data_event,1,4) ~  \'^[0-9\.]+$\' and"
        if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '' and checkDataForm(fdict['dataini'])):
            aux = " cast(substring(data_event,1,4) AS int) >= "+fdict['dataini']+" and"
            consulta += aux
            newform['dataini'] = fdict['dataini']
        else:
            newform['dataini'] = '-'
        if ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != '' and checkDataForm(fdict['datafi'])):
            aux = " cast(substring(data_event,1,4) AS int) <= "+fdict['datafi']+" and"
            consulta += aux
            newform['datafi'] = fdict['datafi']
        else:
            newform['datafi'] = '-'
    else:
        newform['dataini'] = '-'; newform['datafi'] = '-'
    if 'nom' in fdict and fdict['nom'] != '-' and fdict['nom'] != '':     # Anem afegint parametres al where
        consulta += " p.nom LIKE \'%" +fdict['nom']+"%\' and"    
        newform['nom']=fdict['nom']
    else: newform['nom']= '-'
    if 'cognom1' in fdict and fdict['cognom1'] != '-' and fdict['cognom1'] != '': 
        consulta += " p.cognom1 LIKE \'%" + fdict['cognom1']+"%\' and"
        newform['cognom1']=fdict['cognom1']
    else: newform['cognom1'] = '-'
    if 'cognom2' in fdict and fdict['cognom2'] != '-' and fdict['cognom2'] != '':
        consulta += " p.cognom2 LIKE \'%" + fdict['cognom2']+"%\'"
        newform['cognom2']=fdict['cognom2']
    else: newform['cognom2'] = '-'
    if consulta[len(consulta)-3:len(consulta)] == 'and': consulta = consulta[:len(consulta)-3]
    
    return consulta,newform

def AddParametersMatrimoni(fdict,consulta):
    newform = {}
    if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '') or ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != ''):
        consulta += " substring(data_event,1,4) ~  \'^[0-9\.]+$\' and"
        if ('dataini' in fdict and fdict['dataini'] != '-' and fdict['dataini'] != '' and checkDataForm(fdict['dataini'])):
            aux = " cast(substring(data_event,1,4) AS int) >= "+fdict['dataini']+" and"
            consulta += aux
            newform['dataini'] = fdict['dataini']
        else:
            newform['dataini'] = '-'
        if ('datafi' in fdict and fdict['datafi'] != '-' and fdict['datafi'] != '' and checkDataForm(fdict['datafi'])):
            aux = " cast(substring(data_event,1,4) AS int) <= "+fdict['datafi']+" and"
            consulta += aux
            newform['datafi'] = fdict['datafi']
        else:
            newform['datafi'] = '-'
    else:
        newform['dataini'] = '-'; newform['datafi'] = '-'
    consultaMMuller = " or "
    if 'nom' in fdict and fdict['nom'] != '-' and fdict['nom'] != '':     # Anem afegint parametres al where
        consulta += " nom_marit LIKE \'%" +fdict['nom']+"%\' and"
        consultaMMuller += " nom_muller LIKE \'%" +fdict['nom']+"%\' and"    
        newform['nom']=fdict['nom']
    else: newform['nom']= '-'
    if 'cognom1' in fdict and fdict['cognom1'] != '-' and fdict['cognom1'] != '': 
        consulta += " cognom1_marit LIKE \'%" +fdict['cognom1']+"%\' and"
        consultaMMuller += " cognom1_muller LIKE \'%" +fdict['cognom1']+"%\' and"
        newform['cognom1']=fdict['cognom1']
    else: newform['cognom1'] = '-'
    if 'cognom2' in fdict and fdict['cognom2'] != '-' and fdict['cognom2'] != '':
        consulta += " cognom2_marit LIKE \'%" +fdict['cognom2']+"%\'"
        consultaMMuller += " cognom2_muller LIKE \'%" +fdict['cognom2']+"%\'"
        newform['cognom2']=fdict['cognom2']
    else: newform['cognom2'] = '-'
    if consulta[len(consulta)-3:len(consulta)] == 'and': consulta = consulta[:len(consulta)-3]
    if consultaMMuller[len(consultaMMuller)-3:len(consultaMMuller)] == 'and': consultaMMuller = consultaMMuller[:len(consultaMMuller)-3]
    if 'nom' in consulta: consulta += consultaMMuller
    
    return consulta,newform

def getTable(consulta,tipus):
    table = []
    if tipus=='Baptisme':
        with connection.cursor() as cursor:
            cursor.execute(consulta)
            resultat = cursor.fetchall()
        for a in resultat:
            table.append({'Arxiu':a[0],'Num_Reg':a[1],'Data':a[11],'Lloc':a[12],'Nom':a[2],
                             'NomsComp':a[3],'Cognom1':a[4],'Cognom2':a[5],
                             'Sexe':a[6],'Data_Naix':a[7],'Lloc_Naix':a[8],
                             'Obs':a[9],'ObsG':a[14]})
    if tipus == 'Matrimoni':
        with connection.cursor() as cursor:
            cursor.execute(consulta)
            resultat = cursor.fetchall()
        for a in resultat:
            table.append({'Arxiu':a[0],'Num_Reg':a[1],'Data_Ins':a[20],'Data':a[21],'Lloc':a[22],'Nom_Marit':a[2],
                             'Cognom1_Marit':a[3],'Cognom2_Marit':a[4],'Edat_Marit':a[5],
                             'Lloc_Naix_Marit':a[6],'Est_Marit':a[7],'Residencia_Marit':a[8],'Ocupacio_Marit':[9],
                             'Nom_Muller':a[10],'Cognom1_Muller':a[11],'Cognom2_Muller':a[12],'Alies_Muller':a[13],
                             'Lloc_Naix_Muller':a[14],'Residencia_Muller':a[15],'Edat_Muller':a[16],'Est_Muller':a[17],
                             'Esglesia':a[18],'Cap_Mat':a[19],'Obs':a[24]})
    if tipus == 'Obituari':
        with connection.cursor() as cursor:
            cursor.execute(consulta)
            resultat = cursor.fetchall()
        for a in resultat:
            table.append({'Arxiu':a[0],'Num_Reg':a[1],'Data_Ins':a[18],'Data':a[19],'Lloc':a[20],'Nom':a[2],
                             'Cognom1':a[3],'Cognom2':a[4],'Alies':a[5],'Sexe':a[6],'Data_Naix':a[7],'Lloc_Naix':a[8],
                             'Edat':a[9],'Estat_civil':a[10],'Residencia':a[11],'Ocupacio':a[12],'Data_Ente':a[13],'Lloc_Ente':a[14],'Cementiri':a[15],
                             'noms_fills':a[16],'ObsP':a[17],'ObsG':a[22]})
    if tipus == 'Participant':
        with connection.cursor() as cursor:
            cursor.execute(consulta)
            resultat = cursor.fetchall()
        for a in resultat:
            table.append({'Arxiu':a[0],'Num_Reg':a[1],'Tip_Event':a[2],
                             'Data_Event':a[13],'Tip_part':a[3],'Nom':a[4],
                             'Cognom1':a[5],'Cognom2':a[6],'Estat_vital':a[7],
                             'Ofici':a[8],'Lloc_Naix':a[9],'Resid':a[10]})
    return table

#%%
def getMatrimoniVida(Nom,Cognom1,Cognom2,Data_Naix,Data,tableM):
    ConjuntMatrimoni = None
    for m in tableM:
        puntuacio = 0
        Rol = 'Muller'
        if Nom is None:
            puntuacio += 0.5
        elif m['Nom_Marit'] is not None and m['Nom_Marit']==Nom:
            puntuacio += 2; Rol = 'Marit'
        if Cognom1 is None:
            puntuacio += 0.5
        elif m['Cognom1_Marit'] is not None and m['Cognom1_Marit'] == Cognom1:
            puntuacio += 2; Rol = 'Marit'
        if Cognom2 is None:
            puntuacio += 0.5
        elif m['Cognom2_Marit'] is not None and m['Cognom2_Marit'] == Cognom2:
            puntuacio += 2; Rol = 'Marit'
        if Rol == 'Muller':
            if Nom is None:
                puntuacio += 0.5
            elif m['Nom_Muller'] is not None and m['Nom_Muller']==Nom:
                puntuacio += 2
            if Cognom1 is None:
                puntuacio += 0.5
            elif m['Cognom1_Muller'] is not None and m['Cognom1_Muller'] == Cognom1:
                puntuacio += 2
            if Cognom2 is None:
                puntuacio += 0.5
            elif m['Cognom2_Muller'] is not None and m['Cognom2_Muller'] == Cognom2:
                puntuacio += 2
        if Data_Naix is not None and checkData(Data_Naix) and m['Data'] is not None:
            dif = int(m['Data'][0:4]) - int(Data_Naix[0:4])
            if dif < 15 or dif > 70 :
                puntuacio = 0
        else:
            puntuacio -=0.25
        if Data is not None and m['Data'] is not None:
            dif = int(m['Data'][0:4]) - int(Data[0:4])
            if dif < 15 or dif > 70 :
                puntuacio = 0
        else:
            puntuacio -=0.25
        
        if puntuacio >= 4.5:
            matrimoni = "Es va casar amb "
            if Rol == 'Marit': Rol2 = 'Muller'
            else: Rol2 = 'Marit'
            if m['Nom_'+Rol2] is not None : matrimoni+=m['Nom_'+Rol2]+ " "
            else: matrimoni += "- "
            if m['Cognom1_'+Rol2] is not None : matrimoni+=m['Cognom1_'+Rol2]+ " "
            else: matrimoni += "- " 
            if m['Cognom2_'+Rol2] is not None : matrimoni+=m['Cognom2_'+Rol2]+ " "
            else: matrimoni += "- " 
            if m['Data'] is not None: matrimoni += "el dia "+m['Data']
            else: matrimoni += "el dia -"
            ConjuntMatrimoni = [matrimoni,m['Arxiu'].strip(),m['Num_Reg']]
    
    return ConjuntMatrimoni

def getObituariVida(Nom,Cognom1,Cognom2,Data_Naix,Data,Lloc_Naix,tableO):
    ConjuntObituari = None
    for o in tableO:
        puntuacio = 0
        if Nom is None:
            puntuacio += 0.5
        elif o['Nom'] is not None and o['Nom']==Nom:
            puntuacio += 2
        if Cognom1 is None:
            puntuacio += 0.5
        elif o['Cognom1'] is not None and o['Cognom1'] == Cognom1:
            puntuacio += 2
        if Cognom2 is None:
            puntuacio += 0.5
        elif o['Cognom2'] is not None and o['Cognom2'] == Cognom2:
            puntuacio += 2
        if Data_Naix is None:
            puntuacio += 0.25
        elif o['Data_Naix'] is not None and checkData(Data_Naix) and o['Data_Naix'] is not None and checkData(o['Data_Naix']):
            if o['Data_Naix'][0:4]== Data_Naix[0:4]: puntuacio += 1
            else: puntuacio += -1.5
        if Lloc_Naix is None:
            puntuacio += 0.25
        elif o['Lloc_Naix'] is not None and o['Lloc_Naix'] == Lloc_Naix:
            puntuacio += 0.5
            
        if Data is not None and o['Data'] is not None:
            dif = int(o['Data'][0:4]) - int(Data[0:4])
            if dif < 0 or dif > 90 :
                puntuacio = 0
        else:
            puntuacio -= 0.5
        if Data is not None and o['Data_Ins'] is not None  and checkData(o['Data_Ins']) :
            dif = int(o['Data_Ins'][0:4]) - int(Data[0:4])
            if dif < 0 or dif > 90 :
                puntuacio = 0
        else:
            puntuacio -= 0.5    
            
        if puntuacio >= 4.5:
            obituari = "Va morir el dia "
            if o['Data'] is not None: obituari+= o['Data']+" "
            elif o['Data_Ins'] is not None: obituari+= o['Data_Ins']+" "
            else: obituari += "- "
            if o['Edat'] is not None: obituari+= "a l'edat de "+o['Edat']+" "
            else: obituari += "a l'edat de - "
            if o['Residencia'] is not None: obituari+= "a "+o['Residencia']+", "
            if o['Estat_civil'] is not None: obituari+= o['Estat_civil']+", "
            if o['Ocupacio'] is not None: obituari+= "després de treballar com a "+o['Ocupacio']+", "
            if o['Lloc_Ente'] is not None: obituari+= "per ser enterrat a "+o['Lloc_Ente']
            elif o['Cementiri'] is not None: obituari+= "per ser enterrat a "+o['Cementiri']
            obituari += "."
            ConjuntObituari = [obituari,o['Arxiu'].strip(),o['Num_Reg']]
    return ConjuntObituari

def getParticipacionsVida(Nom,Cognom1,Cognom2,Data_Naix,Data,tableP):
    participacions = []
    for p in tableP:
        puntuacio = 0
        if Nom is None:
            puntuacio += 0.5
        elif p['Nom'] is not None and p['Nom']==Nom:
            puntuacio += 2
        if Cognom1 is None:
            puntuacio += 0.5
        elif p['Cognom1'] is not None and p['Cognom1'] == Cognom1:
            puntuacio += 2
        if Cognom2 is None:
            puntuacio += 0.5
        elif p['Cognom2'] is not None and p['Cognom2'] == Cognom2:
            puntuacio += 2
        
        if Data_Naix is not None and checkData(Data_Naix) and p['Data_Event'] is not None and checkData(p['Data_Event']):
            dif = int(p['Data_Event'][0:4]) - int(Data_Naix[0:4])
            if dif < 12 or dif > 65 :
                puntuacio = 0
        else:
            puntuacio -= 0.25
        if Data is not None and p['Data_Event'] is not None  and checkData(p['Data_Event']):
            dif = int(p['Data_Event'][0:4]) - int(Data[0:4])
            if dif < 12 or dif > 65:
                puntuacio = 0
        else:
            puntuacio -=0.25
            
        if puntuacio >= 4.5:
            part = "Va participar a un "+p['Tip_Event']+" com a "+p['Tip_part']+" a data "
            if p['Data_Event'] is not None: part += p['Data_Event']+"."
            else: part += "-."
            ConjuntPart = [part,p['Arxiu'].strip(),p['Num_Reg']]
            participacions.append(ConjuntPart)
        
    return participacions

def getVides(tableB,tableM,tableO,tableP):
    Entrades= []
    for b in tableB:
        Nom =""
        if b['Nom'] is not None: Nom+=b['Nom']
        else: Nom+= "-"
        if b['Cognom1'] is not None: Nom+= " "+b['Cognom1']
        else: Nom += " -"
        if b['Cognom2'] is not None: Nom+= " "+b['Cognom2']
        else: Nom += " -"
        persona = {'Nom':Nom}
        llista = []
        naixement = "Va nèixer el dia "
        if b['Data_Naix'] is not None: naixement+=b['Data_Naix']
        else: naixement+="-"
        if b['Lloc_Naix'] is not None: naixement+=" a " + b['Lloc_Naix']
        else: naixement+=" a -"
        ConjuntNaixement = [naixement,b['Arxiu'].strip(),b['Num_Reg']]
        llista.append(ConjuntNaixement)
        batejat = "Va ser batejat/ada el dia "
        if b['Data'] is not None: batejat+=b['Data']
        else: batejat+="-"
        if b['Lloc'] is not None: batejat+=" a " + b['Lloc']
        else: batejat+=" a -"
        ConjuntBatejat = [batejat,b['Arxiu'].strip(),b['Num_Reg']]
        llista.append(ConjuntBatejat)
        
        Matrimoni = getMatrimoniVida(b['Nom'],b['Cognom1'],b['Cognom2'],b['Data_Naix'],b['Data'],tableM)
        if Matrimoni is not None: llista.append(Matrimoni)
        
        Participacions = getParticipacionsVida(b['Nom'],b['Cognom1'],b['Cognom2'],b['Data_Naix'],b['Data'],tableP)
        for p in Participacions:
            llista.append(p)
        
        Obituari = getObituariVida(b['Nom'],b['Cognom1'],b['Cognom2'],b['Data_Naix'],b['Data'],b['Lloc_Naix'],tableO)
        if Obituari is not None: llista.append(Obituari)
        
        persona['llista'] = llista
        Entrades.append(persona)
        
    return Entrades
        
    
    
    
    
    
    
    