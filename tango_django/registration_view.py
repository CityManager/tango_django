#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

from registration.backends.simple.views import RegistrationView

__author__ = 'CityManager'


class MyRegistrationView(RegistrationView):
    def get_success_url(self, request=None, user=None):
        return '/rango/'

