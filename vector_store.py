import faiss
import numpy as np
import pickle
import os

VECTOR_FOLDER = "vectors"

os.makedirs(VECTOR_FOLDER, exist_ok=True)


def create_vector_store(embeddings, chunks):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, os.path.join(VECTOR_FOLDER, "index.faiss"))

    with open(os.path.join(VECTOR_FOLDER, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    print("✅ Vector Store Created Successfully!")


def search_vector_store(question_embedding, k=3):

    index = faiss.read_index(os.path.join(VECTOR_FOLDER, "index.faiss"))

    with open(os.path.join(VECTOR_FOLDER, "chunks.pkl"), "rb") as f:
        chunks = pickle.load(f)

    D, I = index.search(
        np.array([question_embedding]).astype("float32"),
        k
    )

    return [chunks[i] for i in I[0]]