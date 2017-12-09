from django.shortcuts import redirect

# Verwaltung - Startseite - Übersicht über alle verfügbaren Tabellen
def start(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_verwaltung import view_start
	return view_start(request)

# Verwaltung - Ansicht - Übersicht über Tabelleneinträge mit Option zum bearbeiten
def view(request,app_name,tabelle_name):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_verwaltung import view_view
	return view_view(request,app_name,tabelle_name)

# Verwaltung - Reset id_seq für PostgreSQL
def resetidseq(request,app_name,tabelle_name):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_verwaltung import view_resetidseq
	return view_resetidseq(request,app_name,tabelle_name)

# Suche (OSM)
def search(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dioedb_login')
	from .view_search import view_search
	return view_search(request)

# Dateien
def dateien(request):
	# Ist der User Angemeldet?
	if not request.user.is_authenticated():
		return redirect('dissdb_login')
	if not request.user.has_perm('DB.dateien'):
		return redirect('Startseite:start')
	from .funktionenDateien import view_dateien
	return view_dateien(request)
