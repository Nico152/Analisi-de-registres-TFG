# -*- coding: utf-8 -*-
"""
Created on Sun May 13 16:51:56 2018

@author: Nicola
"""

from django import forms

class NomForm(forms.Form):
    nom = forms.CharField(label='Nom', max_length=100)
    cognom1 = forms.CharField(label='Primer Cognom', max_length=100)
    cognom2 = forms.CharField(label='Segon Cognom', max_length=100)
    
class NomDataForm(forms.Form):
    nom = forms.CharField(label='Nom', max_length=100, widget=forms.TextInput(attrs={'class': 'NomData'}))
    cognom1 = forms.CharField(label='1r Cognom', max_length=100, widget=forms.TextInput(attrs={'class': 'NomData'}))
    cognom2 = forms.CharField(label='2n Cognom', max_length=100, widget=forms.TextInput(attrs={'class': 'NomData'}))
    dataini = forms.CharField(label='Data Inicial', max_length=4, widget=forms.TextInput(attrs={'class': 'NomData'}))
    datafi = forms.CharField(label='Data Final', max_length=4, widget=forms.TextInput(attrs={'class': 'NomData'}))
    
class DataOnlyForm(forms.Form):
    dataini = forms.CharField(label='Data Inicial', max_length=4, widget=forms.TextInput(attrs={'class': 'NomData'}))
    datafi = forms.CharField(label='Data Final', max_length=4, widget=forms.TextInput(attrs={'class': 'NomData'}))