from django import forms
from django.forms import ModelForm, Select
from work_order.models import Wo_journal, Wo_completion, Work_order, Wo_instruction, Wo_priority
from accounts.models import Category as CategoryAction
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Field, Row, Column

class work_order_form(ModelForm):

   def clean_tagnumber(self):
      data = self.cleaned_data['tagnumber']
      
      # Remember to always return the cleaned data.
      return data

   def clean_problem(self):
      data = self.cleaned_data['problem']
      
      # Remember to always return the cleaned data.
      return data

   def clean_priority(self):
      data = self.cleaned_data['priority']
      
      # Remember to always return the cleaned data.
      return data

   def clean_dest_section(self):
      data = self.cleaned_data['dest_section']
      
      # Remember to always return the cleaned data.
      return data

   tagnumber = forms.CharField(widget=forms.TextInput())
   problem = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
   def __init__(self, *args, **kwargs):
      #self.user = kwargs.pop('user') #take current user
      super(work_order_form, self).__init__(*args, **kwargs)

      self.helper = FormHelper()
      self.helper.layout = Layout(
         Field('tagnumber', css_class='form-group col-md-2 mb-0'),
         Field('problem', css_class='form-group col-md-4 mb-0'),
         Row(
               Column('priority', css_class='form-group col-md-2 mb-0'),
               Column('dest_section', css_class='form-group col-md-3 mb-0'),
               css_class='form-row'
         ),
         Submit('submit', 'Submit')
      )

   class Meta:
      template_name = 'work_order/WoCompletion_form.html'  # Specify your own template name/location

      model = Work_order
      fields = ['tagnumber',
                  'problem',
                  'priority',
                  'dest_section',
               ]

class WoJournalForm(ModelForm):

   def clean_comment(self):
      data = self.cleaned_data['comment']
      
      # other check logic if needed
      # Remember to always return the cleaned data.
      return data
   
   def clean_action(self):
      data = self.cleaned_data['action']
      
      # other check logic if needed
      # Remember to always return the cleaned data.
      return data

   comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
   def __init__(self, *args, **kwargs):

      self.user = kwargs.pop('user')
      super(WoJournalForm, self).__init__(*args, **kwargs)
      #get actions 
      actDict = {}
      for action in self.user.actions.all():
         actDict[action.pk] = action.name

      # Converting into list of tuple 
      actlist = list(actDict.items()) 
      self.fields['action'].widget = Select(choices=actlist)

      self.helper = FormHelper()
      self.helper.layout = Layout(
         Field('comment', css_class='form-group col-md-4 mb-0'),
         Field('action', css_class='form-group col-md-2 mb-0'),
         Submit('submit', 'Submit')
      )

   class Meta:
      template_name = 'work_order/WoJournal_form.html'  # Specify your own template name/location

      model = Wo_journal
      fields = ['comment',
                  'action']

class WoInstruction_form(ModelForm):

   def clean_instruction(self):
      data = self.cleaned_data['instruction']
      
      # other check logic if needed
      # Remember to always return the cleaned data.
      return data
   
   instruction = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
   def __init__(self, *args, **kwargs):

      self.user = kwargs.pop('user')
      super(WoInstruction_form, self).__init__(*args, **kwargs)
      self.helper = FormHelper()
      self.helper.layout = Layout(
         Field('instruction', css_class='form-group col-md-4 mb-0'),
         Submit('submit', 'Submit')
      )


   class Meta:
      template_name = 'work_order/WoInstruction_form.html'  # Specify your own template name/location

      model = Wo_instruction
      fields = [
         'instruction',
         ]

class WoCompletion_form(ModelForm):

   def clean_status(self):
      data = self.cleaned_data['status']
      
      # Remember to always return the cleaned data.
      return data

   def clean_activity(self):
      data = self.cleaned_data['activity']
      
      # Remember to always return the cleaned data.
      return data

   def clean_manPower(self):
      data = self.cleaned_data['manPower']
      
      # Remember to always return the cleaned data.
      return data

   def clean_duration(self):
      data = self.cleaned_data['duration']
      
      # other check logic if needed
      if data <= 0:
         raise ValidationError(_('Invalid duration - can not zero/minus'))

      # Remember to always return the cleaned data.
      return data

   def clean_material(self):
      data = self.cleaned_data['material']
      
      # Remember to always return the cleaned data.
      return data

   def clean_tool(self):
      data = self.cleaned_data['tool']
      
      # Remember to always return the cleaned data.
      return data

   manPower = forms.CharField(widget=forms.TextInput())
   duration = forms.CharField(widget=forms.TextInput())
   activity = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
   material = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
   tool = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
   def __init__(self, *args, **kwargs):
      self.user = kwargs.pop('user') #take current user
      super(WoCompletion_form, self).__init__(*args, **kwargs)

      #get actions
      actDict = {}
      for action in self.user.actions.all():
         actDict[action.pk] = action.name

      # Converting into list of tuple 
      actlist = list(actDict.items()) 
      self.fields['status'].widget = Select(choices=actlist)

      self.helper = FormHelper()
      self.helper.layout = Layout(
         Row(
            Column('status', css_class='form-group col-md-4 mb-0'),
            Column('manPower', css_class='form-group col-md-4 mb-0'),
            Column('duration', css_class='form-group col-md-4 mb-0'),
            css_class='form-row'
         ),
         Row(
            Column('activity', css_class='form-group col-md-4 mb-0'),
            Column('material', css_class='form-group col-md-4 mb-0'),
            Column('tool', css_class='form-group col-md-4 mb-0'),
            css_class='form-row'
         ),
         Submit('submit', 'Submit')
      )

   class Meta:
      template_name = 'work_order/WoCompletion_form.html'  # Specify your own template name/location

      model = Wo_completion
      fields = [
         'status',
         'manPower',
         'duration',
         'activity',
         'material',
         'tool',
         ]

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class WoSummaryReportForm(forms.Form):

   def clean_start_date(self):
      data = self.cleaned_data['start_date']
      
      # other check logic if needed
      # Remember to always return the cleaned data.
      return data

   def clean_end_date(self):
      data = self.cleaned_data['end_date']
      
      # other check logic if needed
      # Remember to always return the cleaned data. datetime.timedelta(days=30)
      return data

   def clean_wo_status(self):
      data = self.cleaned_data['wo_status']
      
      # other check logic if needed
      # Remember to always return the cleaned data. datetime.timedelta(days=30)
      return data

   start_date = forms.DateField(widget=DateInput())
   end_date = forms.DateField(widget=DateInput())
   wo_category = forms.CharField(widget=forms.TextInput())

   def __init__(self, *args, **kwargs):

      #self.user = kwargs.pop('user')
      super(WoSummaryReportForm, self).__init__(*args, **kwargs)

      catDict = {}
      for cat in CategoryAction.objects.all():
         catDict[cat.name] = cat.name

      #add one more for Incoming
      catDict['Incoming'] = 'Incoming'

      # Converting into list of tuple 
      catlist = list(catDict.items()) 
      self.fields['wo_category'].widget = Select(choices=catlist)

      self.helper = FormHelper()
      self.helper.form_method = 'get'
      self.helper.layout = Layout(
         Row(
            Column('start_date', css_class='form-group col-md-2 mb-0'),
            Column('end_date', css_class='form-group col-md-2 mb-0'),
            css_class='form-row'
         ),
         Field('wo_category', css_class='form-group col-md-2 mb-0'),
         Submit('submit', 'Submit')
      )

class Wo_search_form(forms.Form):

   catDict = {}
   for cat in CategoryAction.objects.all():
      catDict[cat.name] = cat.name

   #add one more for Incoming
   catDict['Incoming'] = 'Incoming'

   # Converting into list of tuple 
   catlist = list(catDict.items()) 

   start_date = forms.DateField(widget=DateInput())
   end_date = forms.DateField(widget=DateInput())
   wo_category = forms.CharField(widget=Select(choices=catlist))

   def clean_start_date(self):
      data = self.cleaned_data['start_date']
      
      # other check logic if needed
      # Remember to always return the cleaned data.
      return data

   def clean_end_date(self):
      data = self.cleaned_data['end_date']
      
      # other check logic if needed
      # Remember to always return the cleaned data. datetime.timedelta(days=30)
      return data

   def clean_wo_status(self):
      data = self.cleaned_data['wo_status']
      
      # other check logic if needed
      # Remember to always return the cleaned data. datetime.timedelta(days=30)
      return data

   class Meta:
      template_name = 'work_order/user_work_order_list.html'  # Specify your own template name/location
      model = Work_order

class WoReportForm(forms.Form):

    class Meta:
        template_name = 'work_order/WoReport_form.html'  # Specify your own template name/location
