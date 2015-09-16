#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django import template
from rango.models import Category

__author__ = 'CityManager'


register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all()[:10], 'act_cat': cat}
