#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

from django.shortcuts import render


def home(request):
    return render(request, 'index.html')
