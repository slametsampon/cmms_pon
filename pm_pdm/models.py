from django.db import models

class Activity(models.Model):
    """Model representing a Activity of PM PdM"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of Activity(eg. Cleaning, Greasing, Covering)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of Activity')
    duration = models.IntegerField(null=True)#minutes
    manPower = models.IntegerField(null=True)#personel number

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

class PM_PdM(models.Model):
    """Model representing a PM_PdM"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of Activity(eg. PM Motor AC)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of PM_PdM')
    mode = models.CharField(max_length=200, null=True, help_text='Enter mode of PM_PdM (eg. Running, Stop)')

    # ManyToManyField used because Equipment can contain many risks. risk can cover many equipments.
    # Action class has already been defined so we can specify the object above.
    activities = models.ManyToManyField(Activity, help_text='Select activities')


    class Meta:
        ordering = ['mode','name']

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
    def update_or_create_activities_dict(cls,dtDict):

        #get PM_PdM
        pm_pdm = None
        if dtDict.get('name'):
            pm_pdm = PM_PdM.objects.get(name = dtDict.get('name'))

        #get risk
        act = None
        if dtDict.get('activity'):
            act = Activity.objects.get(name=dtDict.get('activity'))

        #add act to PM_PdM
        pm_pdm.risks.add(act)
        pm_pdm.save()
    
