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

@register.simple_tag(takes_context=True)
def render(context,value):
	return template.engines['django'].from_string(value).render(context)

# settings value
@register.simple_tag
def settings_value(name):
    if name in getattr(settings, 'ALLOWED_SETTINGS_IN_TEMPLATES', ''):
        return getattr(settings, name, '')
    return ''
