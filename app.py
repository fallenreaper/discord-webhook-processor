from flask import Flask, request, make_response, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
WEBHOOK = os.environ['DISCORD_WEBHOOK_URL'] or None
if WEBHOOK is None:
	exit(1)

def send_string_to_discord(s: str):
	requests.post(WEBHOOK, json={"content":s})

def send_json_to_discord(data: dict):
	"""Data dict requires the following keys:
	- title
	- author
	- content"""
	_json = {
		"embeds": [
			{
				"title": data['title'], 
				'description': data['content'], 
				'author': { 
					'name': f"From: {data['author']}"
				}
			}
		]
	}
	requests.post(WEBHOOK, json=_json)

@app.route('/hook', methods=["POST"])
def hook():
	print(f"Hook Fired")
	
	try:
		if request.mimetype == 'application/json':
			data = request.get_json()
			send_json_to_discord(data)
		else:
			if request.content_length < 1024:
				data = request.get_data()
				send_string_to_discord(data)
	except Exception as e:
		return make_response(jsonify(message=e), 401)
	return make_response(jsonify(message="Success"), 200)
	
app.run()