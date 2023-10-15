#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# MIT License
#
# Copyright 2023 KrzDvt
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.#!/usr/bin/env python


from misc import *


#
# Classes
#

class DeviceSettings:
  def __init__(self, settingsDict:dict=None):
    self.group:str = None
    self.serial:str = None
    self.manufacturer:str = None
    self.model:str = None
    self.version:str = None
    self.name:str = None

    if settingsDict is not None:
      if 'group' in settingsDict:
        self.group = settingsDict['group']
      if 'serial' in settingsDict:
        self.serial = settingsDict['serial']
      if 'manufacturer' in settingsDict:
        self.manufacturer = settingsDict['manufacturer']
      if 'model' in settingsDict:
        self.serial = settingsDict['model']
      if 'version' in settingsDict:
        self.version = settingsDict['version']
      if 'name' in settingsDict:
        self.name = settingsDict['name']

  def isSet(self) -> bool:
    return ( \
      not isStringEmpty(self.group) and \
      not isStringEmpty(self.serial) and \
      not isStringEmpty(self.model) and \
      not isStringEmpty(self.name) \
    )

  def toDict(self) -> dict:
    res:dict = {}
    if not isStringEmpty(self.group):
      res['group'] = self.group
    if not isStringEmpty(self.serial):
      res['serial'] = self.serial
    if not isStringEmpty(self.manufacturer):
      res['manufacturer'] = self.manufacturer
    if not isStringEmpty(self.model):
      res['model'] = self.model
    if not isStringEmpty(self.version):
      res['version'] = self.version
    if not isStringEmpty(self.name):
      res['name'] = self.name
    return res

class DeclareValue:
  def __init__(self, name:str, unit:str, tag:str, icon:str=None):
    self.name:str = name.strip() if name is not None else None
    self.unit:str = unit.strip() if unit is not None else None
    self.tag:str = tag.strip() if tag is not None else None
    self.icon:str = icon.strip() if icon is not None else None

  def toDict(self) -> dict:
    res:dict = {}
    if not isStringEmpty(self.name):
      res['name'] = self.name
    if not isStringEmpty(self.unit):
      res['unit'] = self.unit
    if not isStringEmpty(self.tag):
      res['tag'] = self.tag
    if not isStringEmpty(self.icon):
      res['icon'] = self.icon
    return res

class DeclareHADevice:
  def __init__(self, deviceSettings:DeviceSettings):
    self.identifiers:[str] = [buildBaseId(deviceSettings.group, deviceSettings.serial)]
    self.manufacturer:str = deviceSettings.manufacturer
    self.model:str = deviceSettings.model
    self.name:str = deviceSettings.name
    self.sw_version:str = deviceSettings.version

  def toDict(self) -> dict:
    res:dict = {}
    if self.identifiers is not None:
      res['identifiers'] = self.identifiers
    if not isStringEmpty(self.manufacturer):
      res['manufacturer'] = self.manufacturer
    if not isStringEmpty(self.model):
      res['model'] = self.model
    if not isStringEmpty(self.name):
      res['name'] = self.name
    if not isStringEmpty(self.sw_version):
      res['sw_version'] = self.sw_version
    return res

class DeclareHAValue:
  def __init__(self, deviceSettings:DeviceSettings, declareValue:DeclareValue):
    topic:str = buildValuesTopic(deviceSettings.group, deviceSettings.serial)

    icon:str = declareValue.icon
    if isStringEmpty(icon):
      if declareValue.unit == '°C' or declareValue.unit == '°F':
        icon = 'mdi:thermometer'
      elif declareValue.unit == 'kB':
        icon = 'mdi:memory'
      else:
        icon = 'mdi:eye'

    self.device:DeclareHADevice = DeclareHADevice(deviceSettings)
    self.enabled_by_default:bool = True
    self.entity_category:str = 'diagnostic'
    self.icon:str = icon
    self.json_attributes_topic = topic
    self.name = declareValue.name
    self.state_class = 'measurement'
    self.state_topic = topic
    self.unique_id = deviceSettings.serial + '_' + declareValue.tag + '_' + deviceSettings.group
    self.unit_of_measurement = declareValue.unit
    self.value_template = '{{ ' + 'value_json.{0}'.format(declareValue.tag) + ' }}'

  def toDict(self) -> dict:
    res:dict = {}
    if self.device is not None:
      res['device'] = self.device.toDict()
    if self.enabled_by_default is not None:
      res['enabled_by_default'] = self.enabled_by_default
    if not isStringEmpty(self.entity_category):
      res['entity_category'] = self.entity_category
    if not isStringEmpty(self.icon):
      res['icon'] = self.icon
    if not isStringEmpty(self.json_attributes_topic):
      res['json_attributes_topic'] = self.json_attributes_topic
    if not isStringEmpty(self.name):
      res['name'] = self.name
    if not isStringEmpty(self.state_class):
      res['state_class'] = self.state_class
    if not isStringEmpty(self.state_topic):
      res['state_topic'] = self.state_topic
    if not isStringEmpty(self.unique_id):
      res['unique_id'] = self.unique_id
    if not isStringEmpty(self.unit_of_measurement):
      res['unit_of_measurement'] = self.unit_of_measurement
    if not isStringEmpty(self.value_template):
      res['value_template'] = self.value_template
    return res
