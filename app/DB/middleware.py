from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import sys_user_addon

class SetLastVisitMiddleware(object):
	def process_response(self, request, response):
		if request.user.is_authenticated():
 			sys_user_addon.objects.update_or_create(user=User.objects.get(pk=request.user.pk),defaults={'last_visit':now()})
		return response
