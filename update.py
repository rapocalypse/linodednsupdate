#!/usr/bin/pyhton3

from json import load
from urllib.parse import urlencode
from urllib.request import urlretrieve

ResourceID 	= ""
DomainID 	= ""
ApiKey		= ""
Api 		= ""

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
