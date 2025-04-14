from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

class AuthMiddleware(MiddlewareMixin):
    """Middleware"""
    def process_request(self, request):
        if request.path_info == "/login/":
            return

        info_dict = request.session.get("info")
        print(info_dict)
        if info_dict:
            return
        return redirect('/login/')

