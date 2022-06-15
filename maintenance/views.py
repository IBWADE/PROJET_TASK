from asyncio import tasks
from django.shortcuts import render,redirect,get_object_or_404
from comptes.models import *
from maintenance.models import *
from django.contrib import messages
from django.contrib.auth import logout,login
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import date
from .filters import MaintenanceFilter
from projet_task.utils import render_to_pdf 
from django.http import HttpResponse

# Create your views here.

@login_required
def edit_task(request,id):
    task = get_object_or_404(maintenance,id=id)
    mytypetasks = TypeTasks.objects.all()
    mytypeactivities = TypeActivities.objects.all()
    adminSite = False
    profil = Profil.objects.get(user=request.user)
    if profil.profile == "Quality Manager":
        adminSite = True
    if request.method == "POST":
        date = request.POST['date']
        operation = request.POST['operation']
        time = request.POST['time']
        location = request.POST['location']
        privilege = request.POST['privilege']
        actype = request.POST['actype']
        acregistration = request.POST['acregistration']
        maintenanceref = request.POST['maintenanceref']
        remark = request.POST['remark']
        typemaintenance = request.POST['typemaintenance']
        ata = request.POST['ata']
        typetaskschecked = request.POST.getlist('tasktype')
        typeactivitieschecked = request.POST.getlist('activitytype')

        task.operation = operation
        task.date = date
        task.time = time
        task.location = location
        task.privilege = privilege
        task.actype = actype
        task.acregistration = acregistration
        task.maintenanceref = maintenanceref
        task.remark = remark
        task.ata = ata
        task.typemaintenance = typemaintenance
        for tc in typetaskschecked:
            mytc = TypeTasks.objects.get(pk=tc)
            if task.tasktype.filter(id=tc).exists():
                pass
            else:
                task.tasktype.add(mytc)
            newmaint.save()
        for ac in typeactivitieschecked:
            myac = TypeActivities.objects.get(pk=ac)
            if task.activitytype.filter(id=ac).exists():
                pass
            else:
                task.activitytype.add(myac)
            newmaint.save()
        task.save()
        messages.success(request,"Successful, task edited !")
        return redirect('manage')
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'task':task,
        'mytypetasks':mytypetasks,
        'mytypeactivities':mytypeactivities

    }
    return render(request,'maintenance/edit_task.html',context)


@login_required
def single_user(request,id):
    query = request.GET.get('q')
    single_profil = get_object_or_404(Profil,id=id)
    user = single_profil.user
    tasks_all = maintenance.objects.filter(technicalrecorder=user)
    tasks_list = maintenance.objects.filter(technicalrecorder=user).order_by('-id')
    datefrom = request.GET.get('from')
    dateto = request.GET.get('to')  

    if dateto and datefrom:
        tasks_list = maintenance.objects.filter(date__lte=dateto,date__gte=datefrom,technicalrecorder=user)
        
    if query:
        tasks_list = maintenance.objects.filter(
            Q(location__icontains=query)|
            Q(operation__icontains=query)|
            Q(date__startswith=query)|
            Q(ata__icontains=query)|
            Q(privilege__icontains=query)|
            Q(actype__icontains=query)|
            Q(acregistration__icontains=query)|
            Q(technicalrecorder__username__startswith=query)|
            Q(maintenanceref__icontains=query)|
            Q(typemaintenance__icontains=query)
    )
    paginator = Paginator(tasks_list,10)
    page = request.GET.get('page')
    try: 
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 15
    else:
        (start_index, end_index) = proper_paginator(tasks, index=8)
    
    page_range = list(paginator.page_range)[start_index:end_index]

    adminSite = False
    profil = get_object_or_404(Profil,user=request.user)
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'adminSite':adminSite,
        'tasks':tasks,
        'profil':profil,
        'user':user,
        'page_range':page_range,
        'tasks_all':tasks_all,
        'single_profil':single_profil,
    }
    return render(request,'maintenance/single-user.html',context)

            


@login_required
def single_user_bis(request,id):
        
        single_profil = get_object_or_404(Profil,id=id)
        user = single_profil.user 
       
        tasks_all = maintenance.objects.filter(technicalrecorder=user)  
        tasks_list = maintenance.objects.filter(technicalrecorder=user).order_by('-id')

        Maintenance = user.maintenance_set.all() 

        myFilter = MaintenanceFilter(request.GET, queryset=Maintenance)
        tasks_list = myFilter.qs 
        tasks_all = tasks_list
        
        

        paginator = Paginator(tasks_list,10)
        page = request.GET.get('page')
        try: 
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        if page is None:
            start_index = 0
            end_index = 15
        else:
            (start_index, end_index) = proper_paginator(tasks, index=8)
        
        page_range = list(paginator.page_range)[start_index:end_index]

        adminSite = False
        profil = get_object_or_404(Profil,user=request.user)
        if profil.profile == "Quality Manager":
            adminSite = True
        
        context = {
                    'user':user,
                    'single_profil':single_profil,
                    'Maintenance':Maintenance, 
                    'myFilter':myFilter,
                    'tasks_all':tasks_all,
                    'page_range':page_range,
                    'adminSite':adminSite,
                    'tasks':tasks,
                    'tasks_all':tasks_all
                  } 


           

        return render(request,'maintenance/single-user-bis.html',context)   

                 
                           
             

@login_required
def dashboard(request):
    adminSite = False
    profil = Profil.objects.get(user=request.user)
    users = User.objects.all()
    tasks = maintenance.objects.all()
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'users':users,
        'tasks':tasks
    }
    return render(request,'maintenance/dashboard.html',context)

@login_required
def tasks_gestion(request):
    query = request.GET.get('q')
    profil = Profil.objects.get(user=request.user)
    tasks_list = maintenance.objects.filter(technicalrecorder=request.user).order_by('-id')
    datefrom = request.GET.get('from')
    dateto = request.GET.get('to')
    if dateto and datefrom:
        tasks_list = maintenance.objects.filter(date__lte=dateto,date__gte=datefrom,technicalrecorder=request.user)
    if query:
        tasks_list = maintenance.objects.filter(
            Q(location__icontains=query)|
            Q(operation__icontains=query)|
            Q(date__startswith=query)|
            Q(ata__icontains=query)|
            Q(privilege__icontains=query)|
            Q(actype__icontains=query)|
            Q(acregistration__icontains=query)|
            Q(technicalrecorder__username__startswith=query)|
            Q(maintenanceref__icontains=query)|
            Q(typemaintenance__icontains=query)
    )
    paginator = Paginator(tasks_list,15)
    page = request.GET.get('page')
    try: 
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 15
    else:
        (start_index, end_index) = proper_paginator(tasks, index=8)
    
    page_range = list(paginator.page_range)[start_index:end_index]

    mytypetasks = TypeTasks.objects.all()
    mytypeactivities = TypeActivities.objects.all()
    if request.method == "POST":
        date = request.POST['date']
        operation = request.POST['operation']
        time = request.POST['time']
        location = request.POST['location']
        privilege = request.POST['privilege']
        actype = request.POST['actype']
        acregistration = request.POST['acregistration']
        maintenanceref = request.POST['maintenanceref']
        remark = request.POST['remark']
        typemaintenance = request.POST['typemaintenance']
        ata = request.POST['ata']
        typetaskschecked = request.POST.getlist('tasktype')
        typeactivitieschecked = request.POST.getlist('activitytype')

        newmaint = maintenance()
        newmaint.date = date
        newmaint.location = location
        newmaint.operation = operation
        newmaint.ata = ata
        newmaint.privilege = privilege
        newmaint.remark = remark
        newmaint.technicalrecorder = request.user
        newmaint.time = time
        newmaint.acregistration = acregistration
        newmaint.actype = actype
        newmaint.maintenanceref = maintenanceref
        newmaint.typemaintenance = typemaintenance
        newmaint.save()
        for tc in typetaskschecked:
            mytc = TypeTasks.objects.get(pk=tc)
            newmaint.tasktype.add(mytc)
            newmaint.save()
        for ac in typeactivitieschecked:
            myac = TypeActivities.objects.get(pk=ac)
            newmaint.activitytype.add(myac)
            newmaint.save()
        newmaint.save()
        return redirect('tasks')
    adminSite = False
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'tasks':tasks,
        'mytypetasks':mytypetasks,
        'mytypeactivities':mytypeactivities,
        'page_range':page_range,
    }
    return render(request,'maintenance/tasks.html',context)

def proper_paginator(tasks, index):
    start_index = 0
    end_index = 15
    if tasks.number > index:
        start_index = tasks.number - index
        end_index = start_index + end_index
    return (start_index, end_index)

@login_required
def user_profil(request):
    adminSite = False
    profil = Profil.objects.get(user=request.user)
    tasks = maintenance.objects.filter(technicalrecorder=request.user)
    user = request.user
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        dateofbirth = request.POST['dateofbirth']
        placeofbirth = request.POST['placeofbirth']
        address = request.POST['address']
        bio = request.POST['bio']
        licensenumber = request.POST['license']

        user.first_name = firstname
        user.last_name = lastname
        user.username = username
        user.email = email
        user.save()
        profil.dateofbirth = dateofbirth
        profil.placeofbirth = placeofbirth
        profil.address = address
        profil.licensenumber = licensenumber
        profil.bio = bio
        try :
            profil.image = request.FILES["image"]
        except :
            print('Pas de photo de profil')
        profil.save()
        messages.success(request,"Successful, profil updated")
        logout(request)
        return redirect('accueil')

    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'tasks':tasks
    }
    return render(request,'maintenance/user_profil.html',context)

@login_required
def delete_user(request,id):
    profil = get_object_or_404(Profil,id=id)
    profil.user.delete()
    messages.success(request,"Successful, User deleted !")
    return redirect('users')

@login_required
def delete_task(request,id):
    task = get_object_or_404(maintenance,id=id)
    task.delete()
    messages.success(request,"Successful, task deleted !")
    return redirect('tasks')

@login_required
def manage_task(request):
    query = request.GET.get('q')
    profil = Profil.objects.get(user=request.user)
    tasks_list = maintenance.objects.all().order_by('-id')
    if request.method == "POST":
        datefrom = request.POST['from']
        dateto = request.POST['to']
        tasks_list = maintenance.objects.filter(date__lte=dateto,date__gte=datefrom).order_by('date')
    if query:
        tasks_list = maintenance.objects.filter(
            Q(location__icontains=query)|
            Q(operation__icontains=query)|
            Q(date__icontains=query)|
            Q(ata__icontains=query)|
            Q(privilege__icontains=query)|
            Q(actype__icontains=query)|
            Q(acregistration__icontains=query)|
            Q(technicalrecorder__username__icontains=query)|
            Q(maintenanceref__icontains=query)|
            Q(typemaintenance__icontains=query)
    )
    paginator = Paginator(tasks_list,10)
    page = request.GET.get('page')
    try : 
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    if page is None:
        start_index = 0
        end_index = 15
    else:
        (start_index, end_index) = proper_paginator(tasks, index=8)
    
    page_range = list(paginator.page_range)[start_index:end_index]
    adminSite = False
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'tasks':tasks,
        'page_range':page_range,
    }
    return render(request,'maintenance/maintenances.html',context)

@login_required
def Users(request):
    query = request.GET.get('q')
    profil = Profil.objects.get(user=request.user)
    profils_list = Profil.objects.all().order_by('-id')
    if query:
        profils_list = Profil.objects.filter(
            Q(licensenumber__icontains=query)|
            Q(user__username__startswith=query)|
            Q(user__email__startswith=query)|
            Q(user__last_name__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(profile__icontains=query)
    )
    paginator = Paginator(profils_list,5)
    page = request.GET.get('page')
    try : 
        profils = paginator.page(page)
    except PageNotAnInteger:
        profils = paginator.page(1)
    except EmptyPage:
        profils = paginator.page(paginator.num_pages)
    emai_used = False
    if page is None:
        start_index = 0
        end_index = 15
    else:
        (start_index, end_index) = proper_paginator(profils, index=8)
    
    page_range = list(paginator.page_range)[start_index:end_index]
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        licensenumber = request.POST['licensenumber']
        profile = request.POST['profile']

        newuser = User()
        newuser.first_name = firstname
        newuser.last_name = lastname
        newuser.username = username
        newuser.email = email
        newuser.set_password(password)
        if User.objects.filter(email=email).exists():
            email_used = True
            messages.warning(request,"Email Used")
        else:
            newuser.save()
            newprofil = Profil()
            newprofil.user = newuser
            newprofil.licensenumber = licensenumber
            newprofil.profile = profile
            newprofil.save()
            messages.success(request,"Successful, user added !")
            return redirect('users')
        
    adminSite = False
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'profils':profils,
        'page_range':page_range
    }
    return render(request,'maintenance/users.html',context)


@login_required
def Users_bis(request):
    query = request.GET.get('q')
    profil = Profil.objects.get(user=request.user)
    profils_list = Profil.objects.all().order_by('-id')
    if query:
        profils_list = Profil.objects.filter(
            Q(licensenumber__icontains=query)|
            Q(user__username__startswith=query)|
            Q(user__email__startswith=query)|
            Q(user__last_name__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(profile__icontains=query)
    )
    paginator = Paginator(profils_list,5)
    page = request.GET.get('page')
    try : 
        profils = paginator.page(page)
    except PageNotAnInteger:
        profils = paginator.page(1)
    except EmptyPage:
        profils = paginator.page(paginator.num_pages)
    emai_used = False
    if page is None:
        start_index = 0
        end_index = 15
    else:
        (start_index, end_index) = proper_paginator(profils, index=8)
    
    page_range = list(paginator.page_range)[start_index:end_index]
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        licensenumber = request.POST['licensenumber']
        profile = request.POST['profile']

        newuser = User()
        newuser.first_name = firstname
        newuser.last_name = lastname
        newuser.username = username
        newuser.email = email
        newuser.set_password(password)
        if User.objects.filter(email=email).exists():
            email_used = True
            messages.warning(request,"Email Used")
        else:
            newuser.save()
            newprofil = Profil()
            newprofil.user = newuser
            newprofil.licensenumber = licensenumber
            newprofil.profile = profile
            newprofil.save()
            messages.success(request,"Successful, user added !")
            return redirect('users')
        
    adminSite = False
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'profils':profils,
        'page_range':page_range
    }
    return render(request,'maintenance/users_bis.html',context)    

@login_required
def news(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        post = Post()
        post.title = title
        post.content = content
        post.auteur = request.user
        try :
            post.photo = request.FILES["photo"]
        except :
            print('Pas de photo de profil')
        post.save()
        messages.success(request,"Successful, post added !")
    query = request.GET.get('q')
    profil = Profil.objects.get(user=request.user)
    posts_list = Post.objects.all()
    if query:
        posts_list = Post.objects.filter(
            Q(title__startswith=query)|
            Q(content__icontains=query)|
            Q(auteur__username__icontains=query)
    )
    paginator = Paginator(posts_list,6)
    page = request.GET.get('page')
    try : 
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    adminSite = False
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'posts':posts
    }
    return render(request,'maintenance/news.html',context)

@login_required
def delete_post(request,id):
    post = get_object_or_404(Post,id=id)
    post.delete()
    messages.success(request,"Successful, post deleted !")
    return redirect('news')

@login_required
def detail_post(request,id):
    profil = Profil.objects.get(user=request.user)
    post = get_object_or_404(Post,id=id)
    comments = Comment.objects.filter(post=post).order_by('-id')
    adminSite = False
    if request.method == 'POST':
            comment_content = request.POST["content"]
            comment = Comment()
            comment.user = request.user
            comment.post = post
            comment.comment_content = comment_content
            comment.save()
            messages.success(request,"Successful, comment added !")
    if profil.profile == "Quality Manager":
        adminSite = True
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'post':post,
        'profil':profil,
        'adminSite':adminSite,
        'is_liked':is_liked,
        'comments':comments,
        'total_likes':post.total_likes()
    }
    return render(request,'maintenance/detail_post.html',context)

@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect("detail_post",post_id)

@login_required
def edit_post(request,id):
    profil = Profil.objects.get(user=request.user)
    post = get_object_or_404(Post,id=id)
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        post.title = title
        post.content = content
        post.save()
        messages.success(request,"Successful, post edited !")
        return redirect('news')
    adminSite = False
    if profil.profile == "Quality Manager":
        adminSite = True
    context = {
        'profil':profil,
        'adminSite':adminSite,
        'post':post,
    }
    return render(request,'maintenance/edit_post.html',context)

@login_required
def update_password(request,id):
    user = get_object_or_404(User,id=id)
    password = request.POST.get('password')

    user.set_password(password)
    user.save()

    return redirect('user_profil')


@login_required
def search(request,id): 
    users = User.objects.get(id=id) 
    Maintenance = users.maintenance_set.all()
    
    Typetasks = TypeTasks.objects.all()
    Typeactivities = TypeActivities.objects.all() 
    tasks_list = maintenance.objects.all().order_by('-id')
    profil = Profil.objects.get(user=request.user)

    myFilter = MaintenanceFilter(request.GET, queryset=Maintenance)
    Maintenance=myFilter.qs  
  
    context = {
        'profil':profil,
        
        'tasks':tasks,
      
        'Maintenance':Maintenance,
        'users':users,
        'Typetasks':Typetasks,
        'Typeactivities':Typeactivities,
        'myFilter':myFilter,     
        'tasks_list':tasks_list  
       
    }
    return render(request,'maintenance/search.html',context)






