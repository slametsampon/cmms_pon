from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Group


class Section(models.Model):
    """Model representing a section of organization"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of section(eg. Electrical & Instrumentation)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of section')
    # Foreign Key used because section can only have one department, but department can have multiple sections
    # Section as a string rather than object because it hasn't been declared yet in the file
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['department','name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #get dept object
        depName = dtDict.get('foreign_department')
        dept = Department.objects.get(name = depName)

        #remove key foreign_department
        dtDict.pop('foreign_department')

        #insert Department
        dtDict['department']=dept

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

class Department(models.Model):
    """Model representing a department of organization"""
    name = models.CharField(max_length=50, null=True, help_text='Enter name of section(eg. Maintenance)')
    
    #initial for numbering of work order PROD/xxxx, HRGA/xxxx
    initial = models.CharField(max_length=5, null=True, help_text='Enter initial of section(eg. Mntc)')
    description = models.CharField(max_length=200, null=True, help_text='Enter description of department')
    
    class Meta:
        ordering = ['name']

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

#class Mode for action
class Mode(models.Model):
    """Model representing a Mode of Action"""
    name = models.CharField(max_length=10, null=True, help_text='Enter name of Mode(eg. Reverse, Forward, Stay)')
    MODE = (
        ('Forward', 'Forward'),
        ('Reverse', 'Reverse'),
        ('Stay', 'Stay'),
    )

    name = models.CharField(max_length=10,
        choices=MODE,
        blank=True,
        help_text='Select Mode',
        default='Forward')

    class Meta:
        ordering = ['name']

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

#class Category for action
class Category(models.Model):
    """Model representing a Category of actions"""
    name = models.CharField(max_length=10, null=True, help_text='Enter name of Mode(eg. Reverse, Forward, Stay)')
    CATEGORY = (
        ('Pending', 'Pending'),
        ('Finish', 'Finish'),
        ('Schedule', 'Schedule'),
        ('Close', 'Close'),
    )

    name = models.CharField(max_length=10,
        choices=CATEGORY,
        blank=True,
        help_text='Select Category',
        default='Pending')

    class Meta:
        ordering = ['name']

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

class Action(models.Model):
    """Model representing a Action of organization"""
    name = models.CharField(max_length=20, null=True, help_text='Enter name of Action(eg. Open, Close, Reject...)')
    description = models.CharField(max_length=100, null=True, help_text='Enter description of Action')

    # Foreign Key used because Action can only have one mode, but mode can have multiple actions
    # Section as a string rather than object because it hasn't been declared yet in the file
    mode = models.ForeignKey('Mode', on_delete=models.SET_NULL, null=True)

    # Foreign Key used because Action can only have one category, but category can have multiple actions
    # Section as a string rather than object because it hasn't been declared yet in the file
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #insert mode
        dtDict['mode'] = Mode.objects.get(name = dtDict.get('foreign_mode'))
        #remove key foreign_mode
        dtDict.pop('foreign_mode')

        #insert category
        dtDict['category'] = Category.objects.get(name = dtDict.get('foreign_category'))
        #remove key foreign_category
        dtDict.pop('foreign_category')

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

class CmmsUser(AbstractUser):
    forward_path = models.IntegerField(null=True)#CmmsUser.id
    reverse_path = models.IntegerField(null=True)#CmmsUser.id

    # ManyToManyField used because Action can contain many CmmsUsers. CmmsUser can cover many Actions.
    # Action class has already been defined so we can specify the object above.
    actions = models.ManyToManyField(Action, help_text='Select actions')

    # Foreign Key used because user can only have one section, but section can have multiple users
    # Section as a string rather than object because it hasn't been declared yet in the file
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)

    # Foreign Key used because user can only have one group, but group can have multiple users
    #group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self, just for username and password
    def init_minimum_data(cls,dtDict):

        return cls.objects.update_or_create(
            username= dtDict.get('username'),
            password=dtDict.get('password'),
        )            

    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_dict(cls,dtDict):

        #insert section
        dtDict['section'] = Section.objects.get(name = dtDict.get('foreign_section'))
        #remove key foreign_section
        dtDict.pop('foreign_section')

        #insert group
        dtDict['group'] = Group.objects.get(name = dtDict.get('foreign_group'))
        #remove key foreign_group
        dtDict.pop('foreign_group')

        #update from name to id
        usr = None
        if dtDict.get('forward_path'):
            usr = CmmsUser.objects.get(username = dtDict.get('forward_path'))
        dtDict['forward_path'] = usr.id

        #update from name to id
        usr = None
        if dtDict.get('reverse_path'):
            usr = CmmsUser.objects.get(username = dtDict.get('reverse_path'))
        dtDict['reverse_path'] = usr.id

        #get first key for unique key
        k=None
        for k,v in dtDict.items():
            if k:
                break
        
        #user as unique value, kindly modify as needed
        return cls.objects.update_or_create(
            username=dtDict.get('username'),
            defaults=dtDict,
        )            

    #Many to many relationship
    #this decorator make posible to call method w/o instantiate class
    @classmethod
    #use cls instead of self
    def update_or_create_action_dict(cls,dtDict):

        #get CmmsUser
        usr = None
        if dtDict.get('username'):
            usr = CmmsUser.objects.get(username = dtDict.get('username'))

        #get action
        act = None
        if dtDict.get('action'):
            act = Action.objects.get(name=dtDict.get('action'))

        #add action to CmmsUser
        usr.actions.add(act)
        usr.save()
    
    def get_absolute_url(self):
        """Returns the url to access a list of work_orders."""
        #"""Returns the url to access a detail record for this work order."""
        return reverse('accounts:account-detail', args=[str(self.id)])

    def __str__(self):
        return self.username

