# -*- coding: utf-8 -*-
"""
Created on Tue May 08 18:28:16 2018

@author: Nicola
"""

from tfg.models import PersonaBuidatrev,Parroquia,Arxiu,Registre,EventTaula,Baptisme
from tfg.models import Matrimoni,Obituari,Participant,Persona
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Since the CSV headers match the model fields,
        # you only need to provide the file's path (or a Python file object)
        directori = os.getcwd()
        os.chdir(r'C:\Users\Nicola\Documents\UPC\Sistemes d Informacio\mysite\tfg\dades')
        insert_count = PersonaBuidatrev.objects.from_csv(r'PersonaBR_CSV')
        print(insert_count)
        insert_count = Parroquia.objects.from_csv('Parroquia_CSV')
        print(insert_count)
        insert_count = Arxiu.objects.from_csv('arxiu_CSV')
        print(insert_count)
        insert_count = Registre.objects.from_csv('registre')
        print(insert_count)
        insert_count = EventTaula.objects.from_csv('event_taula')
        print(insert_count)
        insert_count = Baptisme.objects.from_csv('baptisme.csv')
        print(insert_count)
        insert_count = Matrimoni.objects.from_csv('matrimoni.csv')
        print(insert_count)
        insert_count = Obituari.objects.from_csv('obituari.csv')
        print(insert_count)        
        insert_count = Participant.objects.from_csv('participant.csv')
        print(insert_count)
        insert_count = Persona.objects.from_csv('persona.csv')
        print(insert_count)  
        
        os.chdir(directori)