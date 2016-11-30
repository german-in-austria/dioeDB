from django.shortcuts import get_object_or_404 , render_to_response , redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from DB.funktionenDB import formularView

def maske(request):
	info = ''
	error = ''
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	app_name = 'PersonenDB'
	tabelle_name = 'tbl_personen'
	permName = 'personen'
	primärId = 'person'
	aktÜberschrift = 'Person'
	asurl = '/personendb/maske/'
	if not request.user.has_perm(app_name+'.'+permName+'_maskView'):
		return redirect('Startseite:start')
	view_html_input = ''
	edit_html_input = ''

	aufgabenform = [
		{'titel':'Person','app':'PersonenDB','tabelle':'tbl_personen','id':'person','optionen':['einzeln','elementFrameless'],
		 'felder':['+id','nachname','vorname','geb_datum','weiblich','akt_wohnort','straße_hausnr','plz','!fx1','festnetz1','mobil1','mail1','festnetz2','mobil2','mail2'],
		 'feldoptionen':{'nachname':{'label_col':2,'input_col':4},'vorname':{'label_col':2,'input_col':4,'nl':True},'geb_datum':{'label_col':2,'input_col':4},'weiblich':{'label':'Geschlecht','fxtype':{'type':'select','select':[{'title':'k.A.','value':None},{'title':'männlich','value':False},{'title':'weiblich','value':True}]},'label_col':2,'input_col':4,'nl':True},'akt_wohnort':{'label_col':2,'input_col':10,'label':'Wohnort','nl':True},'straße_hausnr':{'label_col':2,'input_col':6,'label':'Straße+Nr'},'plz':{'label_col':1,'input_col':3,'nl':True},'festnetz1':{'label_col':1,'input_col':3,'label':'Telefon&nbsp;1'},'mobil1':{'label_col':1,'input_col':3,'label':'Mobil&nbsp;1'},'mail1':{'label_col':1,'input_col':3,'label':'E&#8209;Mail&nbsp;1','nl':True},'festnetz2':{'label_col':1,'input_col':3,'label':'Telefon&nbsp;2'},'mobil2':{'label_col':1,'input_col':3,'label':'Mobil&nbsp;2'},'mail2':{'label_col':1,'input_col':3,'label':'E&#8209;Mail&nbsp;2','nl':True}},
		  'sub':[
		 	{'titel':'Informant','app':'PersonenDB','tabelle':'tbl_informanten','id':'informant','optionen':['einzeln','elementFrameless'],
		 	 'felder':['+id','|id_person=parent:id','inf_sigle','pretest','geburtsort','inf_ort','kompetenz_d','haeufigkeit_d','kompetenz_s','haeufigkeit_s','akquiriert_am','kontakt_durch'],
			 'feldoptionen':{'inf_sigle':{'label_col':2,'input_col':4,'label':'GWP Sigle'},'pretest':{'label_col':2,'input_col':4,'nl':True},'geburtsort':{'label_col':2,'input_col':4},'inf_ort':{'label_col':2,'input_col':4,'nl':True},'kompetenz_d':{'label_col':2,'input_col':4,'label':'Dialekt&nbsp;Kompetenz'},'haeufigkeit_d':{'label_col':2,'input_col':4,'label':'Dialekt&nbsp;Häufigkeit','nl':True},'kompetenz_s':{'label_col':2,'input_col':4,'label':'Standard&nbsp;Kompetenz'},'haeufigkeit_s':{'label_col':2,'input_col':4,'label':'Standard&nbsp;Häufigkeit','nl':True},'akquiriert_am':{'label_col':2,'input_col':4},'kontakt_durch':{'label_col':2,'input_col':4,'label':'Kontaktper.','nl':True}},
		 	 'sub':[
		 		{'titel':'Wohnorte','app':'PersonenDB','tabelle':'tbl_informant_x_gewohnt_in','filter':{'wer__exact':'informant'},'id':'wohnorte','optionen':['liste'],
		 		 'felder':['+id','|id_informant=parent:id','wer','aufgewachsen','id_ort','plz','von_jahr','bis_jahr','dauer_jahr'],
				 'feldoptionen':{'wer':{'label_col':2,'input_col':4},'aufgewachsen':{'label_col':2,'input_col':4,'nl':True},'id_ort':{'label_col':2,'input_col':4},'plz':{'label_col':2,'input_col':4,'nl':True},'von_jahr':{'label_col':2,'input_col':2},'bis_jahr':{'label_col':2,'input_col':2},'dauer_jahr':{'label_col':2,'input_col':2,'label':'Dauer(Jahre)','nl':True}}},
		 		{'titel':'Familie','app':'PersonenDB','tabelle':'tbl_informant_x_gewohnt_in','exclude':{'wer__exact':'informant'},'id':'wohnorte','optionen':['liste'],
		 		 'felder':['+id','|id_informant=parent:id','wer','aufgewachsen','id_ort','plz','von_jahr','bis_jahr','dauer_jahr'],
				 'feldoptionen':{'wer':{'label_col':2,'input_col':4},'aufgewachsen':{'label_col':2,'input_col':4,'nl':True},'id_ort':{'label_col':2,'input_col':4},'plz':{'label_col':2,'input_col':4,'nl':True},'von_jahr':{'label_col':2,'input_col':2},'bis_jahr':{'label_col':2,'input_col':2},'dauer_jahr':{'label_col':2,'input_col':2,'label':'Dauer(Jahre)','nl':True}}},
		 		{'titel':'Berufe','app':'PersonenDB','tabelle':'inf_ist_beruf','id':'berufe','optionen':['liste'],
		 		 'felder':['+id','|id_informant=parent:id','id_beruf','ist_aktuell','ist_ausbildung','inf_spezifizierung','von_jahr','bis_jahr','dauer_jahr','|reihung=auto:reihung'],
				 'feldoptionen':{'id_beruf':{'label_col':2,'input_col':4},'ist_aktuell':{'label_col':0,'input_col':3},'ist_ausbildung':{'label_col':0,'input_col':3,'nl':True},'inf_spezifizierung':{'label_col':2,'input_col':10,'nl':True},'von_jahr':{'label_col':2,'input_col':2},'bis_jahr':{'label_col':2,'input_col':2},'dauer_jahr':{'label_col':2,'input_col':2,'label':'Dauer(Jahre)','nl':True}}},
		 		{'titel':'Akquise','app':'PersonenDB','tabelle':'tbl_akquise','id':'akquise','optionen':['einzeln','elementFrameless'],
		 	 	 'felder':['+id','|informant_akqu=parent:id','akquise_status','anrufe_weitere','kooparationsbereitschaft','kommentar_zu_inf','wichtige_informationen'],
				 'feldoptionen':{'akquise_status':{'label_col':1,'input_col':2},'anrufe_weitere':{'label_col':0,'input_col':2},'kooparationsbereitschaft':{'label_col':4,'input_col':2,'nl':True}},
				 'sub':[
				 	{'titel':'Kontakt','app':'PersonenDB','tabelle':'tbl_kontaktaufnahmen','id':'kontakt','optionen':['liste'],
			 		 'felder':['+id','|zu_akquise=parent:id','zeit','kontaktart','id_kontaktierender','beschreibung','Text'],
					 'feldoptionen':{'zeit':{'label_col':1,'input_col':3},'kontaktart':{'label_col':1,'input_col':2,'label':'Art'},'id_kontaktierender':{'label_col':2,'input_col':3,'nl':True}}
					},
				 	{'titel':'Termine','app':'PersonenDB','tabelle':'tbl_termine','id':'termine','optionen':['liste'],
			 		 'felder':['+id','|gehörtzu_akquise=parent:id','titel','termin_art','termin_lokalisierung','zu_dbort','termin_beschreibung','zeit_start','zeit_ende','termin_vereinbart_in','color_id'],
					}
				 ],
				 'suboption':['tab']
				 }
		 	 ],
			 'suboption':['tab']
		 	},
		 	{'titel':'Multiplikator','app':'PersonenDB','tabelle':'tbl_multiplikator_für_ort','id':'multiplikator','optionen':['liste'],
		 	 'felder':['+id','|id_person=parent:id','kontakt_ort','plz','kontakt_zu_p','kontakt_zu_m','sonst_info','kon_inf_altgruppe','kommentar_m','inf_bewertung']},
		 	{'titel':'Mitarbeiter','app':'PersonenDB','tabelle':'tbl_mitarbeiter','id':'mitarbeiter','optionen':['liste'],
		 	 'felder':['+id','|id_person=parent:id','funktion','arbeitsort','team']}
		  ],
		  'suboption':['tab']
		}
	]
	return formularView(app_name,tabelle_name,permName,primärId,aktÜberschrift,asurl,aufgabenform,request,info,error)
