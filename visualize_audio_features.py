from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt


keys = {
    0: 'C',
    1: 'C#/Db',
    2: 'D',
    3: 'D#/Eb',
    4: 'E',
    5: 'F',
    6: 'F#/Gb',
    7: 'G',
    8: 'G#/Ab',
    9: 'A',
    10: 'A#/Bb',
    11: 'B'
}

modes = {
    0: 'minor',
    1: 'major'
}

df = pd.read_json('data/tracks-with-audio-features.json')
df = df.transpose()

rows_with_missing_data = sum([True for _, row in df.iterrows() if any(row.isnull())])
total_rows = len(df.index)
coverage = round(100 * (total_rows - rows_with_missing_data) / total_rows, 2)

df = df.dropna()

fig, axes = plt.subplots(3, 5)

fig.canvas.set_window_title('Histograms / Barcharts')
fig.suptitle(f"Spotify audio features for the Maestro dataset (coverage: {coverage}%)")

axes[0, 0].set_title("danceability (density)")
axes[0, 0].hist(df["danceability"], density=True)
axes[0, 0].set_xlim([0, 1])

axes[0, 1].set_title("energy (density)")
axes[0, 1].hist(df["energy"], density=True)
axes[0, 1].set_xlim([0, 1])

key_counts = Counter(df["key"].sort_values().map(keys))
axes[0, 2].set_title("key")
axes[0, 2].bar(key_counts.keys(), key_counts.values())

axes[0, 3].set_title("loudness (density)")
axes[0, 3].hist(df["loudness"], density=True)
axes[0, 3].set_xlim([-60, 0])
axes[0, 3].set_xlabel("dB")

mode_counts = Counter(df["mode"].sort_values().map(modes))
axes[0, 4].set_title("mode")
axes[0, 4].bar(mode_counts.keys(), mode_counts.values())

axes[1, 0].set_title("speechiness (density)")
axes[1, 0].hist(df["speechiness"], density=True)
axes[1, 0].set_xlim([0, 1])

axes[1, 1].set_title("acousticness (density)")
axes[1, 1].hist(df["acousticness"], density=True)
axes[1, 1].set_xlim([0, 1])

axes[1, 2].set_title("instrumentalness (density)")
axes[1, 2].hist(df["instrumentalness"], density=True)
axes[1, 2].set_xlim([0, 1])

axes[1, 3].set_title("liveness (density)")
axes[1, 3].hist(df["liveness"], density=True)
axes[1, 3].set_xlim([0, 1])

axes[1, 4].set_title("valence (density)")
axes[1, 4].hist(df["valence"], density=True)
axes[1, 4].set_xlim([0, 1])

axes[2, 0].set_title("tempo (density)")
axes[2, 0].hist(df["tempo"], density=True)
axes[2, 0].set_xlabel("beats per minute")

axes[2, 1].set_title("duration (density)")
axes[2, 1].hist(df["duration_ms"].div(1000).div(60), density=True)
axes[2, 1].set_xlabel("minutes")

time_signature_counts = Counter(df["time_signature"].sort_values())
axes[2, 2].set_title("time_signature")
axes[2, 2].bar(time_signature_counts.keys(), time_signature_counts.values())
axes[2, 2].set_xlabel("beats per measure (bar)")

axes[2, 3].axis("off")
axes[2, 4].axis("off")

plt.show()
