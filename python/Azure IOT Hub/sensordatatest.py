# Test get single sensor value
import sensordata
value = sensordata.getsensorvalue("weather_garden_temperature")
print(value,end='\n')

#Test get all OH items
import requests

SENSORSURL = "https://myopenhab.org/rest/items/"
azuretag = ["group_azure_iot"]
response = requests.get(SENSORSURL, auth=('XXX', 'YYY'))
json = response.json()
#Get items tagged with 'AzureIOT'
azureExposedItems = [x for x in json if set(azuretag).issubset(set(x['groupNames']))]

for item in azureExposedItems:
    print("{\"deviceId\": \"openhabian\",\"sensor\": \"%s\",\"state\": \"%s\" }" % (item['name'], item['state']))
    # print("Name: " + item['name'])
    # print("State: " + item['state'])
