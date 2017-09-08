from django.conf import settings
from django.utils.module_loading import import_module
from django import template
from django.template.base import Node
from operator import itemgetter
from django.template.defaultfilters import stringfilter
from django.template import Context
from Startseite.views import sysstatus
import json

register = template.Library()


# Genus > {{ value|genus:"maskulin,feminin,neutrum" }} Als Value wird 'm' oder 'f' erwartet sonst wird das Neutrum verwendet.
@register.filter(name='genus')
def genus(value,arg):
	if value=='m':
		return arg.split(',')[0]
	if value=='f':
		return arg.split(',')[1]
	return arg.split(',')[2]

# formatDuration > {{ value|DurationField }} -> 00:00:00.000000
@register.filter(name='formatDuration')
def formatDuration(value):
	total_seconds = int(value.total_seconds())
	hours = total_seconds // 3600
	minutes = (total_seconds % 3600) // 60
	seconds = (total_seconds % 60) + value.total_seconds()-total_seconds
	return '{:02d}:{:02d}:{:09.6f}'.format(hours, minutes, seconds)

# toJson > {{ value|toJson }}
@register.filter(name='toJson')
def toJson(value):
	return json.dumps(value)

@register.filter(name='kategorienListeFilterFX')
def kategorienListeFilterFX(value):
	from django.apps import apps
	import re
	try:
		print(value)
		amodel = apps.get_model(value['app'], value['table'])
		aRet = []
		for aentry in amodel.objects.all():
			def repl(m):
				try:
					return str(getattr(aentry,m.group(1)))
				except:
					return '!err'
			aRet.append({'title':re.sub(r"!(\w+)", repl, value['title']),'val':re.sub(r"!(\w+)", repl, value['val'])})
		return aRet
	except Exception as e:
		print(e)
		return

# Navbar erstellen #
@register.assignment_tag(takes_context=True)
def navbarMaker(context):
	anavbar = []
	for value in settings.INSTALLED_APPS: # Alle Installierten Apps durchgehen und nach navbar.py suchen.
		try:
			anavbar.extend(import_module("%s.navbar" % value).navbar(context.request))
		except ImportError:
			pass
	return sorted(anavbar,key=itemgetter('sort'))

# Systemstatus #
@register.assignment_tag(takes_context=True)
def getSysStatus(context):
	asysstatus = sysstatus(context.request)
	asysstatus['json'] = json.dumps(asysstatus)
	return asysstatus

@register.assignment_tag
def to_list(*args):
	return args

@register.assignment_tag
def add_to_list(alist,add):
	if alist:
		return alist + [add]
	else:
		return [add]

@register.simple_tag
def getFeldVal(alist,val):
	if alist:
		for aDict in alist:
			if 'name' in aDict and aDict['name'] == val:
				if 'value' in aDict:
					return aDict['value']
				else:
					return
	return

@register.simple_tag
def obj_getattr(aobj,val):
	def pObj_getattr(aobj,val):
		if 'all()' in val:	# Der "all()" Teil ist Expermintell! Ungetestet!
			bAll,pAll = val.split('all()',1)
			if pAll[:2] == '__':
				pAll = pAll[2:]
			if bAll[-2:] == '__':
				bAll = bAll[:-2]
			aData = []
			for aktObj in pObj_getattr(aobj,bAll).all():
				aData.append(pObj_getattr(aktObj,pAll))
			return aData
		if '__' in val:
			avals = val.split('__')
		else:
			avals = [val]
		for aval in avals:
			if '()' in aval:
				aobj = getattr(aobj,aval[:-2])()
			else:
				aobj = getattr(aobj,aval)
		return aobj
	try:
		return pObj_getattr(aobj,val)
	except Exception as e:
		# print(e)
		# print(aobj)
		# print(dir(aobj))
		return ''

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag(takes_context=True)
def render(context,value):
	return template.engines['django'].from_string(value).render(context)

# settings value
@register.simple_tag
def settings_value(name):
    if name in getattr(settings, 'ALLOWED_SETTINGS_IN_TEMPLATES', ''):
        return getattr(settings, name, '')
    return ''
