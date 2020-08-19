from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UserDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'user'
    template_name = 'user_detail.html'
    model = User

# Create your views here.
