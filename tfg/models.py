from django.db import models
#from postgres_copy import CopyManager

# Create your models here.

#class PersonaBuidatrev(models.Model):
#    codi_nom = models.CharField(primary_key=True, max_length=4)
#    objects = CopyManager()
#    
#    class Meta:
#        managed = True
#        db_table = 'persona_buidatrev'
#        
#class Parroquia(models.Model):
#    nom_parroquia = models.CharField(primary_key=True, max_length=40)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'parroquia'
#        
#
#class Arxiu(models.Model):
#    nom_llibre = models.CharField(primary_key=True, max_length=20)
#    nom_parroquia = models.ForeignKey('Parroquia', models.DO_NOTHING, db_column='nom_parroquia', blank=True, null=True)
#    p_buidat = models.ForeignKey('PersonaBuidatrev', models.DO_NOTHING, db_column='p_buidat',related_name='p_buidat+', blank=True, null=True)
#    p_revisat = models.ForeignKey('PersonaBuidatrev', models.DO_NOTHING, db_column='p_revisat',related_name='p_revisat+', blank=True, null=True)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'arxiu'
#
#
#
#class Registre(models.Model):
#    nom_llibre = models.CharField(max_length=20)
#    num_registre = models.IntegerField()
#    pag_llibre = models.CharField(max_length=20, blank=True, null=True)
#    pag_pdf = models.IntegerField(blank=True, null=True)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'registre'
#        unique_together = (('nom_llibre', 'num_registre'),)
#
#class EventTaula(models.Model):
#    nom_llibre = models.CharField(max_length=20)
#    num_registre = models.IntegerField()
#    data_inscripcio = models.CharField(max_length=12, blank=True, null=True)
#    data_event = models.CharField(max_length=12, blank=True, null=True)
#    lloc_event = models.CharField(max_length=175, blank=True, null=True)
#    tipus_event = models.TextField(blank=True, null=True)  # This field type is a guess.
#    observaciogeneral = models.CharField(max_length=500, blank=True, null=True)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'event_taula'
#        unique_together = (('nom_llibre', 'num_registre'),)
#
#
#
#class Baptisme(models.Model):
#    nom_llibre = models.CharField(max_length=20)
#    num_registre = models.IntegerField()
#    nom = models.CharField(max_length=50, blank=True, null=True)
#    noms_complementaris = models.CharField(max_length=70, blank=True, null=True)
#    cognom1 = models.CharField(max_length=50, blank=True, null=True)
#    cognom2 = models.CharField(max_length=50, blank=True, null=True)
#    sexe = models.TextField(blank=True, null=True)  # This field type is a guess.
#    data_naixement = models.CharField(max_length=12, blank=True, null=True)
#    lloc_naixement = models.CharField(max_length=100, blank=True, null=True)
#    observacio = models.CharField(max_length=500, blank=True, null=True)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'baptisme'
#        unique_together = (('nom_llibre', 'num_registre'),)
#
#
#
#class Matrimoni(models.Model):
#    nom_llibre = models.CharField(max_length=20)
#    num_registre = models.IntegerField()
#    nom_marit = models.CharField(max_length=50, blank=True, null=True)
#    cognom1_marit = models.CharField(max_length=50, blank=True, null=True)
#    cognom2_marit = models.CharField(max_length=50, blank=True, null=True)
#    edat_marit = models.CharField(max_length=50, blank=True, null=True)
#    lloc_naixement_marit = models.CharField(max_length=100, blank=True, null=True)
#    estat_civil_marit = models.CharField(max_length=50, blank=True, null=True)
#    residencia_marit = models.CharField(max_length=100, blank=True, null=True)
#    ocupacio_marit = models.CharField(max_length=300, blank=True, null=True)
#    nom_muller = models.CharField(max_length=50, blank=True, null=True)
#    cognom1_muller = models.CharField(max_length=50, blank=True, null=True)
#    cognom2_muller = models.CharField(max_length=50, blank=True, null=True)
#    alies_muller = models.CharField(max_length=20, blank=True, null=True)
#    lloc_naixement_muller = models.CharField(max_length=100, blank=True, null=True)
#    residencia_muller = models.CharField(max_length=100, blank=True, null=True)
#    edat_muller = models.CharField(max_length=50, blank=True, null=True)
#    estat_civil_muller = models.CharField(max_length=50, blank=True, null=True)
#    esglesia = models.CharField(max_length=100, blank=True, null=True)
#    capitols_mat = models.CharField(max_length=100, blank=True, null=True)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'matrimoni'
#        unique_together = (('nom_llibre', 'num_registre'),)
#
#
#class Obituari(models.Model):
#    nom_llibre = models.CharField(max_length=20)
#    num_registre = models.IntegerField()
#    nom = models.CharField(max_length=50, blank=True, null=True)
#    cognom1 = models.CharField(max_length=50, blank=True, null=True)
#    cognom2 = models.CharField(max_length=50, blank=True, null=True)
#    alies = models.CharField(max_length=50, blank=True, null=True)
#    sexe = models.TextField(blank=True, null=True)  # This field type is a guess.
#    data_naixement = models.CharField(max_length=12, blank=True, null=True)
#    lloc_naixement = models.CharField(max_length=122, blank=True, null=True)
#    edat = models.CharField(max_length=50, blank=True, null=True)
#    estat_civil = models.CharField(max_length=20, blank=True, null=True)
#    residencia = models.CharField(max_length=101, blank=True, null=True)
#    ocupacio = models.CharField(max_length=300, blank=True, null=True)
#    data_enterrament = models.CharField(max_length=12, blank=True, null=True)
#    lloc_enterrament = models.CharField(max_length=500, blank=True, null=True)
#    cementiri = models.CharField(max_length=120, blank=True, null=True)
#    noms_fills = models.CharField(max_length=121, blank=True, null=True)
#    obs_obi = models.CharField(max_length=500, blank=True, null=True)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'obituari'
#        unique_together = (('nom_llibre', 'num_registre'),)
#
#
#
#class Participant(models.Model):
#    nom_llibre = models.CharField(max_length=20)
#    num_registre = models.IntegerField()
#    tipus_event = models.TextField(blank=True, null=True)  # This field type is a guess.
#    tipus_part = models.TextField()  # This field type is a guess.
#    nom = models.CharField(max_length=50, blank=True, null=True)
#    cognom1 = models.CharField(max_length=50, blank=True, null=True)
#    cognom2 = models.CharField(max_length=50, blank=True, null=True)
#    estat_vital = models.TextField(blank=True, null=True)  # This field type is a guess.
#    ofici_carrec = models.CharField(max_length=300, blank=True, null=True)
#    lloc_naixement = models.CharField(max_length=100, blank=True, null=True)
#    residencia = models.CharField(max_length=100, blank=True, null=True)
#    observacio = models.CharField(max_length=500, blank=True, null=True)
#    objects = CopyManager()
#
#    class Meta:
#        managed = True
#        db_table = 'participant'
#        unique_together = (('nom_llibre', 'num_registre', 'tipus_part'),)
#
#
#class Persona(models.Model):
#    nom = models.CharField(max_length=50, blank=True, null=True)
#    cognom1 = models.CharField(max_length=50, blank=True, null=True)
#    cognom2 = models.CharField(max_length=50, blank=True, null=True)
#    sexe = models.TextField(blank=True, null=True)  # This field type is a guess.
#    estat_vital = models.TextField(blank=True, null=True)  # This field type is a guess.
#    ofici_carrec = models.CharField(max_length=300, blank=True, null=True)
#    alies = models.CharField(max_length=50, blank=True, null=True)
#    estat_civil = models.CharField(max_length=50, blank=True, null=True)
#    data_naixement = models.CharField(max_length=12, blank=True, null=True)
#    lloc_naixement = models.CharField(max_length=100, blank=True, null=True)
#    residencia = models.CharField(max_length=100, blank=True, null=True)
#    objects = CopyManager()
#    
#    class Meta:
#        managed = True
#        db_table = 'persona'






#class Persona_BR(models.Model):
#    codi_nom = models.CharField(max_length=4, primary_key = True)
#    objects = CopyManager()
#    
#class Parroquia(models.Model):
#    nom_parroquia = models.CharField(max_length = 40, primary_key = True)
#    objects = CopyManager()
#    
#class arxiu(models.Model):
#    nom_llibre = models.CharField(max_length = 20, primary_key = True)
#    nom_parroquia = models.ForeignKey(Parroquia,on_delete=None,blank = True,null = True)
#    p_buidat = models.ForeignKey(Persona_BR,on_delete=None,related_name='Persona Buidatge +',blank = True,null = True)
#    p_revisat = models.ForeignKey(Persona_BR,on_delete=None,related_name='Persona Revisio +',blank = True,null = True)
#    objects = CopyManager()
