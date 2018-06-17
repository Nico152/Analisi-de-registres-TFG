# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404,render,get_list_or_404
from django.template import loader
from django.http import HttpResponse
from django.db import connection

from tfg.tables import ArxiuTable,BatejatTable,ParticipantTable,MatrimoniTable,ObituariTable
from tfg.forms import DataOnlyForm,NomDataForm
from tfg import Assistant
from django_tables2 import RequestConfig

import tfg.Arbre as arbre

# Create your views here.

bform = {}
mform = {}
oform = {}
pform = {}
protaform = {}
apadrinatsform = {}
vidaform = {}
fillscasatsform = {}


#%%
def main(request):
    arxiutable = [] 
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from arxiu")
        arxius = cursor.fetchall()
    for a in arxius:
        arxiutable.append({'Arxiu':a[0],'Nom_Parroquia':a[1],
                           'Persona_B':a[2],'Persona_R':a[3]})
    table = ArxiuTable(arxiutable)
    RequestConfig(request).configure(table)
    table.paginate(page = request.GET.get('page',1),per_page=25)
    context = {'arxiu': table}
    return render(request,'tfg/base.html',context)
#    return HttpResponse('Hello')
#%%
def Baptismes(request):
    global bform
    url = request.build_absolute_uri()
    if request.method == 'POST' or 'cerca-batejat' in url:
        if request.method == 'POST': bform = NomDataForm(request.POST)
        bform.is_valid()
        fdict = bform.cleaned_data
        consulta = "SELECT * from baptisme natural join event_taula"   #Comencem a crear la consulta
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consulta += " WHERE"
                break        
        consulta,newform = Assistant.AddParameters(fdict,consulta)
        baptable = Assistant.getTable(consulta,'Baptisme')
        table = BatejatTable(baptable)
        RequestConfig(request).configure(table)
        table.paginate(page = request.GET.get('page',1),per_page=50)
        bform = NomDataForm(newform)
        context = {'baptismes': table,'form': bform}
        return render(request,'tfg/base_baptismes.html',context)
        
    else:
        arxiutable = [] 
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from arxiu where nom_llibre LIKE 'B%'")
            arxius = cursor.fetchall()
        for a in arxius:
            arxiutable.append({'Arxiu':a[0],'Nom_Parroquia':a[1],
                               'Persona_B':a[2],'Persona_R':a[3]})
        table = ArxiuTable(arxiutable)
        RequestConfig(request).configure(table)
        table.paginate(page = request.GET.get('page',1),per_page=25)
        
        bform = NomDataForm()
        context = {'baptismes': table,
                   'form': bform}
    return render(request,'tfg/base_baptismes.html',context)


#%%
def Matrimonis(request):
    global mform
    url = request.build_absolute_uri()
    if request.method == 'POST' or 'cerca-matrimonis' in url:
        if request.method == 'POST': mform = NomDataForm(request.POST)
        mform.is_valid()
        fdict = mform.cleaned_data
        consulta = "SELECT * from matrimoni natural join event_taula"   #Comencem a crear la consulta
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consulta += " WHERE"
                break
        consulta,newform = Assistant.AddParametersMatrimoni(fdict,consulta)
        Mtable = Assistant.getTable(consulta,'Matrimoni')
        tableM = MatrimoniTable(Mtable)
        RequestConfig(request).configure(tableM)
        tableM.paginate(page = request.GET.get('page',1),per_page=20)
        mform = NomDataForm(newform)
        context = {'matrimonis': tableM,'form': mform}
        return render(request,'tfg/base_matrimonis.html',context)

    else:
        arxiutable = [] 
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from arxiu where nom_llibre LIKE 'M%'")
            arxius = cursor.fetchall()
        for a in arxius:
            arxiutable.append({'Arxiu':a[0],'Nom_Parroquia':a[1],
                               'Persona_B':a[2],'Persona_R':a[3]})
        table = ArxiuTable(arxiutable)
        RequestConfig(request).configure(table)
        table.paginate(page = request.GET.get('page',1),per_page=25)
        
        mform = NomDataForm()
        context = {'matrimonis': table,
                   'form': mform}
    return render(request,'tfg/base_matrimonis.html',context)


#%%
def Obituaris(request):
    global oform
    url = request.build_absolute_uri()
    if request.method == 'POST' or 'cerca-obituaris' in url:
        if request.method == 'POST': oform = NomDataForm(request.POST)
        oform.is_valid()
        fdict = oform.cleaned_data
        consulta = "SELECT * from obituari natural join event_taula"   #Comencem a crear la consulta
        Buit = True
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consulta += " WHERE"
                Buit = False
                break            
        consulta,newform = Assistant.AddParameters(fdict,consulta)
        if not Buit:
            Otable = Assistant.getTable(consulta,'Obituari')
        else:
            Otable = []
        tableO = ObituariTable(Otable)
        RequestConfig(request).configure(tableO)
        tableO.paginate(page = request.GET.get('page',1),per_page=20)
        oform = NomDataForm(newform)
        context = {'obituaris': tableO,'form': oform}
        return render(request,'tfg/base_obituaris.html',context)
        

    else:
        arxiutable = [] 
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from arxiu where nom_llibre LIKE 'O%'")
            arxius = cursor.fetchall()
        for a in arxius:
            arxiutable.append({'Arxiu':a[0],'Nom_Parroquia':a[1],
                               'Persona_B':a[2],'Persona_R':a[3]})
        table = ArxiuTable(arxiutable)
        RequestConfig(request).configure(table)
        table.paginate(page = request.GET.get('page',1),per_page=25)
        
        oform = NomDataForm()
        context = {'obituaris': table,
                   'form': oform}
    return render(request,'tfg/base_obituaris.html',context)




#%%
def ParticipantEvent(request):
    global pform
    if request.method == 'POST' or bool(pform):
        if request.method == 'POST': pform = NomDataForm(request.POST)
        pform.is_valid()
        fdict = {}
        try:
            fdict = pform.cleaned_data
        except:    
            print('Error al cleaned data Participant')
        consulta = "SELECT * from participant natural join event_taula"
        Buit = True
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consulta += " WHERE"
                Buit = False
                break
        consulta,newform = Assistant.AddParameters(fdict,consulta)
        if not Buit:
            partable = Assistant.getTable(consulta,'Participant')
        else:
            partable = []
        table = ParticipantTable(partable)
        RequestConfig(request).configure(table)
        table.paginate(page = request.GET.get('page',1),per_page=50)
        pform = NomDataForm(newform)
        context = {'participant':table,'form':pform}
        render(request,'tfg/general_participant.html',context)
    else:
        pform = NomDataForm()
        table = ParticipantTable([])
        context = {'participant':table,'form':pform}
    return render(request,'tfg/general_participant.html',context)
    
#%%  
def ProtagonistaEvent(request):
    global protaform
    if request.method == 'POST' or bool(protaform):
        if request.method == 'POST': protaform = NomDataForm(request.POST)
        protaform.is_valid()
        fdict = {}
        try:
            fdict = protaform.cleaned_data
        except:    
            print('Error al cleaned data Protagonista')
        consultaB = "SELECT * from baptisme natural join event_taula"   #Comencem a crear la consulta
        consultaM = "SELECT * from matrimoni natural join event_taula"
        consultaO = "SELECT * from obituari natural join event_taula"
        Buit = True
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consultaB += " WHERE";consultaM += " WHERE";consultaO += " WHERE"
                Buit = False
                break
        consultaB,_= Assistant.AddParameters(fdict,consultaB)
        consultaO,_= Assistant.AddParameters(fdict,consultaO)
        consultaM, newform = Assistant.AddParametersMatrimoni(fdict,consultaM)
        
        Btable = []
        if not Buit: Btable = Assistant.getTable(consultaB,'Baptisme')
        tableB = BatejatTable(Btable)
        RequestConfig(request).configure(tableB)
        tableB.paginate(page = request.GET.get('page',1),per_page=10)
        
        Mtable = []
        if not Buit: Mtable = Assistant.getTable(consultaM,'Matrimoni')
        tableM = MatrimoniTable(Mtable)
        RequestConfig(request).configure(tableM)
        tableM.paginate(page = request.GET.get('page',1),per_page=10)
        
        Otable = []
        if not Buit: Otable = Assistant.getTable(consultaO,'Obituari')
        tableO = ObituariTable(Otable)
        RequestConfig(request).configure(tableO)
        tableO.paginate(page = request.GET.get('page',1),per_page=10)
        
        protaform = NomDataForm(newform)
        context = {'baptismes': tableB, 'matrimoni':tableM,'obituari':tableO,'form':protaform}
        render(request,'tfg/general_protagonista.html',context)
        
    else:
        protaform = NomDataForm()
        tableB = BatejatTable([])
        tableM = MatrimoniTable([])
        tableO = ObituariTable([])
        context = {'baptismes': tableB, 'matrimoni':tableM,'obituari':tableO,'form':protaform}
    return render(request,'tfg/general_protagonista.html',context)
    
#%%
def Apadrinats(request):
    global apadrinatsform
    if request.method == 'POST' or bool(apadrinatsform):
        if request.method == 'POST': apadrinatsform = NomDataForm(request.POST)
        apadrinatsform.is_valid()
        fdict = {}
        try:
            fdict = apadrinatsform.cleaned_data
        except:    
            print('Error al cleaned data Apadrinats')
        consulta = ""
        Buit = True
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consulta = "select * from baptisme  natural join event_taula b, participant p where b.nom_llibre = p.nom_llibre and b.num_registre = p.num_registre and (p.tipus_part= 'Padri' or p.tipus_part = 'Padrina') and "
                Buit = False
                break
        consulta,newform = Assistant.AddParameters2(fdict,consulta)
        with connection.cursor() as cursor:   #Consulta 
            if not Buit:
                cursor.execute(consulta)
                resultat = cursor.fetchall()
            else:
                resultat = []
        partable = []
        baptable = []
        for a in resultat:
            partable.append({'Arxiu':a[15],'Num_Reg':a[16],'Tip_Event':a[17],
                             'Data_Event':a[11],'Tip_part':a[18],'Nom':a[19],
                             'Cognom1':a[20],'Cognom2':a[21],'Estat_vital':a[22],
                             'Ofici':a[23],'Lloc_Naix':a[24],'Resid':a[25]})
            baptable.append({'Arxiu':a[0],'Num_Reg':a[1],'Data':a[11],'Lloc':a[12],'Nom':a[2],
                             'NomsComp':a[3],'Cognom1':a[4],'Cognom2':a[5],
                             'Sexe':a[6],'Data_Naix':a[7],'Lloc_Naix':a[8],
                             'Obs':a[9],'ObsG':a[14]})
        tableB = BatejatTable(baptable)
        RequestConfig(request).configure(tableB)
        tableB.paginate(page = request.GET.get('page',1),per_page=10)
        tableP = ParticipantTable(partable)
        RequestConfig(request).configure(tableP)
        tableP.paginate(page = request.GET.get('page',1),per_page=10)
        apadrinatsform = NomDataForm(newform)
        context = {'baptismes':tableB,'participacions':tableP,'form':apadrinatsform}
        return render(request,'tfg/baptismes_apadrinats.html',context)
    else:
        apadrinatsform = NomDataForm()
        tableB = BatejatTable([])
        tableP = ParticipantTable([])
        context = {'baptismes':tableB,'participacions':tableP,'form':apadrinatsform}
    return render(request,'tfg/baptismes_apadrinats.html',context)
#%%

def detail(request,nom_llibre,num_registre):
    nom_llibre = nom_llibre.replace('*','/')
    consulta = 'select * from event_taula where nom_llibre = \''+nom_llibre+'\' and num_registre = '+str(num_registre)
    with connection.cursor() as cursor:   #Consulta BBDD
            cursor.execute(consulta)
            resultat = cursor.fetchone()
    event = {'Arxiu':resultat[0],'Num_Reg':resultat[1],'DataIns':resultat[2],
             'Data_Event':resultat[3], 'Lloc_Event':resultat[4], 'tipus_event':resultat[5],
             'ObsGen':resultat[6]}
    consulta =  'select * from '+event['tipus_event']+ ' where nom_llibre = \''+nom_llibre+'\' and num_registre = '+str(num_registre)
    with connection.cursor() as cursor:   #Consulta BBDD
            cursor.execute(consulta)
            resultat = cursor.fetchone()
    protagonista = []
    if event['tipus_event'] == 'Baptisme':
        protagonista.append({'Arxiu':resultat[0],'Num_Reg':num_registre,'Data':event['Data_Event'],'Lloc':event['Lloc_Event'],'Nom':resultat[2],
                             'NomsComp':resultat[3],'Cognom1':resultat[4],'Cognom2':resultat[5],
                             'Sexe':resultat[6],'Data_Naix':resultat[7],'Lloc_Naix':resultat[8],
                             'Obs':resultat[9],'ObsG':event['ObsGen']})
        table = BatejatTable(protagonista)
    if event['tipus_event'] == 'Matrimoni':
        protagonista.append({'Arxiu':resultat[0],'Num_Reg':num_registre,'Data_Ins':event['DataIns'],'Data':event['Data_Event'],'Lloc':event['Lloc_Event'],'Nom_Marit':resultat[2],
                             'Cognom1_Marit':resultat[3],'Cognom2_Marit':resultat[4],'Edat_Marit':resultat[5],
                             'Lloc_Naix_Marit':resultat[6],'Est_Marit':resultat[7],'Residencia_Marit':resultat[8],'Ocupacio_Marit':resultat[9],
                             'Nom_Muller':resultat[10],'Cognom1_Muller':resultat[11],'Cognom2_Muller':resultat[12],'Alies_Muller':resultat[13],
                             'Lloc_Naix_Muller':resultat[14],'Residencia_Muller':resultat[15],'Edat_Muller':resultat[16],'Est_Muller':resultat[17],
                             'Esglesia':resultat[18],'Cap_Mat':resultat[19],'Obs':event['ObsGen']})
        table = MatrimoniTable(protagonista)
    if event['tipus_event'] == 'Obituari':
        protagonista.append({'Arxiu':resultat[0],'Num_Reg':num_registre,'Data_Ins':event['DataIns'],'Data':event['Data_Event'],'Lloc':event['Lloc_Event'],'Nom':resultat[2],
                             'Cognom1':resultat[3],'Cognom2':resultat[4],'Alies':resultat[5],'Sexe':resultat[6],'Data_Naix':resultat[7],'Lloc_Naix':resultat[8],
                             'Edat':resultat[9],'Estat_civil':resultat[10],'Residencia':resultat[11],'Ocupacio':resultat[12],'Data_Ente':resultat[13],'Lloc_Ente':resultat[14],'Cementiri':resultat[15],
                             'noms_fills':resultat[16],'ObsP':resultat[17],'ObsG':event['ObsGen']})
        table = ObituariTable(protagonista)
    consulta = 'select * from participant where nom_llibre = \''+nom_llibre+'\' and num_registre = '+str(num_registre)
    with connection.cursor() as cursor:   #Consulta BBDD
            cursor.execute(consulta)
            resultat = cursor.fetchall()
    partable = []
    for a in resultat:
        partable.append({'Arxiu':a[0],'Num_Reg':num_registre,'Tip_Event':a[2],
                         'Data_Event':event['Data_Event'],'Tip_part':a[3],'Nom':a[4],
                         'Cognom1':a[5],'Cognom2':a[6],'Estat_vital':a[7],
                         'Ofici':a[8],'Lloc_Naix':a[9],'Resid':a[10]})
    tableP = ParticipantTable(partable)
    RequestConfig(request).configure(table)
    table.paginate(page = request.GET.get('page',1),per_page=10)
    RequestConfig(request).configure(tableP)
    tableP.paginate(page = request.GET.get('page',1),per_page=10)

    image = arbre.getGraph(protagonista, partable, event['tipus_event'])
    
    context = {'protagonista':table,'participacions':tableP, 'image':image}
 
    return render(request,'tfg/detail.html',context)
#%%
def vida(request):
    global vidaform
    if request.method == 'POST' or bool(vidaform):
        if request.method == 'POST': vidaform = NomDataForm(request.POST)
        vidaform.is_valid()
        fdict = {}
        try:
            fdict = vidaform.cleaned_data
        except:    
            print('Error al cleaned data vida')
        consultaB = "";consultaM = "";consultaO = "";consultaP = ""
        Buit = True
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consultaB = "select * from  baptisme natural join event_taula WHERE "
                consultaM = "select * from  matrimoni natural join event_taula WHERE "
                consultaO = "select * from  obituari natural join event_taula WHERE "
                consultaP = "select * from  participant natural join event_taula WHERE "
                Buit = False
                break

        consultaB,_= Assistant.AddParameters(fdict,consultaB)
        consultaO,_= Assistant.AddParameters(fdict,consultaO)
        consultaM,_ = Assistant.AddParametersMatrimoni(fdict,consultaM)   
        consultaP,newform = Assistant.AddParameters(fdict,consultaP)
#        newform = dict(list(newform1.items()) + list(newformData.items()))
        tableB=[];tableM=[];tableO=[];tableP=[]
        if not Buit:
            tableB = Assistant.getTable(consultaB,'Baptisme')
            tableM = Assistant.getTable(consultaM,'Matrimoni')
            tableO = Assistant.getTable(consultaO,'Obituari')
            tableP = Assistant.getTable(consultaP,'Participant')

        vides = Assistant.getVides(tableB,tableM,tableO,tableP)
        vidaform = NomDataForm(newform)
        context = {'form':vidaform,'vides':vides}
        return render(request,'tfg/general_vida.html',context)
    else:
        vidaform = NomDataForm()
        vides = []
        context = {'form':vidaform,'vides':vides}
        return render(request,'tfg/general_vida.html',context)
        
#%%

def simpleMortalitatInfantil(request):   
    return render(request,'tfg/base_obituaris_stats.html',{})
#%%

def FillsCasats(request):
    global fillscasatsform
    if request.method == 'POST' or bool(fillscasatsform):
        if request.method == 'POST': fillscasatsform = NomDataForm(request.POST)
        fillscasatsform.is_valid()
        fdict = {}
        try:
            fdict = fillscasatsform.cleaned_data
        except:    
            print('Error al cleaned data Fillscasats')
        consulta = ""
        Buit = True
        for e in fdict:
            if fdict[e]!='-' and fdict[e]!='':
                consulta = "select * from matrimoni  natural join event_taula b, participant p where b.nom_llibre = p.nom_llibre and b.num_registre = p.num_registre and (p.tipus_part= 'Pare Marit' or p.tipus_part = 'Mare Marit' or  p.tipus_part = 'Mare Muller' or p.tipus_part = 'Pare Muller') and "
                Buit = False
                break
        consulta,newform = Assistant.AddParameters2(fdict,consulta)
        with connection.cursor() as cursor:   #Consulta 
            if not Buit:
                cursor.execute(consulta)
                resultat = cursor.fetchall()
            else:
                resultat = []
        partable = []
        mattable = []
        for a in resultat:
            partable.append({'Arxiu':a[25],'Num_Reg':a[26],'Tip_Event':a[27],
                             'Data_Event':a[21],'Tip_part':a[28],'Nom':a[29],
                             'Cognom1':a[30],'Cognom2':a[31],'Estat_vital':a[32],
                             'Ofici':a[33],'Lloc_Naix':a[34],'Resid':a[35]})
            mattable.append({'Arxiu':a[0],'Num_Reg':a[1],'Data_Ins':a[20],'Data':a[21],'Lloc':a[22],'Nom_Marit':a[2],
                             'Cognom1_Marit':a[3],'Cognom2_Marit':a[4],'Edat_Marit':a[5],
                             'Lloc_Naix_Marit':a[6],'Est_Marit':a[7],'Residencia_Marit':a[8],'Ocupacio_Marit':[9],
                             'Nom_Muller':a[10],'Cognom1_Muller':a[11],'Cognom2_Muller':a[12],'Alies_Muller':a[13],
                             'Lloc_Naix_Muller':a[14],'Residencia_Muller':a[15],'Edat_Muller':a[16],'Est_Muller':a[17],
                             'Esglesia':a[18],'Cap_Mat':a[19],'Obs':a[24]})
        tableM = MatrimoniTable(mattable)
        RequestConfig(request).configure(tableM)
        tableM.paginate(page = request.GET.get('page',1),per_page=10)
        tableP = ParticipantTable(partable)
        RequestConfig(request).configure(tableP)
        tableP.paginate(page = request.GET.get('page',1),per_page=10)
        fillscasatsform = NomDataForm(newform)
        context = {'matrimonis':tableM,'participacions':tableP,'form':fillscasatsform}
        return render(request,'tfg/matrimonis_fillscasats.html',context)
    else:
        fillscasatsform = NomDataForm()
        tableM = MatrimoniTable([])
        tableP = ParticipantTable([])
        context = {'matrimonis':tableM,'participacions':tableP,'form':fillscasatsform}
    return render(request,'tfg/matrimonis_fillscasats.html',context)