from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import logging, os, json, chromadb

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='./.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_embeddings(all_verses):

    # print(all_verses)
    print("Starting - Initializing Vector DB")
    vector_store = Chroma(collection_name='quran-docs', embedding_function=EMBEDDING_MODEL, persist_directory="./docs")
    print("Finished - Initializing Vector DB")

    temp = "\n"
    for i, verse in enumerate(all_verses):
        temp += verse["translation"].split("<sup")[0] + "\n"
        if (i + 1) % 3 == 0:            
            print(temp)
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
            # print(data["meta"])
            for key, verse in enumerate(data["translations"]):
                verse_info = {
                    "translation": f"{chapter_number}:{1+key} {verse['text']}",
                    "verse_key": f"{chapter_number}:{1+key}",
                }
                print(verse_info["translation"])
                all_verses.append(verse_info)
            
        else:
            print(f"Error: {response.status_code} - {response.text}")
    # print(all_verses)

    database_file_name = "./docs/all_verses.json"

    try:
        with open(database_file_name, "w") as database:
            json.dump(all_verses, database)
    except:
        create_embeddings(all_verses)
    
    create_embeddings(all_verses)

def printAllDataInChromaDB():
    """
    Print available metadata in chromadb.

    Usage: For future use to verify if the data is stored properly.
    """
    db = chromadb.PersistentClient("./docs")
    print(f"Collections: {db.list_collections()}")

    collections = db.list_collections()
    for collection in collections:
        print("Collection Name: ", collection.name)
        if input() == "":
            entries = collection.get()
            for i in range(len(entries['ids'])):
                print(f"i = {i}, ids = {entries['ids'][i]}, documents = {entries['documents'][i]}, metadatas = {entries['metadatas'][i]}")


# printAllDataInChromaDB()

if os.path.exists("./docs/all_verses.json"):
    with open("./docs/all_verses.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)        
        create_embeddings(data)
else:
    first_approach()
