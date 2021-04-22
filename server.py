import flask
from flask import request, url_for, render_template, redirect
from plot_ride import update_layout, plot_path
import numpy as np
import json
import plotly.graph_objects as go
from plotly.io import to_html

mapbox_access_token = open("./.public").read()
app = flask.Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	return '''<p>Send request to -hostname-:5000/plot?id=-id-.</p>
			<p>In request body, include standard_points, s2r_points and new_algo_points</p>
			<p>Include points in the following sample format (lat long):<br>
			[[31.4324221 , 73.1317705 ],<br>
			[31.4324221 , 73.1317705 ],<br>
			[31.43188167, 73.13088833],<br>
			[31.431525  , 73.13052833],<br>
			[31.43115667, 73.13016   ],<br>
			[31.4290133 , 73.1277577 ]]</p>'''

@app.route('/plot/',methods=['GET','POST'])
def plot():
	if 'id' in request.args:
		id = int(request.args['id'])
	else:
		return "Error: No id field provided. Please specify an id."
	
	body =  request.get_json(force=True)

	for points in ['standard_points', 's2r_points', 'new_algo_points']:
		if points not in body:
			return "Error: No " + points + " field provided. Please specify " + points + "."
		else:
			body[points] = np.array(body[points]).T
			print(body[points].shape, print(body[points]))
			

	fig = go.Figure()

	plot_path(fig, body['standard_points'], color='rgb(255, 0, 0)', mode='lines+markers', text='orig_points')
	plot_path(fig, body['new_algo_points'], color='rgb(0, 255, 0)', mode='lines', text='new_algo')
	plot_path(fig, body['s2r_points'], color='rgb(0, 0, 255)', mode='lines+markers', text='s2r_points')

	update_layout(fig, 'Ride ID: ' + str(id), body['standard_points'][:,int(body['standard_points'].shape[1]/2)])
	
	# fig.show(renderer='iframe_connected')
	return to_html(fig, include_plotlyjs='cdn')

if __name__ == '__main__':
	app.run(debug=True)