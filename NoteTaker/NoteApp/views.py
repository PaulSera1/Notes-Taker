from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, NoteForm
from .models import Note
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# decorator: ajax and post validator for server layer
def ajax_and_post(function):
    def wrapper(request):
        if request.is_ajax and request.method == 'POST':
            return function(request)
        else:
            return JsonResponse({'error': ''}, status=400)
    return wrapper

# home page
def home(request):
    context = {
        'form': NoteForm()
    }
    context['notes'] = Note.objects.filter(author__username=request.user.username)
    return render(request, 'home.html', context)

# server hidden layer, validates ajax Note creation call
@ajax_and_post
def postnote(request):
    form = NoteForm(request.POST)
    if form.is_valid():
        instance = form.save(False)
        instance.author = request.user
        instance.save()
        ser_instance = serializers.serialize('json', [instance])
        loc = ser_instance.rfind("author") + 9
        sub = ser_instance[loc:]
        username = User.objects.filter(pk=int(sub[:sub.find('}')]))[0].username
        return JsonResponse({'instance': ser_instance[:loc] + sub.replace(sub[:sub.find('}')], '"' + username + '"')}, status=200)
    else:
        return JsonResponse({'error': form.errors}, status=400)

# server hidden layer, validates/performs ajax Note deletion call
@csrf_exempt
@ajax_and_post
def deletenote(request):
    note_id = request.POST['note_id']
    Note.objects.get(pk=note_id).delete()
    return JsonResponse({'sup': 'nub'}, status=200)

# signup view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})