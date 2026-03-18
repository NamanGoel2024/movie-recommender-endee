from sentence_transformers import SentenceTransformer
from endee import Endee

# Connect to Endee and load model
client = Endee()
model = SentenceTransformer("all-MiniLM-L6-v2")
index = client.get_index(name="movies")

def recommend(query: str, top_k: int = 5):
    print(f"\nFinding movies similar to: '{query}'\n")
    
    # Convert query to vector
    query_vector = model.encode(query).tolist()
    
    # Search Endee for closest movies
    results = index.query(vector=query_vector, top_k=top_k)
    
    print(f"Top {top_k} recommendations:")
    print("-" * 50)
    for i, r in enumerate(results, 1):
        title = r["meta"]["title"]
        genre = r["meta"]["genre"]
        score = round(r["similarity"], 3)
        desc = r["meta"]["description"][:80]
        print(f"{i}. {title} ({genre}) — similarity: {score}")
        print(f"   {desc}...")
    print()

# Test queries
recommend("a mind-bending thriller about identity and reality")
recommend("space exploration and humanity survival")
recommend("psychological drama with dark obsession")
