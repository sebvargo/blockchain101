import json
import time
from app import APP, BLOCKCHAIN
from app.utils.objects import Block, Blockchain
from flask import request, render_template, jsonify


@APP.route('/')
def index():
    return render_template('main.html')

@APP.route('/new_transaction', methods = ['POST'])
def new_transaction():
    """
    Add new uncommitted transaction to chain
    """
    data = dict(request.form)
    required_fields = ['author', 'content'] 

    for f in required_fields:
        if not data[f]:
            return f"Invalid transaction data. Missing <{f}>", 404

    data['timestamp'] = time.time()

    BLOCKCHAIN.add_new_transaction(data)

    return f"Success, adding: {json.dumps(data)}", 201

@APP.route('/chain')
def get_chain():
    """
    Return blockchain in JSON format.
    """
    chain_data = []
    for block in BLOCKCHAIN.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length":len(chain_data), "chain": chain_data})

@APP.route('/mine')
def mine_unconfirmed_transactions():
    result = BLOCKCHAIN.mine()
    if not result:
        return "No transactions to mine"
    return f"Block #{result} is mined."

@APP.route('/pending')
def get_pending_transaction():
    return json.dumps(BLOCKCHAIN.unconfirmed_transactions)
