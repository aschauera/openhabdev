#!/usr/bin/env python
# -*- coding: utf8 -*-
import requests	
def set_item(itemName,value):
	r = requests.get("http://192.168.1.5:8081/CMD?"+itemName+"="+value)
	
def get_item(itemName):
	r = requests.get("http://192.168.1.5:8081/rest/items/"+itemName+"/state")
	return r
	
def activate_alarm():
	set_item("Present","OFF")
		
def de_activate_alarm():
	set_item("Present","ON")