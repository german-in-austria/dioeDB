from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.db import models

# Spezielles ModelChoiceWidget als PopUp fuer kuerzere Ladezeiten
class MyModelChoiceWidget(forms.widgets.Select):
	def __init__(self, attrs=None, choices=(), queryset=None):
		super(MyModelChoiceWidget, self).__init__(attrs)
		self.choices = list(choices)
		self.queryset = queryset
	def render(self, name, value, attrs=None):
		atext = '<span class="grey">Keine Eingabe vorhanden</span>'
		btns = ''
		if value:
			atext = '<span title="PK: '+str(value)+'">'+str(self.queryset.get(pk=value))+'</span>'
			btns+= '<button class="seleobj" data-appname="'+self.queryset.model._meta.app_label+'" data-tabname="'+self.queryset.model.__name__+'" data-obj-pk="'+str(value)+'" title="Element in PopUp auswaehlen"><span class="glyphicon glyphicon-folder-open" aria-hidden="true"></span></button>'
			btns+= '<button class="viewobj" data-appname="'+self.queryset.model._meta.app_label+'" data-tabname="'+self.queryset.model.__name__+'" data-obj-pk="'+str(value)+'" title="Element in PopUp anzeigen"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></button>'
			btns+= '<button class="openobj" data-appname="'+self.queryset.model._meta.app_label+'" data-tabname="'+self.queryset.model.__name__+'" data-obj-pk="'+str(value)+'" title="Element in neuen Fenster anzeigen"><span class="glyphicon glyphicon-new-window" aria-hidden="true"></span></button>'
		else:
			btns+= '<button class="seleobj" data-appname="'+self.queryset.model._meta.app_label+'" data-tabname="'+self.queryset.model.__name__+'" data-obj-pk="0" title="Element in PopUp auswaehlen"><span class="glyphicon glyphicon-folder-open" aria-hidden="true"></span></button>'
			btns+= '<button class="viewobj hidden" data-appname="'+self.queryset.model._meta.app_label+'" data-tabname="'+self.queryset.model.__name__+'" data-obj-pk="0" title="Element in PopUp anzeigen"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></button>'
			btns+= '<button class="openobj hidden" data-appname="'+self.queryset.model._meta.app_label+'" data-tabname="'+self.queryset.model.__name__+'" data-obj-pk="0" title="Element in neuen Fenster anzeigen"><span class="glyphicon glyphicon-new-window" aria-hidden="true"></span></button>'
		return '<div class="form-control-static"><input type="hidden" name="'+str(name)+'" value="'+str(value)+'" data-appname="'+self.queryset.model._meta.app_label+'" data-tabname="'+self.queryset.model.__name__+'" data-required="'+str(self.is_required)+'">'+atext+btns+'</div>'

# Angepasstes "ModelChoiceField" um "queryset" an "MyModelChoiceWidget" zu uebergeben.
class MyModelChoiceField(forms.ModelChoiceField):
	widget = MyModelChoiceWidget
	def __init__(self, queryset, empty_label="---------",
				required=True, widget=None, label=None, initial=None,
				help_text='', to_field_name=None, limit_choices_to=None,
				*args, **kwargs):
		if required and (initial is not None):
			self.empty_label = None
		else:
			self.empty_label = empty_label
		forms.Field.__init__(self, required, widget, label, initial, help_text,
						*args, **kwargs)
		self.queryset = queryset
		self.widget.queryset = queryset
		self.limit_choices_to = limit_choices_to
		self.to_field_name = to_field_name
	def _set_queryset(self, queryset):
		self._queryset = queryset
		self.widget.queryset = queryset
		self.widget.choices = self.choices

forms.ModelChoiceField = MyModelChoiceField

# Vorlage zur erstellung von Formularen anhand des Models
def GetModelForm(amodel, *args, **kwargs):
	class NewModelForm(forms.ModelForm):
		class Meta:
			model = amodel
			fields= '__all__'
		def __init__(self):
			self.helper = FormHelper()
			self.helper.form_tag = False
			self.helper.disable_csrf = True
			self.helper.form_id = 'dbForm'
			self.helper.form_class = 'form-horizontal'
			self.helper.label_class = 'col-sm-3'
			self.helper.field_class = 'col-sm-9'
			self.helper.form_method = 'post'
			self.helper.form_action = ''
			super(NewModelForm, self).__init__(*args, **kwargs)
	return NewModelForm()
