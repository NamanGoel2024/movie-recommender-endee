# 🎬 Movie Recommendation System using Endee Vector Database

A semantic movie recommendation system that uses AI to find similar movies based on your description. Built using Endee as the vector database and sentence-transformers for AI embeddings.

## 📽️ Demo
```
Enter your query: space exploration and humanity survival
Filter by genre? (or press Enter to skip): Sci-Fi

1. Interstellar (Sci-Fi)
   Similarity : 50.0%
   Description: A team travels through a wormhole near Saturn in search of a new home for humanity

2. 2001 A Space Odyssey (Sci-Fi)
   Similarity : 34.4%
   Description: A voyage to Jupiter with the AI HAL 9000 descends into a psychological thriller
```

## 🧠 How it works
1. Each movie's title, genre and description is converted into a 384-dimensional vector using the `all-MiniLM-L6-v2` sentence transformer model
2. These vectors are stored in Endee vector database with cosine similarity space
3. When user types a query, it is converted to a vector using the same model
4. Endee searches for the closest movie vectors and returns top 5 matches
5. Results are ranked by similarity percentage

## 🏗️ System Design
```
Movies CSV → Sentence Transformer → Vectors → Endee Database
                                                      ↑
User Query → Sentence Transformer → Query Vector → Cosine Search → Top 5 Movies
```

## 🛠️ Tech Stack
- **Endee** — high performance vector database for similarity search
- **sentence-transformers** — converts text to AI embeddings
- **pandas** — data loading and processing
- **Docker** — runs Endee database
- **Python 3.12**

## 📁 Project Structure
```
movie-recommender-endee/
├── movies.csv          ← 40 movie dataset
├── ingest.py           ← loads movies into Endee
├── recommend.py        ← recommendation engine
├── setup.py            ← one command setup script
├── requirements.txt    ← Python dependencies
└── README.md           ← project documentation
```

## 🚀 Quick Start (One Command)

### Prerequisites
- Python 3.x installed
- Docker installed and running

### Run
```bash
git clone https://github.com/NamanGoel2024/movie-recommender-endee.git
cd movie-recommender-endee
python3 setup.py
```

That's it! setup.py will automatically:
- ✅ Check Docker is installed
- ✅ Start Endee database
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Load movies into Endee
- ✅ Launch the recommender

## 📖 Manual Setup (Alternative)

### 1. Start Endee using Docker
```bash
docker run -d -p 8080:8080 --name endee-server endeeio/endee-server:latest
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Load movies into Endee
```bash
python3 ingest.py
```

### 5. Run recommender
```bash
python3 recommend.py
```

## 💡 How Endee is used
- Creates an index with `dimension=384` and `space_type="cosine"`
- Upserts 40 movie vectors with metadata (title, genre, description)
- Queries the index with user input vector to find top-K similar movies
- Returns results ranked by cosine similarity score

## 🎯 Features
- 🔍 Semantic search — understands meaning not just keywords
- 🎭 Genre filtering — filter results by genre
- 📊 Similarity percentage — shows how close each match is
- ⌨️ Interactive mode — type any query and get instant results
- 🛡️ Handles typos — AI model understands misspelled queries

## 📊 Dataset
40 movies across genres including Sci-Fi, Thriller, Drama, Crime, Horror and Action.
