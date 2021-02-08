from django.db import models
from accounts.models import Section, Department
from pm_pdm.models import PM_PdM

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
    value = models.IntegerField(null=True)#value 1 - 5

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
    rbmValue = models.IntegerField(null=True)#value 1 - 125
    rbmGrade = models.CharField(max_length=50, null=True, help_text='Enter grade of Risk(eg. Critical, Normal, Less)')

    # ManyToManyField used because Equipment can contain many risks. risk can cover many equipments.
    # Action class has already been defined so we can specify the object above.
    risks = models.ManyToManyField(Risk, help_text='Select risks')

    # ManyToManyField used because tbm can contain many PM_PdM. PM_PdM can cover many tbm.
    # PM_PdM class has already been defined so we can specify the object above.
    tbm = models.ManyToManyField(PM_PdM, help_text='Select PM_PdM')

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

    #Many to many relationship
    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_risks_dict(cls,dtDict):

        #get Equipment
        eqp = None
        if dtDict.get('name'):
            eqp = Equipment.objects.get(name = dtDict.get('name'))

        #get risk
        rsk = None
        if dtDict.get('risk'):
            rsk = Risk.objects.get(name=dtDict.get('risk'))

        #add rsk to Equipment
        eqp.risks.add(rsk)
        eqp.save()
    
    #Many to many relationship
    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_tbm_dict(cls,dtDict):

        #get Equipment
        eqp = None
        if dtDict.get('name'):
            eqp = Equipment.objects.get(name = dtDict.get('name'))

        #get tbm - PmPdM
        pm_pdm = None
        if dtDict.get('risk'):
            pm_pdm = Risk.objects.get(name=dtDict.get('risk'))

        #add pm_pdm to Equipment
        eqp.tbm.add(pm_pdm)
        eqp.save()
    
class TBM_Package(models.Model):
    """Model representing a TBM - Time Based Maintenance"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of TBM(eg. PM Critical)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of TBM')
    periode = models.IntegerField(null=True, help_text='Enter periode of TBM (week)')#value 1 - 51

    # ManyToManyField used because eqpPackage can contain many Equipment. Equipment can cover many eqpPackages.
    # Equipment class has already been defined so we can specify the object above.
    eqpPackage = models.ManyToManyField(Equipment, help_text='Select TBM')

    class Meta:
        ordering = ['periode','name']

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

    #Many to many relationship
    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_package_dict(cls,dtDict):

        #get TBM_Package
        pkg = None
        if dtDict.get('name'):
            pkg = TBM_Package.objects.get(name = dtDict.get('name'))

        #get Equioment
        eqp = None
        if dtDict.get('eqp'):
            eqp = Equipment.objects.get(name=dtDict.get('eqp'))

        #add eqp to TBM_Package
        pkg.risks.add(eqp)
        pkg.save()
    
