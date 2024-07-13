from flask_cors import CORS
import json, os, logging, re, shutil
from flask import Flask, Blueprint, render_template, request, abort, session, jsonify, redirect
from functools import wraps
from datetime import datetime, timezone

import embeddings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='./.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app():
    app = Flask(__name__)
    CORS(app=app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST': 
            question = request.json.get('question')
            chats = request.json.get('chats')

            logging.debug(f"Question: {question}")

            return jsonify({"ai_response": question}), 200

        return render_template("index.html")

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app