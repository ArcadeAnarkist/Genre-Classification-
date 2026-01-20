import pandas as pd
from pathlib import Path

INPUT_CSV = "data/måske? /dataset.csv"
OUT_DIR = "data/måske? /new output fil "

def normalize_text(input_value):
    if input_value is None:
        print("Boss du mangler en input fil")
        return 

    text = str(input_value)
    text = text.lower()
    text = text.strip()
    text = text.replace("-", " ")
    text = text.replace("/", " ")


    # Fjern ekstra mellemrum
    while "  " in text:
        text = text.replace("  ", " ")

    return text

def strip_geo_prefix(genre_text):
    if genre_text is None:
        return ""

    geo_words = [
        "dutch", "british", "german", "australian", "canadian",
        "belgian", "irish", "italian", "danish", "finnish",
        "scottish", "icelandic", "barbadian", "arkansas"
    ]

    ny_text = genre_text.lower()

    # Fjern geo-ord
    for word in geo_words:
        ny_text = ny_text.replace(word, "")

    # Fjern ekstra mellemrum
    ny_text = ny_text.strip()
    while "  " in ny_text:
        ny_text = ny_text.replace("  ", " ")

    return ny_text

def has_any(text, keyword_list):
    for keyword in keyword_list:
        keyword = keyword.lower()

        if " " in keyword:
            if keyword in text:
                return True
        else:
            words = text.split(" ")
            if keyword in words:
                return True

    return False



def classify_genre(genre_text: str) -> str:
    #PRIORITET: hiphop -> electronic -> roots -> rock -> pop -> jazz_soul (fallback) 

    text = normalize_text(genre_text)
    text = strip_geo_prefix(text)

    # HIP HOP
    if has_any(text, ["hip hop", "hip-hop", "hiphop", "rap", "trap", "g funk", "g-funk", "gangster", "rap", "hip hop", "hip-hop", "hiphop", "rap", "trap", "g funk", "g-funk", "gangster", "r n b", "r-n-b", "rnb", "trip hop", "trip-hop"]):
        return "hiphop"

    # ELECTRONIC
    if has_any(text, [
        "edm", "electro", "electro house", "house", "trance", "techno", "electronica",
        "big room", "big beat", "gabba", "happy hardcore", "hardcore", "downtempo", "newage", 
        "j-core", "j core", "electropop", "cyberpunk", "metropopolis", "laboratorio", "electronic", "breakbeat", "drum and bass", "drum-and-bass", "dubstep", "idm", "hardstyle", "club"
    ]):
        return "electronic"

    # ROOTS
    if has_any(text, [
        "folk", "americana", "country", "contemporary country", "classic country pop", "alternative country", "roots", 
        "singer-songwriter", "singer songwriter", "stomp and holler", "stomp", "acoustic", "celtic", "folk - pop", "bluegrass"
    ]):
        return "roots"

    # ROCK 
    if has_any(text, [
        "rock", "metal", "hard rock", "glam metal", "punk", "pop punk", "grunge", "garage",
        "alternative", "alternative rock", "alt rock", "britpop", "prog", "emo", "goth", 
        "new wave", "permanent wave", "art rock", "yacht rock", "invasion", "grindcore", "industrial", "rockabilly", "ska", "guitar",
        "rock-and-roll", "rock and roll", "dance rock", "classic rock", "modern rock", "album rock", "metalcore"
    ]):
        return "rock"

    # POP
    if has_any(text, [
        "pop", "dance pop", "disco", "bubblegum pop", "candy pop", "boy band", "nederpop", "eurodance", "australian dance", "dance", 
        "schlager", "europop", "art pop", "chamber pop", "brill building pop", "baroque pop", "australian psych", "psych",
        "neo mellow", "mellow gold", "soft rock", "operatic pop", "adult", "adult standards", "indie", "dutch indie", "austropop", "dancehall"
    ]):
        return "pop"

    # JAZZ / SOUL
    if has_any(text, [
        "soul", "neo soul", "classic soul", "chicago soul", "motown","funk",
        "jazz", "acid jazz", "bebop", "contemporary vocal jazz","reggae", "reggae fusion",
        "latin", "latin jazz", "latin alternative", "afropop", "cabaret", "chanson",
        "soundtrack", "ambient", "compositional ambient", "blues", "afrobeat", "gospel", "grove"
    ]):
        return "jazz_soul"

    # fallback
    return "other"


def main():
    # 1. Tjek at input-filen findes
    input_path = Path(INPUT_CSV)
    output_path = Path(OUT_DIR)
    
    data = pd.read_csv(input_path)
    genre_column = "track_genre"
    genre_buckets = []

    for genre_value in data[genre_column]:
        bucket = classify_genre(genre_value)
        genre_buckets.append(bucket)

    data["_bucket"] = genre_buckets

    data[genre_column] = data["_bucket"]

    bucket_names = ["rock", "pop", "hiphop", "electronic", "roots", "jazz_soul", "other"]

    all_file = output_path / "all_songs.csv"
    data.drop(columns=["_bucket"]).to_csv(all_file, index=False)
    print("all:", len(data), "rækker gemt i", all_file)

    # 9. Gem én CSV-fil pr. genre
    for bucket_name in bucket_names:
        rows_in_bucket = data[data["_bucket"] == bucket_name]
        rows_in_bucket = rows_in_bucket.drop(columns=["_bucket"])

        output_file = output_path / (bucket_name + ".csv")
        rows_in_bucket.to_csv(output_file, index=False)

        print( bucket_name, ":", len(rows_in_bucket), "rækker gemt i", output_file)

print("\n")
if __name__ == "__main__":
    main()
print("\n")

data = pd.read_csv("data/måske? /dataset.csv")
print("Rows læst fra input:", len(data))
print("Kolonner:", list(data.columns))
