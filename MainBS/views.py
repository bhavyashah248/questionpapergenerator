# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Teacher, Chapter, Type, Question, Subject
from MainBS import BSalgo as bs
import random


# Create your views here.
def index(request):
    return render(request, 'MainBS/login.html', None)


@login_required(login_url="/MainBS")
def BSform(request):
    return render(request, 'MainBS/BSform.html', None)


def Auth(request):
    uname = request.POST.get('username', '')
    pwd = request.POST.get('pwd', '')
    user = authenticate(username=uname, password=pwd)

    if user is not None:

        if user.is_active:
            login(request, user)
            return redirect('Home/', request, None)
    else:
        return redirect('/MainBS')


@login_required(login_url="/MainBS")
def Home(request):
    return render(request, 'MainBS/Home.html', None)


@login_required(login_url="/MainBS")
def lout(request):
    logout(request)
    return render(request, 'MainBS/login.html', None)


@login_required(login_url="/MainBS")
def addq(request):
    teacher = Teacher.objects.get(user=request.user)
    sub = teacher.subject
    typ = Type.objects.filter(subject=sub)
    chap = Chapter.objects.filter(subject=sub)

    return render(request, 'MainBS/addq.html', {'type': typ, 'chapter': chap, 'subject': sub})


@login_required(login_url="/MainBS")
def sub(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        sub = teacher.subject
        chap = str(request.POST.get('chapter', ''))
        type = str(request.POST.get('type', ''))
        # marks = str(request.POST.get('marks', ''))
        quest = str(request.POST.get('question', ''))
        ans = str(request.POST.get('answer', ''))
        # fsub = Subject.objects.get(subject = sub)
        fchap = Chapter.objects.get(name=chap)
        tall = type.split('(')
        tname = tall[0]
        rest = tall[1]
        rest2 = rest.split(')')
        tmarks =rest2[0]
        # print(tname)
        # print(tmarks)
        ftype = Type.objects.get(name=tname, marks=tmarks)
        # print(ftype)
        que = Question(subject=sub, chapter=fchap, type=ftype, question=quest, prob='50', answer=ans)
        que.save()
        return render(request, 'MainBS/success.html', {"result": que})
    except:
        return render(request, 'MainBS/fail.html', None)


@login_required(login_url="/MainBS")
def gen(request):
    teacher = Teacher.objects.get(user=request.user)
    sub = teacher.subject
    typ = Type.objects.filter(subject=sub)
    chap = Chapter.objects.filter(subject=sub)
    return render(request, 'MainBS/gen.html', {"type": typ, 'chapter': chap})



@login_required(login_url="/MainBS")
def result(request):
    typeweight = []
    chapweight = []
    tdata = []
    teacher = Teacher.objects.get(user=request.user)
    sub = teacher.subject
    typ = Type.objects.filter(subject=sub).order_by('-marks')
    chap = Chapter.objects.filter(subject=sub)
    marks = str(request.POST.get('total', ''))
    user_marks = 0
    # count1 = 0
    for each_type in typ:
        typpattern = []
        typpattern.append(each_type)
        temp = str(request.POST.get(each_type.name, ''))
        typpattern.append(temp)
        typpattern.append(each_type.marks)
        user_marks += (int(temp)*int(each_type.marks))
        # count1 += int(temp)
        typeweight.append(typpattern)
    count2 = 0
    for each_type in chap:
        temp = str(request.POST.get(each_type.name, ''))
        count2 += int(temp)
        chapweight.append(int(temp))

    # print("Count1 = ",int(count1),"  count2 = ",int(count2),"  marks = ",marks,"  usermarks = ",user_marks)
    if int(marks) == int(count2) and int(marks) == int(user_marks):
        result = bs.algo(marks=marks, typePattern=typeweight, chapPattern=chapweight, sub=sub, tchapters=chap)
        tdata.append(marks)
        tdata.append(typeweight)
        tdata.append(chapweight)

        return render(request, 'MainBS/result.html', {"result": result})
    else:
        teacher = Teacher.objects.get(user=request.user)
        sub = teacher.subject
        typ = Type.objects.filter(subject=sub)
        chap = Chapter.objects.filter(subject=sub)
        return render(request, 'MainBS/genFail.html', {"type": typ, 'chapter': chap})


def populate(request):
    teacher = Teacher.objects.get(user=request.user)
    sub = teacher.subject
    # fsub = Subject.objects.filter(subject = sub)
    fchap = Chapter.objects.filter(subject = sub)
    ftype = Type.objects.filter(subject = sub)
    for each1 in fchap:
        for each in ftype:
            string = "for Subject "+ str(sub) + " of " + str(each1) + " Chapter and of " + str(each) + " Type."
            que = Question(subject=sub, chapter=each1, type=each, question="Question " + string, prob=random.randint(1,100), answer="Answer "+ string)
            que.save()

    return render(request, 'MainBS/success.html', None)
