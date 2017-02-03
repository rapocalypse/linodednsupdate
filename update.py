#!/usr/bin/pyhton3

from json import load
from urllib.parse import urlencode
from urllib.request import urlretrieve

# Frist thing you should to is generate an API Key, on your profile, copy it and paste below
ApiKey		= ""

# You can get the ResourceID by creating a new A zone and after saving clicking on the edit link.
# On the url the ResourceID will be shown. Copy it and paste below
ResourceID 	= ""

# Use this CURL call to get your Domain ID: https://api.linode.com/?api_key={api_key}&api_action=domain.list
# Remeber to replace the above {api_key} with the one you pasted on ApiKey variable above.
DomainID 	= ""

# No need to change anything below this line

Api 		= "https://api.linode.com/api/?api_key={0}&resultFormat=JSON"

def getIp():
	file, headers = urlretrieve("http://icanhazip.com/")
	return open(file).read().strip()

def run(do, params):
	api = "{0}&api_action={1}".format(Api.format(ApiKey), do)
	api = "{0}&{1}".format(api, urlencode(params))
	file, headers = urlretrieve(api)
	return load(open(file))


def update():
	info = run("domain.resource.list", {"DomainID": DomainID, "ResourceID": ResourceID})["DATA"]
	info = info[0]

	myIp = getIp()

	if (info['TARGET'] != myIp) :
		request = {
			"ResourceID": info['RESOURCEID'],
			"DomainID": info['DOMAINID'],
			"Name": info['NAME'],
			"type": info['TYPE'],
			"Target": myIp,
			"TTL_Sec": info['TTL_SEC']
		}

		run("domain.resource.update", request)
		print('update requested')
	else:
		print("no need to update")

update()
