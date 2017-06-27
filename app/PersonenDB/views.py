from django.shortcuts import get_object_or_404 , render_to_response , redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from DB.funktionenDB import formularView
from django.core.urlresolvers import reverse

def maske(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_personen'
	permName = 'personen'
	primaerId = 'person'
	aktueberschrift = 'Person'
	asurl = '/personendb/maske/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{'titel':'Person','app':'PersonenDB','tabelle':'tbl_personen','id':'person','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','nachname','vorname','geb_datum','weiblich','akt_wohnort','strasse_hausnr','plz','festnetz1','mobil1','mail1','festnetz2','mobil2','mail2'],
		 'feldoptionen':{'nachname':{'label_col':2,'input_col':4},'vorname':{'label_col':2,'input_col':4,'nl':True},'geb_datum':{'label_col':2,'input_col':4},'weiblich':{'label':'Geschlecht','fxtype':{'type':'select','select':[{'title':'k.A.','value':None},{'title':'männlich','value':False},{'title':'weiblich','value':True}]},'label_col':2,'input_col':4,'nl':True},'akt_wohnort':{'label_col':2,'input_col':10,'label':'Wohnort','nl':True},'strasse_hausnr':{'label_col':2,'input_col':6,'label':'Strasse+Nr'},'plz':{'label_col':1,'input_col':3,'nl':True},'festnetz1':{'label_col':1,'input_col':3,'label':'Telefon&nbsp;1'},'mobil1':{'label_col':1,'input_col':3,'label':'Mobil&nbsp;1'},'mail1':{'label_col':1,'input_col':3,'label':'E&#8209;Mail&nbsp;1','nl':True},'festnetz2':{'label_col':1,'input_col':3,'label':'Telefon&nbsp;2'},'mobil2':{'label_col':1,'input_col':3,'label':'Mobil&nbsp;2'},'mail2':{'label_col':1,'input_col':3,'label':'E&#8209;Mail&nbsp;2','nl':True}},
		  'sub':[
		 	{'titel':'Informant','app':'PersonenDB','tabelle':'tbl_informanten','id':'informant','optionen':['einzeln','elementFrameless'],
		 	 'felder':['+id','|id_person=parent:id','inf_sigle','pretest','inf_gruppe','eignung','geburtsort','inf_ort','familienstand','ausserhalbwohnort','ausbildung_max','ausbildung_spez','kompetenz_d','haeufigkeit_d','kompetenz_s','haeufigkeit_s','akquiriert_am','kontakt_durch','kommentar'],
			 'feldoptionen':{'inf_sigle':{'label_col':2,'input_col':4,'label':'GWP Sigle'},'pretest':{'label_col':2,'input_col':4,'nl':True},'inf_gruppe':{'label':'Inf. Gruppe','label_col':2,'input_col':4},'eignung':{'label_col':2,'input_col':4,'nl':True},'geburtsort':{'label_col':2,'input_col':4},'inf_ort':{'label_col':2,'input_col':4,'nl':True},'familienstand':{'label_col':2,'input_col':4},'ausserhalbwohnort':{'label_col':2,'input_col':4,'nl':True},'ausbildung_max':{'label_col':2,'input_col':4},'ausbildung_spez':{'label_col':2,'input_col':4,'nl':True},'kompetenz_d':{'label_col':2,'input_col':4,'label':'Dialekt&nbsp;Kompetenz'},'haeufigkeit_d':{'label_col':2,'input_col':4,'label':'Dialekt&nbsp;Häufigkeit','nl':True},'kompetenz_s':{'label_col':2,'input_col':4,'label':'Standard&nbsp;Kompetenz'},'haeufigkeit_s':{'label_col':2,'input_col':4,'label':'Standard&nbsp;Häufigkeit','nl':True},'akquiriert_am':{'label_col':2,'input_col':4},'kontakt_durch':{'label_col':2,'input_col':4,'label':'Kontaktper.','nl':True},'kommentar':{'label_col':2,'input_col':10,'nl':True}},
		 	 'sub':[
		 		{'titel':'Wohnort','titel_plural':'Wohnorte','app':'PersonenDB','tabelle':'tbl_informant_x_gewohnt_in','filter':{'wer__exact':'informant'},'id':'wohnorte','optionen':['liste'],
		 		 'felder':['+id','|id_informant=parent:id','wer','aufgewachsen','arbeitsort','id_ort','plz','von_jahr','bis_jahr','dauer_jahr','|reihung=auto:reihung'],
				 'feldoptionen':{'wer':{'label_col':2,'input_col':10,'nl':True},'aufgewachsen':{'label_col':2,'input_col':4},'arbeitsort':{'label_col':2,'input_col':4,'nl':True},'id_ort':{'label_col':2,'input_col':4},'plz':{'label_col':2,'input_col':4,'nl':True},'von_jahr':{'label_col':2,'input_col':2},'bis_jahr':{'label_col':2,'input_col':2},'dauer_jahr':{'label_col':2,'input_col':2,'label':'Dauer(Jahre)','nl':True}}},
		 		{'titel':'Familie','app':'PersonenDB','tabelle':'tbl_informant_x_gewohnt_in','exclude':{'wer__exact':'informant'},'id':'wohnorte','optionen':['liste'],
		 		 'felder':['+id','|id_informant=parent:id','wer','aufgewachsen','arbeitsort','id_ort','plz','von_jahr','bis_jahr','dauer_jahr','beziehungsdauer','kompetenz_d','haeufigkeit_d','|reihung=auto:reihung'],
				 'feldoptionen':{'wer':{'label_col':2,'input_col':10,'nl':True},'aufgewachsen':{'label_col':2,'input_col':4},'arbeitsort':{'label_col':2,'input_col':4,'nl':True},'id_ort':{'label_col':2,'input_col':4},'plz':{'label_col':2,'input_col':4,'nl':True},'von_jahr':{'label_col':2,'input_col':2},'bis_jahr':{'label_col':2,'input_col':2},'dauer_jahr':{'label_col':2,'input_col':2,'label':'Dauer(Jahre)','nl':True},'kompetenz_d':{'label_col':2,'input_col':4,'label':'Dialekt&nbsp;Kompetenz'},'haeufigkeit_d':{'label_col':2,'input_col':4,'label':'Dialekt&nbsp;Häufigkeit','nl':True},'beziehungsdauer':{'label_col':10,'input_col':2,'nl':True}}},
		 		{'titel':'Beruf','titel_plural':'Berufe','app':'PersonenDB','tabelle':'inf_ist_beruf','id':'berufe','optionen':['liste'],
		 		 'felder':['+id','|id_informant=parent:id','id_beruf','ist_aktuell','ist_ausbildung','inf_spezifizierung','fahrtdauer','von_jahr','bis_jahr','dauer_jahr','|reihung=auto:reihung'],
				 'feldoptionen':{'id_beruf':{'label_col':2,'input_col':10,'foreignkeytarget':reverse('PersonenDB:berufe'),'nl':True},'ist_aktuell':{'label_col':2,'input_col':4},'ist_ausbildung':{'label_col':2,'input_col':4,'nl':True},'inf_spezifizierung':{'label_col':2,'input_col':4},'fahrtdauer':{'label_col':4,'input_col':2,'nl':True},'von_jahr':{'label_col':2,'input_col':2},'bis_jahr':{'label_col':2,'input_col':2},'dauer_jahr':{'label_col':2,'input_col':2,'label':'Dauer(Jahre)','nl':True}}},
		 		{'titel':'Akquise','app':'PersonenDB','tabelle':'tbl_akquise','id':'akquise','optionen':['einzeln','elementFrameless'],
		 	 	 'felder':['+id','|informant_akqu=parent:id','akquise_status','anrufe_weitere','kooparationsbereitschaft','kommentar_zu_inf','wichtige_informationen'],
				 'feldoptionen':{'akquise_status':{'label_col':1,'input_col':2,'fxtype':{'type':'prozent'}},'anrufe_weitere':{'label_col':0,'input_col':2},'kooparationsbereitschaft':{'label_col':4,'input_col':2,'nl':True}},
				 'sub':[
				 	{'titel':'Kontaktaufnahme','titel_plural':'Kontaktaufnahmen','app':'PersonenDB','tabelle':'tbl_kontaktaufnahmen','id':'kontakt','optionen':['liste'],
			 		 'felder':['+id','|zu_akquise=parent:id','zeit','kontaktart','id_kontaktierender','beschreibung','Text'],
				 	 'elementtitel':'{% load dioeTags %} - <span data-formtitel="zeit">{% getFeldVal aData.felder \'zeit\' %}</span> - <span data-formtitel="kontaktart">{% getFeldVal aData.felder \'kontaktart\' %}</span> - <span data-formtitel="id_kontaktierender">{% getFeldVal aData.felder \'id_kontaktierender\' %}</span>',
					 'feldoptionen':{'zeit':{'label_col':3,'input_col':3},'kontaktart':{'label_col':1,'input_col':3,'nl':True,'label':'Art'},'id_kontaktierender':{'label_col':3,'input_col':9,'nl':True}},
					 'sub':[
				 		{'titel':'Termin','titel_plural':'Termine','app':'PersonenDB','tabelle':'tbl_termine','id':'termine','optionen':['liste','elementeclosed'],
			 		 	 'felder':['+id','|termin_vereinbart_in=parent:id','titel','termin_art','termin_lokalisierung','zu_dbort','termin_beschreibung','zeit_start','zeit_ende','color_id'],
				 	 	 'elementtitel':'{% load dioeTags %} - <span data-formtitel="zeit_start">{% getFeldVal aData.felder \'zeit_start\' %}</span> bis <span data-formtitel="zeit_ende">{% getFeldVal aData.felder \'zeit_ende\' %}</span> - <span data-formtitel="titel">{% getFeldVal aData.felder \'titel\' %}</span>',
	 					 'sub':[
	 				 		{'titel':'Teilnehmer','app':'PersonenDB','tabelle':'tbl_terminteilnehmer','id':'teilnehmer','optionen':['liste','elementeclosed'],
	 			 		 	 'felder':['+id','|zu_termin=parent:id','person','teilnahme_art'],
	 				 	 	 'elementtitel':'{% load dioeTags %} - <span data-formtitel="person">{% getFeldVal aData.felder \'person\' %}</span> - <span data-formtitel="teilnahme_art">{% getFeldVal aData.felder \'teilnahme_art\' %}</span>',
							 }
						 ]
						}
					 ]
					}
				 ],
				 'suboption':['tab']
				 }
		 	 ],
			 'suboption':['tab']
		 	},
		 	{'titel':'Multiplikator','titel_plural':'Multiplikatoren','app':'PersonenDB','tabelle':'tbl_multiplikator_fuer_ort','id':'multiplikator','optionen':['liste'],
		 	 'felder':['+id','|id_person=parent:id','kontakt_ort','plz','kontakt_zu_p','kontakt_zu_m','sonst_info','kon_inf_altgruppe','kommentar_m']},
		 	{'titel':'Mitarbeiter','app':'PersonenDB','tabelle':'tbl_mitarbeiter','id':'mitarbeiter','optionen':['liste'],
		 	 'felder':['+id','|id_person=parent:id','funktion','arbeitsort','team']}
		  ],
		  'suboption':['tab']
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def termine(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_termine'
	permName = 'personen'
	primaerId = 'termine'
	aktueberschrift = 'Termine'
	asurl = '/personendb/termine/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{'titel':'Termin','titel_plural':'Termine','app':'PersonenDB','tabelle':'tbl_termine','id':'termine','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','titel','termin_art','termin_lokalisierung','zu_dbort','termin_beschreibung','zeit_start','zeit_ende','color_id','termin_vereinbart_in'],
		 'elementtitel':'{% load dioeTags %} - <span data-formtitel="zeit_start">{% getFeldVal aData.felder \'zeit_start\' %}</span> bis <span data-formtitel="zeit_ende">{% getFeldVal aData.felder \'zeit_ende\' %}</span> - <span data-formtitel="titel">{% getFeldVal aData.felder \'titel\' %}</span>',
		 'sub':[
	 		{'titel':'Teilnehmer','app':'PersonenDB','tabelle':'tbl_terminteilnehmer','id':'teilnehmer','optionen':['liste','elementeclosed'],
 		 	 'felder':['+id','|zu_termin=parent:id','person','teilnahme_art'],
	 	 	 'elementtitel':'{% load dioeTags %} - <span data-formtitel="person">{% getFeldVal aData.felder \'person\' %}</span> - <span data-formtitel="teilnahme_art">{% getFeldVal aData.felder \'teilnahme_art\' %}</span>',
		 	}
		 ]
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)

def berufe(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_berufe'
	permName = 'personen'
	primaerId = 'berufe'
	aktueberschrift = 'Berufe'
	asurl = '/personendb/berufe/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')

	aufgabenform = [
		{'titel':'Beruf','titel_plural':'Berufe','app':'PersonenDB','tabelle':'tbl_berufe','id':'berufe','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','bezeichnung','berufskategorie','kommunikationsgrad','standardkompetenz']
		}
	]
	return formularView(app_name,tabelle_name,permName,primaerId,aktueberschrift,asurl,aufgabenform,request,info,error)
