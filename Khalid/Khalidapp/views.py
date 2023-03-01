from django.shortcuts import redirect, render, HttpResponse
from .models import User,TvShows
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'login.html')


def register(request):
    users = User.objects.all()
    errors = User.objects.basic_validator(request.POST)
    for user in users:
        if (user.email == request.POST['email']):
            errors['email'] = "This email already exist"
    if (len(errors) > 0):
        for key, Value in errors.items():
            messages.error(request, Value)
            return redirect('/')
    else:
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=firstname,
                            last_name=lastname, email=email, password=pw_hash)
        request.session['first_name'] = User.objects.last().first_name
        request.session['userid'] = User.objects.last().id

        return redirect('/shows')


def success(request):

    return render(request, 'success.html')


def login(request):
    login_user = User.objects.filter(email=request.POST['email1'])
    if login_user:
        logged_user = login_user[0]
        if (bcrypt.checkpw(request.POST['password1'].encode(), logged_user.password.encode())):
            request.session['userid'] = logged_user.id
            request.session['email'] = logged_user.email
            request.session['first_name'] = logged_user.first_name
            messages.success(request, "login successful!")
            return redirect('/shows')
        messages.error(request, "invaled password")
        return redirect('/')
    messages.error(request, "invalid user")
    return redirect("/")


def newShow(request):
    return render(request, 'newShow.html')

def updateShow(request):
    return render(request, 'updateShow.html')


def shows(request):
    errors = TvShows.objects.basic_validator(request.POST)
    if (len(errors) > 0):
        for key, Value in errors.items():
            messages.error(request, Value)
            return redirect('/shows/new')
    else:
        title = request.POST['title']
        network = request.POST['network']
        date = request.POST['date']
        desc = request.POST['desc']
        thisUser=User.objects.last()
        obj=TvShows.objects.create(title=title,
                            network=network, date=date, desc=desc,like=thisUser)
        
        return redirect('/shows')


def allTvshows(request):
     all=TvShows.objects.all()
     count=0
     for i in all:
         if i.likeFlag==False:
             count+=1
     context={
         'datas':all,
         'count':count,
     }

     return render(request, 'allTvshows.html',context)


def delete(request,id):
    tvShow=TvShows.objects.get(id=int(id))
    tvShow.delete()
    return redirect('/shows')

def update(request,id):
    tvShow=TvShows.objects.get(id=int(id))
    context={
         'data':tvShow,
     }
    return render(request,'updateShow.html',context)

def updateinfo(request,id):
    tvShow=TvShows.objects.get(id=int(id))
    tvShow.title = request.POST['title']
    tvShow.network = request.POST['network']
    tvShow.date = request.POST['date']
    tvShow.desc = request.POST['desc']
    tvShow.save()
    messages.success(request,"Update Complete")
    return redirect('/shows')

def show(request,id):
    tvShow=TvShows.objects.get(id=int(id))
    context={'data':tvShow}
    return render(request,'tvShowDetail.html',context)


def like(request,id):
    tvShow=TvShows.objects.get(id=int(id))
    tvShow.likeCount=1
    tvShow.likeFlag=False
    tvShow.save()
    return redirect('/shows')

def unlike(request,id):
    tvShow=TvShows.objects.get(id=int(id))
    tvShow.likeCount=0
    tvShow.likeFlag=True
    tvShow.save()
    return redirect('/shows')

def logout(request):
    del request.session['userid']
    return redirect('/')