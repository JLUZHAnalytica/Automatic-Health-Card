from flask import Flask
from auto_health import *

app = Flask(__name__)

@app.route("/username=<username>&password=<password>/number=<number>")
def single(username,password,number):
    return main(username,password,number)

@app.route("/username=<username>&password=<password>/start=<start>&end=<end>")
def plural(username,password,start,end):
    return mains(username,password,start,end)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000")