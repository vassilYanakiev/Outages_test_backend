from flask import Flask,jsonify,request,render_template
from datetime import datetime,timedelta
import json

#mine
from flappings import flapping_alarms

# read file
with open('./data.json', 'r') as myfile:
    data = myfile.read()

# parse file
outages = json.loads(data)
app = Flask(__name__)

#stores = [{
#    'name': 'My Store',
#    'items': [{'name':'my item', 'price': 15.99 }]
#}]

@app.route('/')
def home():
  return render_template('index.html')

#get /outages
@app.route('/flappings')
def get_flappings():
    #return outages
  return jsonify({'flappings': flapping_alarms(outages)})
  #pass


#get /outages
@app.route('/outages')
def get_outages():
    #return outages
  return jsonify({'outages': outages})
  #pass

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
  return jsonify(new_outage)


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
  #if outages['name'] == name:
 #        return jsonify( {'items':store['items'] } )
  return jsonify({'current': current_outages})

@app.route('/outages/recent:<int:time_back>')
def get_recent_outages(time_back):
  now = datetime.now()
  recent_outages = []
  for outage in outages:
      date_time_obj = datetime.strptime(outage['startTime'], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=outage['duration'])
      if date_time_obj < now and date_time_obj>now - timedelta(minutes=time_back):
          recent_outages.append(outage)
  #if outages['name'] == name:
 #        return jsonify( {'items':store['items'] } )
  return jsonify({'recent': recent_outages})

app.run(port=5000)
