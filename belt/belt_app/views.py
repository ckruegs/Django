from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager, Quote, QuoteManager
from django.contrib import messages
import bcrypt
from datetime import datetime

# Create your views here.
def index(request):
    for user in User.objects.all():
        print(user.password)
    context = {
        "all_users": User.objects.all(),
    }
    return render(request, 'index.html', context)

def process_user(request):
    validation_messages = User.objects.user_validator(request.POST)
    if len(validation_messages) > 0:
        for key, msg in validation_messages.items():
            messages.error(request, msg)
        return redirect('/')
    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        email=request.POST['email'],
        password=hashed,
    )
    request.session['logged_in_user'] = new_user.id
    return redirect('/dashboard')

def dashboard(request):
    print(request.session)
    if 'logged_in_user' not in request.session:
        return redirect('/')
    my_user = User.objects.get(id=request.session['logged_in_user'])
    context = {
        'logged_in_user': my_user,
        "all_users": User.objects.all(),
        'my_quotes': Quote.objects.all(),
    }
    return render(request, 'dashboard.html', context)

def login_user(request):
    email_users = User.objects.filter(email=request.POST['email'])
    if len(email_users) < 1:
        messages.error(request, 'Email not found.')
        return redirect('/')
    user_to_verify = email_users[0]
    password = request.POST['password']
    if bcrypt.checkpw(password.encode(), user_to_verify.password.encode()):
        request.session['logged_in_user'] = user_to_verify.id
        return redirect('/dashboard')
    messages.error(request, "Password do not match!")
    return redirect('/')

def process_quote(request):
    validation_messages = Quote.objects.quote_validator(request.POST)
    if len(validation_messages) > 0:
        for key, msg in validation_messages.items():
            messages.error(request, msg)
        return redirect('/dashboard')
    my_user = User.objects.get(id=request.session['logged_in_user'])
    Quote.objects.create(
        quotedby = request.POST['quotedby'],
        quotedescription = request.POST['quotedescription'],
        submitter = my_user
    )
    return redirect('/dashboard')

# render page
def quote_edit(request, id):
    my_user = User.objects.get(id=request.session['logged_in_user'])
    context = {
        'logged_in_user': my_user,
        'quote': Quote.objects.get(id=id),
        'my_quotes': Quote.objects.all(),
        "all_users": User.objects.all(),
    }
    return render(request, 'edit.html', context)

# submit button - edit models
def quote_update(request, id):
    my_quote = Quote.objects.get(id=id)
    validation_messages = Quote.objects.quote_validator(request.POST)
    if len(validation_messages) > 0:
        for key, msg in validation_messages.items():
            messages.error(request, msg)
        return redirect(f'/quotes/{my_quote.id}/edit')
    my_quote = Quote.objects.get(id=id)
    my_quote.quotedby = request.POST['quotedby']
    my_quote.quotedescription = request.POST['quotedescription']
    my_quote.save()
    return redirect('/dashboard')

def show_user(request, id):
    my_user = User.objects.get(id=request.session['logged_in_user'])
    context = {
        'logged_in_user': my_user,
        'theuser': User.objects.all(),
        'my_quotes': Quote.objects.all(),
        'quote': Quote.objects.filter(id=id),
    }
    return render(request, 'user.html', context)

def quote_delete(request,id):
    my_quote = Quote.objects.get(id=id)
    my_quote.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')