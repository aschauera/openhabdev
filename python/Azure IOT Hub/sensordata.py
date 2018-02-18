#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests

SENSORDATAURL = "https://myopenhab.org/rest/items/{strsensor}/state?$value"
SENSORSURL = "https://myopenhab.org/rest/items/"
AZURETAG = ["group_azure_iot"]

# Handles sensor data


def getsensorvalue(sensorname):
    sensorurl = SENSORDATAURL.format(strsensor=sensorname)
    response = requests.get(sensorurl,
                            auth=('aaschauer@outlook.com', 'o#017Kralerhof'))
    #print("Status Code: " + str(response.status_code), end='\n')
    #print("Value: " + str(response.text), end='\n')
    return str(response.text)


def getallsensors():
    response = requests.get(SENSORSURL, auth=(
        'XXX', 'YYY'))
    json = response.json()
    # Get items tagged with 'AzureIOT'
    azureExposedItems = [x for x in json if set(
        AZURETAG).issubset(set(x['groupNames']))]

    return azureExposedItems


def createiothublistofmessages(items):
    messages = []
    for item in items:
        messages.append(createiothubmessage(item))
    return messages


def createiothubmessage(item):
    return str("{\"deviceId\": \"openhabian\",\"sensor\": \"%s\",\"state\": \"%s\" }" % (item['name'], item['state']))
