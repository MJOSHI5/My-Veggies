from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

#path('register', views.register),
def register(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            safe_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = safe_pw,
            )

            request.session['user_id'] = user.id
        return redirect('/success')

    return redirect('/')
    

#path('login', views.login),
def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])
        if len(user) > 0:
            user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/success')
        
    messages.error(request, "Email or password is incorrect!")
    return redirect('/')


#path('success', views.success),
def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to login/register buddy!")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    all_veggies = Veggie.objects.all()
    context = {
        'user':user,
        'all_veggies':all_veggies,
    }

    return render(request, 'success.html', context)

def add_veggie(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session['user_id'])
        veggies = Veggie.objects.create(
            kind = request.POST['veggie'],
            user_uploader = user,
        )

        #user.user_likes.add(veggies)#User likes related name for likes
        #likes = models.ManyToManyField(User, related_name = 'user_likes')
    return redirect('/success')


#path('show/<int:veggie_id>/likes', views.likes ),
def add_likes(request, veggie_id):
    user = User.objects.get(id=request.session['user_id'])
    veggies = Veggie.objects.get(id=veggie_id)
    user.user_likes.add(veggies) 
    #user.user_likes.add(veggies) User likes related name for likes likes = models.ManyToManyField(User, related_name = 'user_likes')

    #Example from fav books
        #user.favorited_books.add(book) 
        #favorited_by = models.ManyToManyField(User, related_name="favorited_books")
    return redirect(f'/show/likes/{veggie_id}')

#path('show/likes', views.show_likes),
def show_likes(request, veggie_id):
    user = User.objects.get(id=request.session['user_id'])
    veggies = Veggie.objects.get(id=veggie_id)
    context = {
        'user':user,
        'veggies':veggies,
        'likes':veggies,
    }
    return render(request, 'likes.html', context)

#path('show/<int:veggie_id>/un_likes', views.un_likes),
def un_likes(request, veggie_id):
    user = User.objects.get(id=request.session['user_id'])
    veggies = Veggie.objects.get(id=veggie_id)
    user.user_likes.remove(veggies)
    return redirect(f'/show/likes/{veggie_id}')
    
#path('show/<int:veggie_id>', views.single_veggie),
def single_veggie(request, veggie_id):
    user = User.objects.get(id=request.session['user_id'])
    veggie = Veggie.objects.get(id=veggie_id)
    context = {
        'user':user,
        'veggie':veggie,
    }
    return render(request, 'single_veggie.html', context)

#path('veggies/<int:veggie_id>/edit', views.edit),
def edit(request, veggie_id):
    
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'veggie':Veggie.objects.get(id=veggie_id),
        'edit':Veggie.objects.get(id=veggie_id)
    }
    return render(request, 'edit.html', context)


#path('edit-form/<int:veggie_id', views.edit_form),
def edit_form(request, veggie_id):
    if request.method == "POST":
        to_edit = Veggie.objects.get(id=veggie_id)
        if to_edit.user_uploader.id == request.session['user_id']:
            
            to_edit.kind = request.POST['veggie']
            to_edit.save()
        
        return redirect(f'/show/{veggie_id}')

#path('veggies/<int:veggie_id>', views.delete),
def delete(request, veggie_id):
    to_delete = Veggie.objects.get(id=veggie_id)
    if to_delete.user_uploader.id == request.session['user_id']:
    
        to_delete.delete()
    return redirect('/success')


def logout(request):
    request.session.flush()
    return redirect('/')