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
# pip install paho-mqtt


import json
import uuid

from misc import *
from devnval import *

from paho.mqtt import client as MqttClient


class MqttSettings:
  def __init__(self, settingsDict:dict=None):
    self.hostname:str = None;
    self.port:int = None
    self.topic:str = None
    self.clientId:str = None
    self.username:str = None
    self.password:str = None
    self.caCertsPath:str = None
    self.isHA:bool = None

    if settingsDict is not None:
      if 'hostname' in settingsDict:
        self.hostname = settingsDict['hostname']
      if 'port' in settingsDict:
        self.port = int(settingsDict['port'])
      if 'topic' in settingsDict:
        self.topic = settingsDict['topic']
      if 'clientId' in settingsDict:
        self.clientId = settingsDict['clientId']
      if 'username' in settingsDict:
        self.username = settingsDict['username']
      if 'password' in settingsDict:
        self.password = settingsDict['password']
      if 'caCertsPath' in settingsDict:
        self.caCertsPath = settingsDict['caCertsPath']
      if 'isHA' in settingsDict:
        self.isHA = bool(settingsDict['isHA'])

    if isStringEmpty(self.clientId):
      self.clientId = str(uuid.uuid4())

  def isSet(self) -> bool:
    return ( self.hostname is not None and self.port is not None )


def buildMqttClient(settings:MqttSettings) -> MqttClient.Client :
  client = MqttClient.Client(settings.clientId)
  if settings.username is not None and len(settings.username.strip()) > 0:
    client.username_pw_set(settings.username, settings.password)
  if settings.caCertsPath is not None and len(settings.caCertsPath.strip()) > 0:
    client.tls_set(ca_certs=settings.caCertsPath)
  return client

def declareValues2HAMqtt(client:MqttClient.Client, deviceSettings:DeviceSettings, declareValues:[DeclareValue]):
  type:str = None
  topic:str = None
  payload:str = None
  declareHAValue:DeclareHAValue = None
  for declareValue in declareValues:
    type = declareValue.type if not isStringEmpty(declareValue.type) else 'sensor'
    topic = 'homeassistant/{0}/{1}/{2}/config'.format( \
      type,
      deviceSettings.serial, \
      declareValue.tag
    )
    declareHAValue = DeclareHAValue(deviceSettings, declareValue)
    payload = json.dumps(declareHAValue, cls=JsonEncoder)
    client.publish(topic, payload, qos=0, retain=True)

def declareValues2DefaultMqtt(client:MqttClient.Client, deviceSettings:DeviceSettings, declareValues:[DeclareValue]):
  topic:str = buildValuesTopic(deviceSettings.group, deviceSettings.serial)
  payload:str = None

  payload = json.dumps(deviceSettings, cls=JsonEncoder)
  client.publish('declare/{0}/device'.format(topic), payload, qos=0, retain=True)

  for declareValue in declareValues:
    payload = json.dumps(declareValue, cls=JsonEncoder)
    client.publish('declare/{0}/value/{1}'.format(topic, declareValue.tag), payload, qos=0, retain=True)

def declareValues2Mqtt(deviceSettings:DeviceSettings, mqttSettings:MqttSettings, declareValues:[DeclareValue]) -> bool:
  def onDeclareMqttConnect(client, userdata, flags, rc):
    if rc == 0:
      try:
        if mqttSettings.isHA:
          declareValues2HAMqtt(client, deviceSettings, declareValues)
        else:
          declareValues2DefaultMqtt(client, deviceSettings, declareValues)
      except Exception as excp:
        print('Failed to send declare : ' + str(excp))
      try:
        client.loop_stop()
        client.disconnect()
      except:
        pass
    else:
      print('Failed to connect for declare, return code {0}'.format(rc))
  client = buildMqttClient(mqttSettings)
  client.on_connect = onDeclareMqttConnect
  client.loop_start()
  client.connect(mqttSettings.hostname, mqttSettings.port)
  return True

def _adaptValues2Mqtt(values:object, mqttSettings:MqttSettings) -> list :
  if mqttSettings.isHA:
    state = {}
    attributes = {}
    for attr, value in vars(values).items():
      if not attr.startswith('_') and value is not None:
        if isinstance(value, dict):
          for dictAttr in value:
            lowerDictAttr = dictAttr.lower()
            if 'latitude' in lowerDictAttr:
              attributes['latitude'] = value[dictAttr]
            elif 'longitude' in lowerDictAttr:
              attributes['longitude'] = value[dictAttr]
        elif isinstance(value, bool):
          state[attr] = 'on' if value else 'off'
        else:
          state[attr] = value
      elif attr == '_evLocation' and isinstance(value, dict):
        attributes['latitude'] = value['latitude']
        attributes['longitude'] = value['longitude']
    return [state, attributes]
  else:
    return [values]

def sendValues2Mqtt(values:object, deviceSettings:DeviceSettings, mqttSettings:MqttSettings) -> bool:
  if not deviceSettings.isSet() or not mqttSettings.isSet():
    return False
  def onValuesMqttConnect(client, userdata, flags, rc):
    if rc == 0:
      try:
        adaptValues = _adaptValues2Mqtt(values, mqttSettings)
        if len(adaptValues[0]) > 0:
          client.publish(buildValuesTopic(deviceSettings.group, deviceSettings.serial, TOPIC_STATE if mqttSettings.isHA else None), json.dumps(adaptValues[0], cls=JsonEncoder))
        if len(adaptValues[1]) > 0:
          client.publish(buildValuesTopic(deviceSettings.group, deviceSettings.serial, TOPIC_ATTRIBUTES), json.dumps(adaptValues[1], cls=JsonEncoder))
      except Exception as excp:
        print('Failed to send values : ' + str(excp))
      try:
        client.loop_stop()
        client.disconnect()
      except:
        pass
    else:
      print('Failed to connect for send, return code {0}'.format(rc))
  client = buildMqttClient(mqttSettings)
  client.on_connect = onValuesMqttConnect
  client.loop_start()
  client.connect(mqttSettings.hostname, mqttSettings.port)
  return True
