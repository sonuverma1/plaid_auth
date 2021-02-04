from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework.views import APIView


class Signup(APIView):
    def get(self, request):
        form = UserCreationForm(request.POST)
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        # if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home/')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

# class Login(APIView):
