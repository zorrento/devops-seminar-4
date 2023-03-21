from flask import Flask, request
app = Flask(__name__)

@app.route("/BMI")
def index():
    mass = float(request.args.get('mass'))
    height = float(request.args.get('height'))
    height = height/100.
    return str(round(mass/pow(height, 2), 2))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)