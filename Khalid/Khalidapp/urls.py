from django.urls import path     
from .import views
urlpatterns = [
    path('', views.index),	   
    path('register',views.register),
    path('success',views.success),
    path('login',views.login),
    path('shows/new', views.newShow),
    path('shows/shows', views.shows),
    path('shows', views.allTvshows),
    path('delete/<int:id>', views.delete),
    path('update/<int:id>', views.update),
    path('updateinfo/<int:id>', views.updateinfo),
    path('show/<int:id>', views.show),
    path('like/<int:id>', views.like),
    path('unlike/<int:id>', views.unlike),
    path('logout', views.logout),


]
