from flask import Flask,jsonify,request,render_template
from datetime import datetime,timedelta
from flask_cors import CORS
import json

from flappings import flapping_alarms

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

with open('./data.json', 'r') as myfile:
    data = myfile.read()


outages = json.loads(data)




@app.route('/')
def home():
  return render_template('index.html')

#get /outages
@app.route('/flappings')
def get_flappings():
    #return outages
  return jsonify(flapping_alarms(outages))
  #pass


#get /outages
@app.route('/outages')
def get_outages():

  return jsonify(outages)


#post /outages data: {name :}
@app.route('/outages' , methods=['POST'])
def create_store():
  request_data = request.get_json()
  new_outage = {
    'service_id':request_data['service_id'],
    'duration':request_data['duration'],
    'startTime':request_data['startTime']
  }
  outages.append(new_outage)
  return 'Done', 201


#get /outages/current
@app.route('/outages/current')
def get_current_outages():
  now = datetime.now()
  current_outages = []
  for outage in outages:
      date_time_obj_start = datetime.strptime(outage['startTime'], '%Y-%m-%d %H:%M:%S')
      date_time_obj_end = date_time_obj_start + timedelta(minutes=outage['duration'])
      if date_time_obj_start < now and date_time_obj_end > now :
          current_outages.append(outage)
  return jsonify(current_outages)

@app.route('/outages/recent:<int:time_back>')
def get_recent_outages(time_back):
  now = datetime.now()
  recent_outages = []
  for outage in outages:
      date_time_obj = datetime.strptime(outage['startTime'], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=outage['duration'])
      if date_time_obj < now and date_time_obj>now - timedelta(minutes=time_back):
          recent_outages.append(outage)

  return jsonify(recent_outages)


if __name__ == '__main__':
    app.run(port=5000)
