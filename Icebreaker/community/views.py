from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import GroupTable, MemberTable, CommentTable, UpdateTable
from datetime import datetime



def login_procedure(request):
    if request.user.is_authenticated:
        return redirect('/')


    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'registration/login.html',{'error1':'both fields are required'})
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/login.html', {'error1': 'invalid information'})
    else:
        return render(request, 'registration/login.html',{})





def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):

            # create user
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)

            login(request, user)
            return HttpResponseRedirect('/')

        else:
            return render(request, 'registration/register.html', {})

    else:
        return render(request, 'registration/register.html', {})



def home(request):
    log = 0
    if request.user.is_authenticated:
        log = 1

    return render(request, 'community/home.html', {'log':log})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def view_community(request):
    info = GroupTable.objects.all()
    return render(request, 'community/view-community.html', {'info':info})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def make_group(request):
    if request.method == 'POST':
        title = request.POST['title']
        type = request.POST['type']
        lat = request.POST['lat']
        lon = request.POST['lon']
        date = request.POST['date']
        address = request.POST['address']


        s = GroupTable(title=title, date=date, lat=lat, lon=lon,type=type, number=0, founder=request.user, address=address)
        s.save()
        return HttpResponseRedirect('/community/my-group/')


    else:
        return render(request, 'community/make-group.html', {})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def page_not_found(request):
    return render(request, 'community/nopage.html', {})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def my_group(request):
    if request.method == 'POST':
        content = GroupTable.objects.filter(founder=request.user)
        count = content.count()
        usr = request.user
        if 'checks[]' in request.POST:

            checks = request.POST.getlist('checks[]')
            for c in checks:
                c1 = int(c)
                GroupTable.objects.filter(pk=c1).delete()

                return render(request, 'community/my-group.html', {'content': content, 'usr': usr, 'count':count})

        else:

            return render(request, 'community/my-group.html', {'content': content, 'usr': usr, 'count':count})

    else:
        content=GroupTable.objects.filter(founder=request.user)
        count = content.count()
        usr = request.user
        return render(request, 'community/my-group.html', {'content':content, 'usr':usr,'count':count})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def joined_group(request):
    content = MemberTable.objects.filter(
        user=request.user
    ).only("group")
    return render(request, 'community/joined-group.html', {'content':content})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def update_detail(request, u_id):

    group = GroupTable.objects.filter(pk=u_id)
    if group.count() == 0:
        return render(request, 'community/nopage.html', {})
    group = GroupTable.objects.get(pk=u_id)
    if group.founder!= request.user:
        return render(request, 'community/nopage.html', {})

    content = UpdateTable.objects.filter(group=group)
    c = content.count()

    if request.method == 'POST':
        update = request.POST['update']
        if update=='':
            pass
            #return render(request, 'community/update-detail.html', {'content': content, 'group': group, 'c': c})
        else:
            u = UpdateTable(update=update, group=group)
            u.save()
            #return redirect('update_detail')
            content = UpdateTable.objects.filter(group=group)
        return render(request, 'community/update-detail.html', {'content': content, 'group': group, 'c': c})
    else:

        return render(request, 'community/update-detail.html', {'content':content, 'group':group, 'c':c})



@login_required(login_url="http://127.0.0.1:8000/register/login/")
def group_detail(request, g_id):
    content = GroupTable.objects.filter(pk=g_id)
    if request.method == 'POST':
        #comment
        if 'choice' in request.POST:
            choice = request.POST['choice']
            group = GroupTable.objects.get(pk=g_id)
            comments = CommentTable.objects.filter(group=group)
            if choice == "yes":
                #group = GroupTable.objects.get(pk=g_id)
                joined =MemberTable.objects.filter(user=request.user, group=group)
                if joined.count()==0:  #not joined
                    join = MemberTable(user=request.user, group=group)
                    join.save()     #joined
                    group.number = group.number+1
                    group.save()
                    return render(request, 'community/group-detail.html', {'content': content, 'message':'you have joined', 'comments':comments})
                else:
                    return render(request, 'community/group-detail.html', {'content': content, 'message':'you have already joined', 'comments':comments})
            else: #clicked no
                #group=GroupTable.objects.get(pk=g_id)
                joined =MemberTable.objects.filter(user=request.user, group=group)
                if joined.count()>0:  #joined
                    joined.delete()
                    group.number = group.number-1
                    group.save()
                    return render(request, 'community/group-detail.html', {'content': content, 'message':'you are out of the group', 'comments':comments})
                else:
                    return render(request, 'community/group-detail.html', {'content': content, 'message':'you never joined the group', 'comments':comments})
        else:
            group = GroupTable.objects.get(pk=g_id)
            comments = CommentTable.objects.filter(group=group)

            comment = request.POST['comment']
            if comment != "":
                c = CommentTable(group=group, comment=comment, user=request.user)
                c.save()
            return render(request, 'community/group-detail.html',
                          {'content': content, 'message': 'you need to select 1 option', 'comments':comments})



    else:
        #print(content.count())
        if content.count()==0:
            return render(request, 'community/nopage.html', {})
       # for con in content:
        #   comments= CommentTable.objects.filter(group=con)[:10]
        group = GroupTable.objects.get(pk=g_id)
        comments = CommentTable.objects.filter(group=group)

        return render(request, 'community/group-detail.html', {'content':content, 'comments':comments})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def group_edit(request, g_id):
    if request.method == 'POST':
        title = request.POST['title']
        type = request.POST['type']
        lat = request.POST['lat']
        lon = request.POST['lon']
        date = request.POST['date']
        address = request.POST['address']

        s = GroupTable.objects.get(pk=g_id)
        s.title=title
        s.type=type
        s.lat=lat
        s.lon=lon
        s.date=date
        s.address=address
        #s = GroupTable(title=title, date=date, lat=lat, lon=lon,type=type, number=0, founder=request.user, address=address)
        s.save()
        return HttpResponseRedirect('/community/group-detail/'+g_id+'/')


    else:
        c=GroupTable.objects.filter(pk=g_id)
        if c.count()==0:
            return render(request, 'community/nopage.html', {})

        else:
            content= GroupTable.objects.get(pk=g_id)
            if content.founder==request.user:
                return render(request, 'community/group-edit.html', {'content':content})
            else:
                return render(request, 'community/nopage.html', {})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def profile_detail(request, u_id):
    #no need for filter and
    usr = User.objects.filter(pk=u_id)
    if usr.count()==0:
        return render(request, 'community/nopage.html', {})
    usr = User.objects.get(pk=u_id)
    if usr == request.user:
        return redirect('my_group')

    content = GroupTable.objects.filter(founder=usr)

    return render(request, 'community/profile.html', {'content':content, 'usr':usr})
