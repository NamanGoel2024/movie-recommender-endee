# Movie Recommendation System using Endee Vector Database

A semantic movie recommendation system built using Endee as the vector database and sentence-transformers for AI embeddings.

## What it does
Type any movie description or theme and it finds the most similar movies from the database using vector similarity search.

## System Design
1. Movie data (title + genre + description) is converted into 384-dimensional vectors using the `all-MiniLM-L6-v2` sentence transformer model
2. These vectors are stored in Endee vector database with cosine similarity space
3. At query time, the user's input is embedded using the same model
4. Endee performs a top-K cosine similarity search and returns the closest movies

## How Endee is used
- Creates an index with dimension=384 and space_type="cosine"
- Upserts movie vectors with metadata (title, genre, description)
- Queries the index with a user input vector to find similar movies

## Setup Instructions

### 1. Start Endee using Docker
```bash
docker-compose up -d
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Ingest movie data into Endee
```bash
python3 ingest.py
```

### 5. Run recommendations
```bash
python3 recommend.py
```

## Example Output
```
Finding movies similar to: 'space exploration and humanity survival'
1. Interstellar (Sci-Fi) — similarity: 0.5
2. 2001 A Space Odyssey (Sci-Fi) — similarity: 0.344
3. Arrival (Sci-Fi) — similarity: 0.339
```

## Tech Stack
- Endee — vector database for similarity search
- sentence-transformers — text to vector embeddings
- pandas — data loading and processing
- Python 3.12
