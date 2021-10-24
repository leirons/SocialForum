from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.http import HttpResponse


class CheckIsUserBlocked(MiddlewareMixin):
    def process_request(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.is_blocked and not request.user.is_staff:
                logout(request)
                return HttpResponse("Вы забенены")