#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# MIT License
#
# Copyright 2023 KrzDvt
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.#!/usr/bin/env python

#
# Dependencies
#
# pip install flask flask-httpauth


from misc import *

from flask import Flask
from flask_httpauth import HTTPBasicAuth


class HttpApiSettings:
  def __init__(self, settingsDict:dict=None):
    self.host:str = None
    self.port:int = None
    self.users:dict[str, str] = None

    if settingsDict is not None:
      if 'host' in settingsDict:
        self.host = settingsDict['host']
      if 'port' in settingsDict:
        self.port = int(settingsDict['port'])
      if 'users' in settingsDict:
        self.users = settingsDict['users']

  def isSet(self) -> bool:
    return True


def dispHttpApiSettings(settings:HttpApiSettings, tab:str=''):
  print('{0}host={1}'.format(tab, settings.host))
  print('{0}port={1}'.format(tab, settings.port))
  print('{0}{1} user(s)'.format(tab, len(settings.users) if settings.users is not None else 0))

def buildHttpApi(appName:str, settings:HttpApiSettings) -> Flask:
  app:Flask = Flask(appName)
  auth:HTTPBasicAuth = HTTPBasicAuth()

  if settings.users is not None and len(settings.users) > 0:
    @auth.verify_password
    def verify_password(username, password):
      if settings.users is not None and username in settings.users and settings.users[username] == password:
        return username
      else:
        return None
  else:
    @auth.verify_password
    def verify_password(username, password):
      return username

  return app, auth

def runHttpApi(flask:Flask, settings:HttpApiSettings):
  host:str = settings.host if not isStringEmpty(settings.host) else None
  port:int = settings.port
  flask.run(host=host, port=port)