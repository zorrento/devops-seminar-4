from flask import Flask, request
import requests
import ast
import time
import pymongo

app = Flask(__name__)

@app.route("/app")
def index():
    myclient = pymongo.MongoClient("mongodb://mongo-container:27017/")
    mydb = myclient["data"]
    mycol = mydb["people"]
    try:
        id = int(request.args.get('id'))
        age = int(request.args.get('age'))
        mass = float(request.args.get('mass'))
        height = float(request.args.get('height'))
    except TypeError:
        return "Not enough data!"
    search_res = mycol.find_one({"id": id, "age": age, "mass": mass, "height": height})
    if not search_res:
        parameters = {'id': id, 'age': age, 'mass': mass, 'height': height}
        response = requests.get("http://third-service-container/risk", params=parameters)
        data_dict = ast.literal_eval(response.text)
        data_to_insert = {
            'id': id,
            'age': age,
            'pressure': data_dict['pressure'],
            'mass': mass,
            'height': height,
            'body_mass_index': data_dict['bmi'],
            'risk': data_dict['risk'],
            'timestamp': time.time_ns()
        }
        mycol.insert_one(data_to_insert)
    else:
        if (round(search_res['timestamp'] / 10 ** 9) - round(time.time_ns() / 10 ** 9)) > 300:
            parameters = {'id': id, 'age': age, 'mass': mass, 'height': height}
            response = requests.get("http://third-service-container/risk", params=parameters)
            data_dict = ast.literal_eval(response.text)
            data_to_insert = {
                'id': id,
                'age': age,
                'pressure': data_dict['pressure'],
                'mass': mass,
                'height': height,
                'body_mass_index': data_dict['bmi'],
                'risk': data_dict['risk'],
                'timestamp': time.time_ns()
            }
            mycol.insert_one(data_to_insert)
    search_res = mycol.find_one({"id": id, "age": age, "mass": mass, "height": height})
    return str(search_res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
