from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

APP_THEME =  settings.APP_THEME



@method_decorator(login_required(login_url='/auth/sign-in/'), name='dispatch')
class DashBoardHome(View):
    def get(self, request,*args, **kwargs):
        context = {
            
            'APP_THEME': APP_THEME
        }
        return render(request,'_templates/'+APP_THEME+'layouts/dashboard/dashboard.html', context)