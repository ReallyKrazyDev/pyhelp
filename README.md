# Pyhelp

Python Helper tools

This library provides some reusable modules used in other projects

It is tested on a Raspberry Pi 3B running Raspberry Pi OS, and data may be sent in Home Assistant format (it is able to declare itself on Home Assistant)


## List of modules

  - ```misc.py``` : very simple methods (strings, ...) and classes (JSON encoder, ...)
  - ```mqtt.py``` : simplified mqtt client
  - ```httpapi.py``` : integrated http server for API calls
  - ```devnval.py``` : devices and values classes, compatible with Home Assistant over MQTT


## Dependencies

Run those commands to install dependencies of parts of the library
  - to use mqtt client : ```pip install paho-mqtt```
  - to use http api server : ```pip install flask flask-httpauth```