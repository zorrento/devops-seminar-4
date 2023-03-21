from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route("/risk")
def index():
    try:
        id = int(request.args.get('id'))
        age = int(request.args.get('age'))
        mass = float(request.args.get('mass'))
        height = float(request.args.get('height'))
    except TypeError:
        return "Not enough data!"
    antropometry = {'mass' : str(mass), 'height' : str(height)}
    response = requests.get("http://first-service-container/BMI", params=antropometry) #BMI
    body_mass_index = float(response.text)
    id_param = {'id' : str(id)}
    response = requests.get("http://second-service-container/press", params = id_param)# PRESSURE
    pressure = int(response.text)
    result = "None"
    if pressure > 140 and body_mass_index > 35 and age > 30: result = "High"
    if pressure > 140 and body_mass_index > 30 and age <= 30: result = "Medium"
    if pressure > 130 and pressure <= 140 and body_mass_index > 40 and age >= 25: result = "High"
    if pressure > 130 and pressure <= 140 and body_mass_index > 30 and body_mass_index <= 40 and age >= 30: result = "Medium"
    if result == "None": result = "Low"
    print(pressure, body_mass_index, age, result)
    result = {'risk' : result, 'bmi' : body_mass_index, 'pressure' : pressure}
    return jsonify(result)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)