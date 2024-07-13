from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='./.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_embeddings(all_verses, chapter_number):

    print(all_verses)

    temp = []
    for i, verse in enumerate(all_verses):
        temp.append(verse["translation"])
        if i + 1 % 3 == 0:            
            print("Starting - Initializing Vector DB")
            vector_store = Chroma(collection_name='quran-docs', embedding_function=EMBEDDING_MODEL, persist_directory="./docs")
            print("Finished - Initializing Vector DB")

            print("Starting - Storing to Vector DB")
            vector_store.add_texts(texts=temp, metadatas=[verse["verse_key"]])

        
    return True

def first_approach():
    import requests

    base_url = "https://api.quran.com/api/v4/quran/translations/131"

    for chapter_number in range(1, 115):
        params = {"chapter_number": chapter_number}

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            # print(data["meta"])
            all_verses = []
            for key, verse in enumerate(data["translations"]):
                verse_info = {
                    "translation": f"{chapter_number}:{1+key} {verse['text']}",
                    "verse_key": f"{chapter_number}:{1+key}",
                }
                # print(verse_info)
                all_verses.append(verse_info)
            
            create_embeddings(all_verses, chapter_number)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        break

first_approach()