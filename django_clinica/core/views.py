from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from .forms import RegisterForm
from django.views import View

# Create your views here.
#pagina principal

class HomeView(TemplateView):
    template_name= 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context


#pagina de precios y ofertas
class PricingView(TemplateView):
    template_name= 'pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context
    

#registro de usuarios

class RegisterView(View):

    def get(self, request):
        data = {
            'form': RegisterForm()
        }
        return render(request, 'registration/register.html', data)

    def post(self, request):  # Cambiar Post a post
        user_creation_form = RegisterForm(data=request.POST)  # Cambiar Post a POST
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        
        data = {
            'form': user_creation_form
        }
        return render(request, 'registration/register.html', data)
    
    