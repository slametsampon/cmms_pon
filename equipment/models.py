from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Group
from accounts.models import Section, Department


class Category(models.Model):
    """Model representing a Category of equipment"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of Category(eg. Motor, Compressor...)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of Category')
    # Foreign Key used because Category can only have one section, but section can have multiple Categorys
    # Category as a string rather than object because it hasn't been declared yet in the file
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['section','name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #get sect object
        sectName = dtDict.get('foreign_section')
        sect = Section.objects.get(name = sectName)

        #remove key foreign_section
        dtDict.pop('foreign_section')

        #insert Section
        dtDict['section']=sect

        #get first key for unique key
        k=None
        for k,v in dtDict.items():
            if k:
                break
        
        #name as unique value, kindly modify as needed
        return cls.objects.update_or_create(
            name=v,
            defaults=dtDict,
        )            

class Risk(models.Model):
    """Model representing a Risk of RBM"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of Risk(eg. safety, enviromental)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of Risk')
    value = models.IntegerField(null=True)#value 0 - 5

    class Meta:
        ordering = ['name',]

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #get first key for unique key
        k=None
        for k,v in dtDict.items():
            if k:
                break
        
        #name as unique value, kindly modify as needed
        return cls.objects.update_or_create(
            name=v,
            defaults=dtDict,
        )            

class Unit(models.Model):
    """Model representing a Unit of Plant"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of Unit(eg. Boiler, Membrane, Cooling Tower)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of Unit')
    # Foreign Key used because Unit can only have one area, but area can have multiple Units
    # Unit as a string rather than object because it hasn't been declared yet in the file
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ['area','name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #get area object
        areaName = dtDict.get('foreign_area')
        areaObj = Section.objects.get(name = areaName)

        #remove key foreign_area
        dtDict.pop('foreign_area')

        #insert Area
        dtDict['area']=areaObj

        #get first key for unique key
        k=None
        for k,v in dtDict.items():
            if k:
                break
        
        #name as unique value, kindly modify as needed
        return cls.objects.update_or_create(
            name=v,
            defaults=dtDict,
        )            

class Area(models.Model):
    """Model representing a Area of Plant"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of Area(eg. Utility, Area 100, CO2)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of Area')
    # Foreign Key used because Area can only have one department, but department can have multiple Areas
    # Department as a string rather than object because it hasn't been declared yet in the file
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ['department','name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #get department object
        departmentName = dtDict.get('foreign_department')
        departmentObj = Section.objects.get(name = departmentName)

        #remove key foreign_department
        dtDict.pop('foreign_department')

        #insert department
        dtDict['department']=departmentObj

        #get first key for unique key
        k=None
        for k,v in dtDict.items():
            if k:
                break
        
        #name as unique value, kindly modify as needed
        return cls.objects.update_or_create(
            name=v,
            defaults=dtDict,
        )            

class Equipment(models.Model):
    """Model representing a Equipment of Plant"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of Equipment(eg. TI-4102, C-018, P-021)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of Equipment')
    # Foreign Key used because Equipment can only have one unit, but unit can have multiple Equipments
    # unit as a string rather than object because it hasn't been declared yet in the file
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    rbmEnv = models.IntegerField(null=True)#value 1 - 5
    rbmSafety = models.IntegerField(null=True)#value 1 - 5
    rbmCont = models.IntegerField(null=True)#value 1 - 5
    class Meta:
        ordering = ['unit','name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #get unit object
        unitName = dtDict.get('foreign_unit')
        unitObj = Unit.objects.get(name = unitName)

        #remove key foreign_unit
        dtDict.pop('foreign_unit')

        #insert unit
        dtDict['unit']=unitObj

        #get first key for unique key
        k=None
        for k,v in dtDict.items():
            if k:
                break
        
        #name as unique value, kindly modify as needed
        return cls.objects.update_or_create(
            name=v,
            defaults=dtDict,
        )            

#just testing git