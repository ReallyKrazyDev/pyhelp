
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# MIT License
#
# Copyright 2023 KrzDvt
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.#!/usr/bin/env python


from json import JSONEncoder


#
# Classes
#

class JsonEncoder(JSONEncoder):
  def default(self, o):
    try:
      return o.toDict()
    except:
      return o.__dict__


#
# Methods
#

def isStringEmpty(string:str) -> bool:
  return string is None or len(string.strip()) <= 0

def buildBaseId(group:str, serial:str) -> str:
  return '{0}_{1}'.format(group, serial)

def buildValuesTopic(group:str, serial:str, suffix:str=None) -> str:
  if not isStringEmpty(suffix):
    return '{0}/{1}/{2}'.format(group, serial, suffix)
  else:
    return '{0}/{1}'.format(group, serial)