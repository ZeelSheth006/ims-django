from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = ['/accounts/login/', '/accounts/register/', '/admin/']

        user = getattr(request, "user", None)

        if request.path not in allowed_urls:
            if user is None or not user.is_authenticated:
                return redirect('/accounts/login/')

        return self.get_response(request)
