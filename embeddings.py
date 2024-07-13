def create_embeddings(all_verses, chapter_number):
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
                print(verse_info)
                all_verses.append(verse_info)
            
            create_embeddings(all_verses, chapter_number)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        break


def second_approach():
    import requests

    def get_all_verses_with_translations(translation_id=131):
        """Fetches all verses with translations and metadata from the Quran API.

        Args:
            translation_id: The ID of the desired translation (default: 131 for Sahih International).

        Returns:
            A list of dictionaries, each representing a verse with its metadata and translation.
        """
        all_verses = []

        for chapter_number in range(110, 115):  # Quran has 114 chapters
            base_url = "https://api.quran.com/api/v4/quran/verses/by_chapter"
            params = {
                "chapter_number": chapter_number,
                "per_page": 1000,  # Ensure all verses are fetched
                "translations": translation_id,
            }
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                print(data)
                for key, verse in data["verses"]:
                    verse_info = {
                        "chapter_number": chapter_number,
                        "verse_key": f"{chapter_number}:{key}",
                        "verse_id": verse["id"],
                        "text_uthmani": verse["text_uthmani"],
                        "translation": verse["translations"][0]["text"]
                    }
                    all_verses.append(verse_info)
            else:
                print(f"Error fetching chapter {chapter_number}: {response.status_code} - {response.text}")

        return all_verses


    # Example usage
    all_verses_data = get_all_verses_with_translations()

    if all_verses_data:
        for verse in all_verses_data:
            print(f"Chapter: {verse['chapter_number']} ({verse['chapter_name']}), Verse: {verse['verse_number']} (ID: {verse['verse_id']})")
            print(f"Arabic: {verse['text_uthmani']}")
            print(f"Translation: {verse['translation']}")
            print("-----")  # Separator between verses

# second_approach()
first_approach()