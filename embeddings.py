from langchain_huggingface import HuggingFaceEmbeddings
import logging, os, json
import os, pymongo, pprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='./.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

try:
    client = MongoClient(os.environ.get("DB_CONNECTION_STRING"))
    client.admin.command('ping')
    logging.debug("Connected to MongoDB Atlas successfully")
    
    db = client.get_database("master")
    atlas_collection = db.get_collection("quran-embeddings")
    vector_search_index = "vector_index"
    
    logging.debug(f"index info: {db['quran-embeddings'].index_information()}")

    logging.debug("Starting - Initializing Vector DB")
    vector_store = MongoDBAtlasVectorSearch(collection=atlas_collection, embedding=EMBEDDING_MODEL, index_name=vector_search_index)
    logging.debug("Finished - Initializing Vector DB")

except ConnectionFailure as e:
    logging.debug(f"Failed to connect to MongoDB Atlas: {e}")

def similarity_search(query, k=3):
    logging.debug(f"Query: {query}")
    result = vector_store.similarity_search(query, k=k)
    logging.debug(f"result: {result}")
    return result

def create_embeddings(all_verses):
    temp = "\n"
    for i, verse in enumerate(all_verses):
        temp += verse["translation"].split("<sup")[0] + "\n"
        if (i + 1) % 3 == 0:            
            logging.debug(temp)
            vector_store.add_texts(texts=[temp], metadatas=[verse])
            temp = "\n"

    return True

def first_approach():
    import requests

    base_url = "https://api.quran.com/api/v4/quran/translations/131"

    all_verses = []
    for chapter_number in range(1, 115):
        params = {"chapter_number": chapter_number}

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            # logging.debug(data["meta"])
            for key, verse in enumerate(data["translations"]):
                verse_info = {
                    "translation": f"{chapter_number}:{1+key} {verse['text']}",
                    "verse_key": f"{chapter_number}:{1+key}",
                }
                logging.debug(verse_info["translation"])
                all_verses.append(verse_info)
            
        else:
            logging.debug(f"Error: {response.status_code} - {response.text}")
    # logging.debug(all_verses)

    database_file_name = "./docs/all_verses.json"

    try:
        with open(database_file_name, "w") as database:
            json.dump(all_verses, database)
    except:
        create_embeddings(all_verses)
    
    create_embeddings(all_verses)

count = atlas_collection.count_documents({})
if count == 0:
    if os.path.exists("./docs/all_verses.json"):
        with open("./docs/all_verses.json", 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)        
            create_embeddings(data)
    else:
        first_approach()