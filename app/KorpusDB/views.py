from django.shortcuts import get_object_or_404 , render , render_to_response , redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from django.db.models import Count
from DB.funktionenDB import formularView
import datetime
import json
from .models import sys_presettags
import KorpusDB.models as dbmodels

def aufgabensets(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_aufgabensets'
	permName = 'aufgabensets'
	primaerId = 'aufgabenset'
	aktueberschrift = 'Aufgabensets'
	asurl = '/korpusdb/aufgabensets/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	aufgabenform = [
		{'titel':'Aufgabenset','app':'KorpusDB','tabelle':'tbl_aufgabensets','id':'aufgabenset','optionen':['einzeln'],
		 'felder':['+id','Kuerzel','Name_Aset','Fokus','Art_ASet','Kommentar','zu_Phaenomen','|zusammengestellt_als=aufgabenzusammenstellung:id'],
		 'sub':[
			{'titel':'Aufgaben','app':'KorpusDB','tabelle':'tbl_aufgaben','id':'aufgabe','optionen':['liste'],
			 'felder':['+id','Variante','ist_dialekt','Beschreibung_Aufgabe','|von_ASet=parent:id'],
			 'sub':[
				{'titel':'Antwortmoeglichkeiten','app':'KorpusDB','tabelle':'tbl_antwortmoeglichkeiten','id':'antwortmoeglichkeit','optionen':['liste'],
				 'felder':['+id','Kuerzel','frei','|Reihung=auto:reihung','|zu_Aufgabe=parent:id']},
				{'titel':'Aufgabenfiles','app':'KorpusDB','tabelle':'tbl_aufgabenfiles','id':'aufgabenfiles','optionen':['liste'],
				 'felder':['+id','id_Mediatyp','ist_Anweisung','File_Link','Kommentar','|Reihung=auto:reihung','|id_Aufgabe=parent:id']}
			 ]
			},
			{'titel':'Aufgabenzusammenstellung','app':'KorpusDB','tabelle':'tbl_aufgabenzusammenstellungen','id':'aufgabenzusammenstellung','optionen':['einzeln'],
			 'felder':['+id=parent:zusammengestellt_als','Bezeichnung_AZus','Kommentar','AZusCol'],
			 'sub':[
				{'titel':'Beinhaltete Medientypen','app':'KorpusDB','tabelle':'tbl_azusbeinhaltetmedien','id':'azusbeinhaltetmedien','optionen':['liste'],
				 'felder':['+id','id_Mediatyp','|Reihung=auto:reihung','|id_AZus=parent:id']}
			 ]
			}
		 ]
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def tagsedit(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'KorpusDB'
	tabelle_name = 'tbl_tags'
	permName = 'tags'
	primaerId = 'tags'
	aktueberschrift = 'Tags'
	asurl = '/korpusdb/tagsedit/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{'titel':'Tag','titel_plural':'Tags','app':'KorpusDB','tabelle':'tbl_tags','id':'tags','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','Tag','Tag_lang','zu_Phaenomen','Kommentar','Generation','AReihung'],
 		 'sub':[
	 		{'titel':'Tag Familie - Parent','titel_plural':'Tag Familie - Parents','app':'KorpusDB','tabelle':'tbl_tagfamilie','id':'tagfamilieparents','optionen':['liste','elementeclosed'],
 		 	 'felder':['+id','|id_ChildTag=parent:id','id_ParentTag'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ParentTag">{% getFeldVal aData.felder \'id_ParentTag\' %}</span>',
		 	},
	 		{'titel':'Tag Familie - Child','titel_plural':'Tag Familie - Childs','app':'KorpusDB','tabelle':'tbl_tagfamilie','id':'tagfamiliechilds','optionen':['liste','elementeclosed'],
 		 	 'felder':['+id','|id_ParentTag=parent:id','id_ChildTag'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_ChildTag">{% getFeldVal aData.felder \'id_ChildTag\' %}</span>',
		 	},
	 		{'titel':'Tag Ebene zu Tag','titel_plural':'Tag Ebenen zu Tag','app':'KorpusDB','tabelle':'tbl_tagebenezutag','id':'tagebenezutag','optionen':['liste','elementeclosed'],
 		 	 'felder':['+id','|id_Tag=parent:id','id_TagEbene'],
			 'elementtitel':'{% load dioeTags %} - <span data-formtitel="id_TagEbene">{% getFeldVal aData.felder \'id_TagEbene\' %}</span>',
		 	},
		 ],
		 'suboption':['tab']
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def maske(request,ipk=0,apk=0):
	pass




### Funktionen: ###

def getTagList(Tags,TagPK):
	TagData = []
	if TagPK == None:
		for value in Tags.objects.filter(id_ChildTag=None):
			child=getTagList(Tags,value.pk)
			TagData.append({'model':value,'child':child})
	else:
		for value in Tags.objects.filter(id_ChildTag__id_ParentTag=TagPK):
			child=getTagList(Tags,value.pk)
			TagData.append({'model':value,'child':child})
	return TagData

# getTagFamilie für AntwortenTags
def getTagFamilie(Tags):
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_Tag.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen-=1
				pClose+=1
				del afam[-1]
		except:
			pass
		#print(''.rjust(aGen,'-')+'|'+str(value.id_Tag.Tag)+' ('+str(value.id_Tag.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag':value,'aGen':aGen,'pClose':pClose, 'pChilds':value.id_Tag.id_ParentTag.all().count()})
		afam.append(value.id_Tag)
		aGen+=1
	return oTags
# getTagFamilie für PresetTags
def getTagFamiliePT(Tags):
	afam = []
	aGen = 0
	oTags = []
	for value in Tags:
		pClose = 0
		try:
			while not value.id_ChildTag.filter(id_ParentTag=afam[-1].pk):
				aGen-=1
				pClose+=1
				del afam[-1]
		except:
			pass
		#print(''.rjust(aGen,'-')+'|'+str(value.Tag)+' ('+str(value.pk)+' | '+str([val.pk for val in afam])+' | '+str(aGen)+' | '+str(pClose)+')')
		oTags.append({'aTag':value,'aGen':aGen,'pClose':pClose, 'pChilds':value.id_ParentTag.all().count()})
		afam.append(value)
		aGen+=1
	return oTags
