# -*- coding: utf-8 -*-
"""
Created on Sat Jun 02 20:03:42 2018

@author: Nicola
"""

import psycopg2
import matplotlib.pylab as plt

try:
    conn = psycopg2.connect("dbname='TFG' user='postgres' host='localhost' password='peca2012'")
except:
    print "I am unable to connect to the database"

consulta = "select data_event, data_inscripcio, data_enterrament, edat, substring(data_event,1,4) ~  '^[0-9\.]+$' AS IsDataEvent, "
consulta += "substring(data_inscripcio,1,4) ~  '^[0-9\.]+$' AS IsDataInsc, substring(data_enterrament,1,4) ~  '^[0-9\.]+$' AS IsDataEnterrament"
consulta += " from event_taula natural join obituari"
with conn.cursor() as cursor:
    cursor.execute(consulta)
    resultat = cursor.fetchall()
    
    
D = {'1707-1709':0,'1710-1719':0,'1720-1729':0,'1730-1739':0,'1740-1749':0,
     '1750-1759':0,'1760-1769':0,'1770-1779':0,'1780-1789':0,'1790-1799':0,
     '1800-1809':0,'1810-1819':0,'1820-1829':0,'1830-1839':0,'1840-1849':0,
     '1850-1851':0}
for a in resultat:
    AnyMort = " ";
    if a[4]: AnyMort= a[0][0:4]
    elif a[5]: AnyMort = a[1][0:4]
    elif a[6]: AnyMort = a[2][0:4]
    
    if AnyMort != " " and a[3]:
        edat = a[3]
        edatnumerica = 0
        for c in edat:
            if c.isdigit():
                edatnumerica = edatnumerica*10+int(c)
        if 'a' in edat and not 'dia' in edat: 
            isMortalitatInfantil = False
        elif 'm' in edat and edatnumerica < 12:
            isMortalitatInfantil = True
        elif ('d' or 's' or 'néixer' or 'neixer') in edat or edatnumerica == 0:
            isMortalitatInfantil = True
        else:
            isMortalitatInfantil = False
        if isMortalitatInfantil:
            if int(AnyMort) < 1710: D['1707-1709'] +=1 
            elif int(AnyMort) < 1720: D['1710-1719'] +=1
            elif int(AnyMort) < 1730: D['1720-1729'] +=1
            elif int(AnyMort) < 1740: D['1730-1739'] +=1
            elif int(AnyMort) < 1750: D['1740-1749'] +=1
            elif int(AnyMort) < 1760: D['1750-1759'] +=1
            elif int(AnyMort) < 1770: D['1760-1769'] +=1
            elif int(AnyMort) < 1780: D['1770-1779'] +=1
            elif int(AnyMort) < 1790: D['1780-1789'] +=1
            elif int(AnyMort) < 1800: D['1790-1799'] +=1
            elif int(AnyMort) < 1810: D['1800-1809'] +=1
            elif int(AnyMort) < 1820: D['1810-1819'] +=1
            elif int(AnyMort) < 1830: D['1820-1829'] +=1
            elif int(AnyMort) < 1840: D['1830-1839'] +=1
            elif int(AnyMort) < 1850: D['1840-1849'] +=1
            else: D['1850-1851'] +=1
        

keys = list(D.keys())                
keys.sort()
values = []
for a in keys:
    values.append(D[a])
    
    
plt.bar(range(len(D)),values,align='center')
plt.xticks(range(len(D)),keys,rotation = 90)
plt.rcParams["figure.figsize"] = [4,4.5]
plt.savefig('fig1.png', dpi = 300)
plt.close()

