from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
from django.views.generic.edit import FormView
import datetime

import pandas as pd
from xlrd import open_workbook

from cmms_pon import settings 
from utility.forms import DepartmentForm, SectionForm, ImportFileForm
from accounts.models import Department, Section, Action, Mode, Category, CmmsUser
from work_order.models import Wo_priority
from utility.transform import dict_helper as dh


class UtilityHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'utility/home.html'

class DepartmentCreate(LoginRequiredMixin, CreateView):

    form_class = DepartmentForm
    model = Department
    template_name = 'utility/DepartmentForm.html'  # Specify your own template name/location

    # Sending user object to the form, to verify which fields to display/remove (depending on group)
    def get_form_kwargs(self):
        kwargs = super(DepartmentCreate, self).get_form_kwargs()

        return kwargs

    def get_initial(self):        
        initial = super(DepartmentCreate, self).get_initial()

        return initial
        # now the form will be shown with the link_pk bound to a value

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepartmentCreate,self).get_context_data(**kwargs)

        return context

    def form_valid(self, form,**kwargs):
        self.object = form.save(commit=False)

        self.object.save()

        return super(DepartmentCreate,self).form_valid(form)    

class SectionCreate(LoginRequiredMixin, CreateView):

    form_class = SectionForm
    model = Section
    template_name = 'utility/SectionForm.html'  # Specify your own template name/location

    # Sending user object to the form, to verify which fields to display/remove (depending on group)
    def get_form_kwargs(self):
        kwargs = super(SectionCreate, self).get_form_kwargs()

        return kwargs

    def get_initial(self):        
        initial = super(SectionCreate, self).get_initial()

        return initial
        # now the form will be shown with the link_pk bound to a value

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SectionCreate,self).get_context_data(**kwargs)

        return context

    def form_valid(self, form,**kwargs):
        self.object = form.save(commit=False)

        self.object.save()

        return super(SectionCreate,self).form_valid(form)    

class ImportFileFormView(FormView):
    template_name = 'utility/ImportFileForm.html'
    form_class = ImportFileForm
    success_url = '/utility/config/import/'

    MODEL = (
        (0,'Department'),
        (1,'Section'),
        (2,'Mode'),
        (3,'Category'),
        (4,'Action'),
        (5,'CmmsUser'),
        (6,'CmmsUserAction'),
        (7,'CmmsUserGroup'),
        (8,'Wo Priority'),
    )
    #buffer context
    plus_context = {}

    def get_initial(self):
        initial = super(ImportFileFormView, self).get_initial()

        #get parameter from request.POST parameters, and put default value if none 'key': 
        initial['file_name'] = self.plus_context.get('file_name', None)
        #print(f"initial['file_name'] : {initial['file_name']}")

        return initial
        # now the form will be shown with the link_pk bound to a value

    # Sending user object to the form, to verify which fields to display/remove (depending on group)
    def get_form_kwargs(self):
        kwargs = super(ImportFileFormView, self).get_form_kwargs()
        kwargs.update({'sheetNames': self.plus_context.get('sheetNames', None)})
        kwargs.update({'modelNames': self.plus_context.get('modelNames', None)})
        kwargs.update({'sheet_index': self.plus_context.get('sheet_index', 0)})
        kwargs.update({'model_index': self.plus_context.get('model_index', 0)})
        return kwargs

    def get_context_data(self, **kwargs):
        self.plus_context['modelNames'] = self.MODEL

        # Call the base implementation first to get a context self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)

        #restore previous value
        context['file_name'] = self.plus_context.get('file_name', None)
        context['sheetNames'] = self.plus_context.get('sheetNames', [])
        context['modelNames'] = self.plus_context.get('modelNames', [])

        isFileAvailable = self.plus_context.get('isFileAvailable', False)
        if isFileAvailable:
            self.plus_context['isFileAvailable'] = False
            context['dataDict']=self.plus_context.get('dataDict',None)
            context['countBefore'] = Action.objects.all().count()
            context['countAfter']=self.plus_context.get('countAfter',None)

        return context

    def form_valid(self, form,**kwargs):

        #get data from form 
        file_name = form.cleaned_data.get('file_name')
        model_index = form.cleaned_data.get('model_index')
        sheet_index = form.cleaned_data.get('sheet_index')

        #persistance previous value
        self.plus_context['sheet_index'] = sheet_index
        self.plus_context['model_index'] = model_index

        if not file_name:
            file_name = self.plus_context.get('file_name', None)

        if 'open_file' in self.request.POST:
            if len(file_name):
                self.plus_context['file_name'] = file_name
                self.plus_context['sheetNames'] = self.openFile(file_name)

        elif 'read_file' in self.request.POST:
            if len(file_name):
                #persistance previous value
                self.plus_context['isFileAvailable'] = True
                self.plus_context['dataDict'] = self.readFile(file_name, sheet_index)

        elif 'save_database' in self.request.POST:
            self.savaUpdateDatabase(model_index)

        return super(ImportFileFormView,self).form_valid(form)    

    def openFile(self, file_name):
        sheetList =[]
        
        file_name = f'{settings.MEDIA_ROOT}\{file_name}'
        book = open_workbook(file_name)
        sheetNames = book.sheet_names()

        if sheetNames:
            sheetDict ={}
            i=0
            for sheet in sheetNames:
                sheetDict[i]=sheet
                i+=1
            # Converting into list of tuple 
            sheetList = list(sheetDict.items())

        return sheetList

    def readFile(self, file_name, sheet_index):

        #get list of tuple
        file_name = f'{settings.MEDIA_ROOT}\{file_name}'
        sheet_name = self.plus_context.get('sheetNames')

        sheetIdx = sheet_name[sheet_index]
        sheet = sheetIdx[1]

        dataFrame = pd.read_excel(file_name, sheet)
        dataDict = dataFrame.to_dict()

        return (dataDict)

    def savaUpdateDatabase(self,model_index):
        modelIdx = self.MODEL[model_index]
        modelName = modelIdx[1]

        dataDict = self.plus_context.get('dataDict',None)
        if modelName == 'Department':
            for dtDict in dh.to_pair_dict(dataDict):

                #update_or_create for first field as unique value
                obj, created = Department.update_or_create_dict(dtDict)            
            self.plus_context['countAfter'] = Department.objects.all().count()

        elif modelName == 'Section':
            for dtDict in dh.to_pair_dict(dataDict):
                
                #update_or_create for first field as unique value
                obj, created = Section.update_or_create_dict(dtDict)            
            self.plus_context['countAfter'] = Section.objects.all().count()

        elif modelName == 'Action':
            for dtDict in dh.to_pair_dict(dataDict):

                #update_or_create for first field as unique value
                obj, created = Action.update_or_create_dict(dtDict)            
            self.plus_context['countAfter'] = Action.objects.all().count()

        elif modelName == 'Category':
            for dtDict in dh.to_pair_dict(dataDict):
                
                #update_or_create_dict
                obj, created = Category.update_or_create_dict(dtDict)            
            self.plus_context['countAfter'] = Category.objects.all().count()

        elif modelName == 'Mode':
            for dtDict in dh.to_pair_dict(dataDict):
                
                #update_or_create_dict
                obj, created = Mode.update_or_create_dict(dtDict)            
            self.plus_context['countAfter'] = Mode.objects.all().count()

        elif modelName == 'CmmsUser':
            for dtDict in dh.to_pair_dict(dataDict):
                #init_minimum_data, username and password first
                obj, created = CmmsUser.init_minimum_data(dtDict)            

            for dtDict in dh.to_pair_dict(dataDict):
                #update_or_create_dict
                obj, created = CmmsUser.update_or_create_dict(dtDict)            
            self.plus_context['countAfter'] = CmmsUser.objects.all().count()

        elif modelName == 'CmmsUserAction':
            for dtDict in dh.to_pair_dict(dataDict):
                
                #update_or_create_action_dict
                CmmsUser.update_or_create_action_dict(dtDict)            
            self.plus_context['countAfter'] = CmmsUser.objects.all().count()

        elif modelName == 'CmmsUserGroup':
            for dtDict in dh.to_pair_dict(dataDict):
                k=None
                for k,v in dtDict.items():
                    if k:
                        break
                #username as unique value
                obj, created = Group.objects.update_or_create(
                    name=v,
                )    
            self.plus_context['countAfter'] = Group.objects.all().count()

        elif modelName == 'Wo Priority':
            for dtDict in dh.to_pair_dict(dataDict):
                
                #update_or_create_dict
                Wo_priority.update_or_create_dict(dtDict)            
            self.plus_context['countAfter'] = Wo_priority.objects.all().count()

