import numpy as np
import matplotlib.pyplot as plt
import umap
from langchain_community.vectorstores import FAISS

def visualize_vector_space(vector_db, label="Vector Space"):
    """
    Generate a UMAP scatter plot of the FAISS embeddings.
    Returns a Matplotlib Figure for use in Streamlit or Notebook.
    """
    # Extract dense vectors from FAISS index
    embeddings = vector_db.index.reconstruct_n(0, vector_db.index.ntotal)
    embeddings = np.array(embeddings)

    if embeddings.shape[0] < 5:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Not enough data for UMAP (need >5 chunks)",
                ha="center", fontsize=12)
        ax.axis('off')
        return fig

    reducer = umap.UMAP(n_components=2, random_state=42)
    coords = reducer.fit_transform(embeddings)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(coords[:, 0], coords[:, 1], s=8, alpha=0.7)
    ax.set_title(label)
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")

    return fig