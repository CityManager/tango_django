#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import os
from rango.models import Category, Page
import random
import django

__author__ = 'CityManager'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_django.settings')


django.setup()


def populate():
    python_cat = add_cat('python', views=128, likes=64)

    add_page(python_cat, title='Official Python Tutorial',
             url='http://docs.python.org/3/tutorial/')

    add_page(cat=python_cat,
             title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
             title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat("Django", views=64, likes=32)

    add_page(cat=django_cat,
             title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat, title="Django Rocks",
             url="http://www.djangorocks.com/")

    add_page(cat=django_cat, title="How to Tango with Django",
             url="http://www.tangowithdjango.com/")

    frame_cat = add_cat("Other Frameworks", views=32, likes=16)

    add_page(cat=frame_cat, title="Bottle",
             url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat, title="Flask", url="http://flask.pocoo.org")

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

    for p in Page.objects.all():
        p.views = random.randint(0, 200)
        p.save()


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
