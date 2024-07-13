from flask_cors import CORS
import json, os, logging, re, shutil
from flask import Flask, Blueprint, render_template, request, abort, session, jsonify, redirect
from functools import wraps
from datetime import datetime, timezone
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# import embeddings

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

            vector_store = Chroma(collection_name="quran-docs", persist_directory="./docs", embedding_function=EMBEDDING_MODEL)

            results = vector_store.similarity_search(query=question, k=1)
            context_data = ""
            for result in results:
                context_data += f'"{result.page_content}"' + '\n\n'

            logging.debug(f"context_data: {context_data}")

            logging.debug(f"Question: {question}")

            return jsonify({"ai_response": context_data}), 200

        return render_template("index.html")

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app