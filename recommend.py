from sentence_transformers import SentenceTransformer
from endee import Endee

# Connect to Endee and load model
client = Endee()
model = SentenceTransformer("all-MiniLM-L6-v2")
index = client.get_index(name="movies")

def recommend(query: str, genre_filter: str = None, top_k: int = 5):
    print(f"\nFinding movies similar to: '{query}'")
    if genre_filter:
        print(f"Filtering by genre: '{genre_filter}'")
    print()

    # Convert query to vector
    query_vector = model.encode(query).tolist()

    # Fetch more results to account for genre filtering
    fetch_k = top_k * 4 if genre_filter else top_k
    results = index.query(vector=query_vector, top_k=fetch_k)

    # Filter by genre if specified
    if genre_filter:
        results = [
            r for r in results
            if genre_filter.lower() in (r.get("meta") or {}).get("genre", "").lower()
        ]

    if not results:
        print("No movies found matching your criteria. Try a different genre or query.\n")
        return

    print(f"Top {min(top_k, len(results))} recommendations:")
    print("=" * 60)
    for i, r in enumerate(results[:top_k], 1):
        meta = r.get("meta") or {}
        title = meta.get("title", "Unknown")
        genre = meta.get("genre", "Unknown")
        score = round(r.get("similarity", 0) * 100, 1)
        desc  = meta.get("description", "No description available.")
        print(f"{i}. {title} ({genre})")
        print(f"   Similarity : {score}%")
        print(f"   Description: {desc}")
        print()

# Interactive mode
print("\n🎬 Movie Recommendation System")
print("Powered by Endee Vector Database")
print("=" * 60)
print("Type a movie description to get recommendations!")
print("Type 'quit' to exit\n")

while True:
    query = input("Enter your query: ").strip()
    if not query:
        print("Please enter something!\n")
        continue
    if query.lower() == 'quit':
        print("Goodbye! 🎬")
        break

    genre = input("Filter by genre? (Sci-Fi / Drama / Thriller / Crime / Horror / Action / Animation - or press Enter to skip): ").strip()

    recommend(query, genre_filter=genre if genre else None)
