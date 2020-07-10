from flask import Flask
from app.utils.objects import Blockchain

# initialize Flask app
APP = Flask(__name__)

BLOCKCHAIN = Blockchain()

from app import controller