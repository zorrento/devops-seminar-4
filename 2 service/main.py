from flask import Flask, request
import random
app = Flask(__name__)

@app.route("/press")
def index():
    id = int(request.args.get('id'))
    return str(random.randint(95, 165))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)