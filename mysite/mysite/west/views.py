# -*-coding:utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from models import Character
from django.shortcuts import render
from django.template.context_processors import csrf
from django import forms

# Create your views here.

# def hello(request):
#     return HttpResponse("<p>西餐</p>")
"""
def staff(request):
    staff_list=Character.objects.all()
    staff_str=map(str,staff_list)
    context ={'label':' '.join(staff_str)}
    # return HttpResponse("<p>"+' '.join(staff_str) + "</p>")
    return render(request,'templay.html',context)
"""
def staff(request):
    staff_list = Character.objects.all()
    return render(request, 'templay.html', {'staffs': staff_list})

def templay(request):
    context ={}
    context['label']='Hello World! west templay'
    return render(request,'templay.html',context)

def form(request):
    return render(request,'form.html')

class CharacterForm(forms.Form):
    """存入数据格式的自动转换
    """
    name=forms.CharField(max_length=200)

def investigate(request):
    # if request.GET:
    #     form=CharacterForm(request.GET)  #报错
    form=CharacterForm(request.GET)         #先定义即可

    if request.POST:
        form=CharacterForm(request.POST)  #传入数据格式
        if form.is_valid():
            submitted=form.cleaned_data['name']
            new_record=Character(name=submitted)
            new_record.save()
    ctx={}
    ctx.update(csrf(request))
    all_records=Character.objects.all()
    ctx['staff']=all_records
    ctx['form'] =form   #格式单独写报错 form 未定义先用 先在前面的定义
    return render(request,"investigate.html",ctx)






