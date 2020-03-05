import requests
from flask import Flask, abort, request, jsonify, g, url_for, Response
from flask import make_response, flash, redirect, render_template, session

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return "hello"


if __name__ == "__main__":
    app.run()
