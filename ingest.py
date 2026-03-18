import pandas as pd
from sentence_transformers import SentenceTransformer
from endee import Endee, Precision

# 1. Connect to Endee
client = Endee()

# 2. Create index
try:
    client.create_index(
        name="movies",
        dimension=384,
        space_type="cosine",
        precision=Precision.INT8
    )
    print("Index 'movies' created.")
except Exception as e:
    print(f"Index may already exist: {e}")

# 3. Load movie data
df = pd.read_csv("movies.csv")
print(f"Loaded {len(df)} movies")

# 4. Load AI embedding model
print("Loading AI model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 5. Create text for each movie
texts = [
    f"{row['title']} {row['genre']} {row['description']}"
    for _, row in df.iterrows()
]

# 6. Convert texts to vectors
print("Generating embeddings...")
vectors = model.encode(texts, show_progress_bar=True)

# 7. Upload vectors to Endee
index = client.get_index(name="movies")
items = []
for i, (_, row) in enumerate(df.iterrows()):
    items.append({
        "id": str(row["id"]),
        "vector": vectors[i].tolist(),
        "meta": {
            "title": row["title"],
            "genre": row["genre"],
            "description": row["description"]
        }
    })

index.upsert(items)
print(f"Successfully ingested {len(items)} movies into Endee!")
