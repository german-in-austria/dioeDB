from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from .models import sys_importdatei, user_verzeichnis, group_verzeichnis, user_korpusdb_erhebung

from django import forms
from KorpusDB.models import tbl_erhebungen
from .forms import OrgModelChoiceField

admin.site.register(sys_importdatei)

class UserVerzeichnisInline(admin.StackedInline):
	model = user_verzeichnis
	extra = 0

class UserKorpusDBErhebungsartenForm(forms.ModelForm):
	erhebung = OrgModelChoiceField(queryset=tbl_erhebungen.objects.all())
	class Meta:
		model = tbl_erhebungen
		fields= '__all__'

class UserKorpusDBErhebungsarten(admin.StackedInline):
	model = user_korpusdb_erhebung
	form = UserKorpusDBErhebungsartenForm
	extra = 0

# Define a new User admin
class UserAdmin(BaseUserAdmin):
	inlines = (UserVerzeichnisInline, UserKorpusDBErhebungsarten, )

class GroupVerzeichnisInline(admin.StackedInline):
	model = group_verzeichnis
	extra = 0

# Define a new User admin
class GroupAdmin(BaseGroupAdmin):
	inlines = (GroupVerzeichnisInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Re-register GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
