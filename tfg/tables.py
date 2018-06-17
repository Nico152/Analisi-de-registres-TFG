# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:07:09 2018

@author: Nicola
"""

import django_tables2 as tables
#from tfg.models import Arxiu 

class ArxiuTable(tables.Table):
    Arxiu = tables.Column()
    Nom_Parroquia = tables.Column(verbose_name='Nom Parròquia')
    Persona_B = tables.Column(verbose_name = 'Persona Buidatge')
    Persona_R = tables.Column(verbose_name = 'Persona Revisat')
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        
class BatejatTable(tables.Table):
    Arxiu = tables.Column()
    Num_Reg = tables.Column(verbose_name='Nº')
    Data = tables.Column()
    LLoc = tables.Column()
    Nom = tables.Column()
    NomsComp = tables.Column(verbose_name='Noms Complementaris')
    Cognom1 = tables.Column(verbose_name='Primer Cognom')
    Cognom2 = tables.Column(verbose_name= 'Segon Cognom')
    Sexe = tables.Column()
    Data_Naix = tables.Column(verbose_name = 'Data Naixement')
    Lloc_Naix = tables.Column(verbose_name = 'Lloc Naixement')
    Obs = tables.Column(verbose_name = 'Observacions')
    ObsG = tables.Column(verbose_name = 'Observacions Generals')
    
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        row_attrs = {
                'onclick': lambda record: "myFunction(\'"+record['Arxiu'].strip()+"\',"+str(record['Num_Reg'])+")"
                }

class ParticipantTable(tables.Table):
    Arxiu = tables.Column()
    Num_Reg = tables.Column(verbose_name='Nº')
    Tip_Event = tables.Column(verbose_name = 'Tipus Esdeveniment')
    Data_Event = tables.Column()
    Tip_part = tables.Column(verbose_name = 'Tipus Relació')
    Nom = tables.Column()
    Cognom1 = tables.Column(verbose_name='Primer Cognom')
    Cognom2 = tables.Column(verbose_name= 'Segon Cognom') 
    Estat_vital = tables.Column(verbose_name='Estat Vital')
    Ofici = tables.Column()
    Lloc_Naix = tables.Column(verbose_name='Lloc Naixement')
    Resid = tables.Column(verbose_name='Residència')
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        row_attrs = {
                'onclick': lambda record: "myFunction(\'"+record['Arxiu'].strip()+"\',"+str(record['Num_Reg'])+")"
                }
    
class MatrimoniTable(tables.Table):
    Arxiu = tables.Column()
    Num_Reg = tables.Column(verbose_name='Nº')
    Data_Ins = tables.Column(verbose_name = 'Data Inscripció')
    Data = tables.Column()
    LLoc = tables.Column()
    Nom_Marit = tables.Column(verbose_name = 'Nom Marit')
    Cognom1_Marit = tables.Column(verbose_name = 'Primer Cognom Marit')
    Cognom2_Marit = tables.Column(verbose_name = 'Segon Cognom Marit')
    Edat_Marit = tables.Column(verbose_name = 'Edat Marit')
    Lloc_Naix_Marit = tables.Column(verbose_name = 'Lloc Naixement Marit')
    Est_Marit = tables.Column(verbose_name = 'Estat Civil Marit')
    Residencia_Marit = tables.Column(verbose_name = 'Residència Marit')
    Ocup_Marit = tables.Column(verbose_name = 'Ocupació Marit')
    Nom_Muller = tables.Column(verbose_name = 'Nom Muller')
    Cognom1_Muller = tables.Column(verbose_name = 'Primer Cognom Muller')
    Cognom2_Muller = tables.Column(verbose_name = 'Segon Cognom Muller')
    Alies_Muller = tables.Column(verbose_name = 'Àlies Muller')
    Lloc_Naix_Muller = tables.Column(verbose_name = 'Lloc Naixement Muller')
    Residencia_Muller = tables.Column(verbose_name = 'Residència Muller')
    Edat_Muller = tables.Column(verbose_name = 'Edat Muller')
    Est_Muller = tables.Column(verbose_name = 'Estat Civil Muller')
    Esglesia = tables.Column(verbose_name = 'Esglèsia')
    Cap_Mat = tables.Column(verbose_name = 'Capitols Matrimonials')
    Obs = tables.Column(verbose_name = 'Observacions Generals')
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        row_attrs = {
                'onclick': lambda record: "myFunction(\'"+record['Arxiu'].strip()+"\',"+str(record['Num_Reg'])+")"
                }
        

class ObituariTable(tables.Table):
    Arxiu = tables.Column()
    Num_Reg = tables.Column(verbose_name = 'Nº')
    Data_Ins = tables.Column(verbose_name = 'Data Inscripció')
    Data = tables.Column()
    LLoc = tables.Column()
    Nom = tables.Column()
    Cognom1 = tables.Column(verbose_name='Primer Cognom')
    Cognom2 = tables.Column(verbose_name= 'Segon Cognom')
    Alies = tables.Column(verbose_name = 'Àlies')
    Sexe = tables.Column()
    Data_Naix = tables.Column(verbose_name= 'Data Naixement')
    Lloc_Naix = tables.Column(verbose_name = 'Lloc Naixement')
    Edat = tables.Column()
    Estat_civil = tables.Column(verbose_name = 'Estat civil')
    Residencia = tables.Column(verbose_name = 'Residència')
    Ocupacio = tables.Column(verbose_name = 'Ocupació')
    Data_Ente = tables.Column(verbose_name = 'Data Enterrament')
    Lloc_Ente = tables.Column(verbose_name = 'Lloc Enterrament')
    Cementiri = tables.Column()
    nom_fills = tables.Column(verbose_name = 'Noms Fills')
    ObsP = tables.Column(verbose_name = 'Observació Persona')
    ObsG = tables.Column(verbose_name = 'Observació General')
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        row_attrs = {
                'onclick': lambda record: "myFunction(\'"+record['Arxiu'].strip()+"\',"+str(record['Num_Reg'])+")"
                }
    
    