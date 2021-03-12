from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    #<form action="/register" method="POST">
    path('register', views.register),
    #<form action="/login" method="POST">
    path('login', views.login),
    #'success.html'
    path('success', views.success),
    #<form action="/add_veggie" method="POST">
    path('add_veggie', views.add_veggie),
    #<a href="/veggies/{{veggie.id}}/edit">Edit</a>
    path('veggies/<int:veggie_id>/edit', views.edit),
    #<a href="/show/{{veggie.id}}">Show</a>
    path('show/<int:veggie_id>', views.single_veggie),
    #<form action="/edit-form/{{veggie.id}}" method="POST">
    path('edit-form/<int:veggie_id>', views.edit_form),
    #<a href="/veggies/{{veggie.id}}/delete">Delete</a>
    path('veggies/<int:veggie_id>/delete', views.delete),
    #<a href="/show/{{veggie.id}}/likes">Likes</a>
    path('show/<int:veggie_id>/likes', views.add_likes ),
    #<a href="/show/{{veggie.id}}/un_likes">Un-likes</a>
    path('show/<int:veggie_id>/un_likes', views.un_likes),
    #return redirect(f'/show/likes{veggie_id}')
    path('show/likes/<int:veggie_id>', views.show_likes),
    #<a href="/logout">Logout</a>
    path('logout', views.logout),
]