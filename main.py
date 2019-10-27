# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import http.client
import json
from http.client import HTTPSConnection
from base64 import b64encode
import datetime as DT
from collections import Counter



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
#app = Flask(__name__)


#@app.route('/')
def get_transactions():
	today = DT.date.today()
	week_ago = today - DT.timedelta(days=7)
	#print(week_ago)
	conn = http.client.HTTPSConnection("gateway-staging.ncrcloud.com")
	payload = "{\"pageSize\":200,\"fromTransactionDateTimeUtc\":{\"dateTime\":\"2019-10-24T03:00:25.055Z\"}}"
	userAndPass = b64encode(b"acct:root@hack_anhem:Password.1").decode("ascii")
	headers = {
		'accept': "application/json",
		'content-type' : "application/json",
		'nep-application-key' : "8a0384356ddb119e016e08ef1028003c",
		#'nep-organization' : "ur-hack",
		'nep-organization' : "silver-merchant-552480",
		'nep-service-version' : "2:1",
		'Authorization' : 'Basic %s' %  userAndPass
		}

	conn.request("POST", "/transaction-document/transaction-documents/find", payload, headers)

	res = conn.getresponse()
	data = res.read()
	temp = data.decode("utf-8")
	transactions = json.loads(temp)
	trans = transactions["pageContent"]
	#print(trans[0]["tlogId"])
	#return transactions["pageContent"]
	trans_id = []
	for cur_trans in trans:
	#	cur_trans = json.loads(t)
		trans_id.append(cur_trans["tlogId"])
	#print(trans_id)
	#return trans
	return trans_id
	
def get_items(trans_id):
	#from collections import Counter 
	#items = dict()
	#for id in trans_id:
	conn = http.client.HTTPSConnection("gateway-staging.ncrcloud.com")
	userAndPass = b64encode(b"acct:root@hack_anhem:Password.1").decode("ascii")
	headers = {
		'accept': "application/json",
		'content-type' : "application/json",
		'nep-application-key' : "8a0384356ddb119e016e08ef1028003c",
		#'nep-organization' : "ur-hack",
		'nep-organization' : "silver-merchant-552480",
		'nep-service-version' : "2:1",
		'Authorization' : 'Basic %s' %  userAndPass
	}
	temp = "/transaction-document/transaction-documents/"
	items = {}
	for id in trans_id:
		url = temp + id
		conn.request("GET",url,headers=headers)
		res = conn.getresponse()
		data = res.read()
		trans = json.loads(data.decode("utf-8"))
	    #print(trans)
		#category = trans["category"]
		#print(category)
		#category = trans["category"]["name"]
		#if category not in items:
		#	items[category] = {}
		for item in trans["tlog"]["items"]:
			#ixt = item["productName"]
		#print(ixt)
			category = item["category"]["name"]
			#print(category)
			if category not in items:
				items[category] = {}
			item_name = item["productName"]
			items[category][item_name] = items[category].get(item_name,0) + 1
	for cat in items.keys():
		print("Most popular ones for %s in order:" %cat)
		srt_item = Counter(items[cat])
		high = srt_item.most_common(5)
		for i in high: 
			print("  " + i[0]) 
	
			
			
		
		

	

		

	
	


if __name__ == '__main__':
	
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    #app.run(host='127.0.0.1', port=8080, debug=True)
	trans_id = get_transactions()
	get_items(trans_id)
# [END gae_python37_app]
