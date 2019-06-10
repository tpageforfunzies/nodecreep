import requests
from kubernetes import client, config
import os
import json
import time


def main():
	update_slack_node_statuses()


def update_slack_node_statuses():
	# call k8s api and get node statuses
	# Configs can be set in Configuration class directly or using helper utility
	# this uses the file mounted by the cronjob from the configmap yaml
	config.load_kube_config(os.path.join(os.getcwd(), './kubeconfig'))
	v1 = client.CoreV1Api()
	ret = v1.list_node(watch=False)

	# prepare the request for the slack webhook
	# set in the cronjob yaml
	url = os.environ['SLACK_WEBHOOK']
	headers = {'Content-type': 'application/json'}
	# cronjob yaml 
	data = {"username": os.environ['SLACK_USERNAME'],
		    "mrkdwn": True,
		    "attachments": []}
	
	# parse and format node status data for slack api
	# attachment per node/item with title of the nodename
	for i in ret.items:
		attachment = {
	        "title": str(i.status.addresses[1].address),
	        "pretext": "",
	        "text": "",
	        "fields": [],
	        "mrkdwn_in": [
	            "text",
	            "pretext",
	            "ts",
	            "fields",
	        ],
	        "footer": "spaghetti-tron industries",
	        # also from the cronjob yaml
            "footer_icon": os.environ['FOOTER_ICON'],
            "ts": time.time(),
	    }
	    
		for condition in i.status.conditions:
			# make a field for the condition
			field = {
				"title": "Type: " + str(condition.type),
				"value": "Status: " + str(condition.status),
				"short": True
			}

			# set the color red to start, guilty into proven innocent
			attachment["color"] =  "#ff0000"

			# change side bar color if it finds a ready status
			if condition.type == "Ready" and condition.status == "True":
				attachment["color"] =  "#36a64f"
				field["value"] += " :white_check_mark:"

			# append the condition field to the node attachment
			attachment["fields"].append(field)

		# add this node's attachment to the request data
		data['attachments'].append(attachment)


	# send request to slack webhook/bot
	requests.post(url, headers=headers, data=json.dumps(data))


if __name__ == '__main__':
	main()
