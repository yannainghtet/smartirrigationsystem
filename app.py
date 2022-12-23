from flask import Flask, render_template, request, redirect, make_response, Response
import random
import json
from random import random
from flask_sqlalchemy import SQLAlchemy
from time import sleep
import os
import logging
import machinelearning

from turbo_flask import Turbo
import threading
from datetime import datetime
from pytz import timezone
import time

app = Flask(__name__)
temperature = 0
humidity = 0
soilmoisture = 0
temp2 = 0
hum2 = 0
soil2 = 0
turbocount = 0
glcount = 0
wateramount = 0
turbo = Turbo(app)

#Starting page
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['GET','POST'])
def submit():
  name= request.form['name']
  email=request.form['email']
  return redirect('/log_Data')


@app.route('/log_Data', methods=['GET','POST'])
def log_Data():
    global temperature
    global humidity
    global soilmoisture
    global temp2
    global hum2
    global soil2
    global time

    if request.method == 'POST':
        app.logger.info(request.form)
        temperature = float(request.form.get('temp1'))
        # print("Field1-Temp: {}".format(temperature))
        humidity = float(request.form.get('hum1'))
        # print("Field1-Hum: {}".format(humidity))
        soilmoisture = float(request.form.get('soilm1'))
        # print("Field1-Soil: {}".format(soilmoisture))
        # print("**********************************************")
        temp2 = float(request.form.get('temp2'))
        # print("Field2-Temp: {}".format(temp2))
        hum2 = float(request.form.get('hum2'))
        # print("Field2-Hum: {}".format(hum2))
        soil2 = float(request.form.get('soilm2'))
        #print("Field2-Soil: {}".format(soil2))
        print("**********************************************")
        reading_time = datetime.now(tz=timezone('Asia/Yangon'))
        #return "data logged"
    return render_template('base.html', temperature=temperature, humidity=humidity,soilmoisture = soilmoisture,time=time)


@app.route('/field2', methods=['GET','POST'])
def log_Data2():
    global temp2
    global hum2
    global soil2
    global time

    if request.method == 'POST':
        # #app.logger.info(request.form)
        # temperature = float(request.form.get('temp1'))
        # # print("Field1-Temp: {}".format(temperature))
        # humidity = float(request.form.get('hum1'))
        # # print("Field1-Hum: {}".format(humidity))
        # soilmoisture = float(request.form.get('soilm1'))
        # # print("Field1-Soil: {}".format(soilmoisture))
        # # print("**********************************************")
        temp2 = request.form.get('temp2')
        # print("Field2-Temp: {}".format(temp2))
        hum2 = request.form.get('hum2')
        # print("Field2-Hum: {}".format(hum2))
        soil2 = request.form.get('soilm2')
        # print("Field2-Soil: {}".format(soil2))
        print("**********************************************")
        reading_time = datetime.now(tz=timezone('Asia/Yangon'))
        # return "data logged"
    return render_template('ml.html', temp2=temp2, hum2=hum2, soil2=soil2, time=time)




@app.route("/", methods = ["GET","POST"])
def predict():
    global wateramount
    if request.method == "POST":
        cpday   = request.form['cpday']
        sm      = request.form['sm']
        temp    = request.form['temp']
        humi    = request.form['humi']
        tempmax = request.form['tempmax']
        tempmin = request.form['tempmin']
        evapo   = request.form['evapo']
        cpfactor = request.form['cpfactor']

        env_values = [[cpday,sm,temp,humi,tempmax,tempmin,evapo,cpfactor]]

        wateramt = machinelearning.WateramountPrediction(env_values)
        print(wateramt)
        wateramount = wateramt
    return render_template("base.html", n= wateramount )

    
@app.route('/data', methods=["GET", "POST"])
def data():    
    if request.method == 'GET':
        Temperature = temperature
        Humidity = humidity	
        data = [time() * 1000, Temperature, Humidity]

        response = make_response(json.dumps(data))

        response.content_type = 'application/json'

        return response    

@app.route('/temp-data')
def temp_data():
    def generate_temp_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime(' %H:%M:%S'), 'value': temperature})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_temp_data(), mimetype='text/event-stream')     

@app.route('/hum-data')
def hum_data():
    def generate_hum_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime(' %H:%M:%S'), 'value': humidity})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_hum_data(), mimetype='text/event-stream')

@app.route('/soil-data')
def soil_data():
    def generate_soil_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': soilmoisture})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_soil_data(), mimetype='text/event-stream')

@app.route('/temp-data-b')
def temp_data_b():
    def generate_temp_data_b():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime(' %H:%M:%S'), 'value': temp2})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_temp_data_b(), mimetype='text/event-stream')

@app.route('/hum-data-b')
def hum_data_b():
    def generate_hum_data_b():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime(' %H:%M:%S'), 'value': hum2})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_hum_data_b(), mimetype='text/event-stream')

@app.route('/soil-data-b')
def soil_data_b():
    def generate_soil_data_b():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': soil2})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_soil_data_b(), mimetype='text/event-stream')
#-----------------------------------------------------------------------

@app.context_processor
def injectSensorData():

    global temperature
    global humidity
    global soilmoisture

        
    return dict(
    temperature = temperature,
    humidity = humidity,
    soilmoisture = soilmoisture,
    )

#----------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Background updater thread that runs before 1st client connects
@app.before_first_request
def before_first_request():
    threading.Thread(target=update_sensor_data).start()

def update_sensor_data():
    with app.app_context():    
        while True:
            sleep(4)
            turbo.push(turbo.replace(render_template('base.html'), 'base'))
            
#-----------------------------------------------------------------------

if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)# Get port number of env at runtime, else use default port 5000
    app.run(debug=True, host='0.0.0.0', port=port)  # 0.0.0.0 port forwarding resolves the host IP address at runtime
