import json


def clean_artist_name(name):
    illegal_symbols = "/"

    for symbol in illegal_symbols:
        name = name.replace(symbol, " ")

    return name.replace("  ", " ").strip()


def clean_track_name(name):
    illegal_symbols = ".,()\"'/-;“«»”&!"

    for symbol in illegal_symbols:
        name = name.replace(symbol, " ")

    replacements = [
        ("movements", " "),
        ("Movements", " "),
        ("Movement", " "),
        ("movement", " "),
        ("mov", " "),
        ("First", "I"),
        ("first", "I"),
        ("1st", "I"),
        ("2nd", "II"),
        ("3rd", "III"),
        ("4th", "IV"),
        ("Opus", "Op"),
        ("Seriouses", "Serieuses"),
        ("PreludesBII", "Preludes BII"),
        ("SuiteBergamasque", "Suite Bergamasque"),
        ("Variaions", "Variations"),
        ("Islamei", "Islamey"),
        ("IsoldasLiebestod", "Isolde Liebestod"),
        ("RameauSelections", "Rameau Selections")
    ]

    for replacement in replacements:
        name = name.replace(replacement[0], replacement[1])

    return name.replace("  ", " ").strip()


original_file = "data/maestro-v3.0.0.json"
with open(original_file, "r") as f_in:
    data = json.load(f_in)
    artists = data["canonical_composer"]
    tracks = data["canonical_title"]

    for key in artists:
        artists[key] = clean_artist_name(artists[key])

    for key in tracks:
        tracks[key] = clean_track_name(tracks[key])

cleaned_file = "data/maestro-v3.0.0-clean.json"
with open(cleaned_file, "w") as f_out:
    f_out.write(json.dumps(data))
