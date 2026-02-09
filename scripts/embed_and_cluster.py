from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans


# ------------------
# Configuration
# ------------------

DATA_PATH = Path("data/processed/emails_sample.csv")
OUT_PATH = Path("data/processed/emails_clustered.csv")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
N_CLUSTERS = 6  # chosen empirically
RANDOM_STATE = 43


# ---------------------
# Helpers
# ---------------------

def load_dataset(path: Path) -> pd.DataFrame:
    """
    Load the dataset by given path
    
    Returns:
        df: pd.Dataframe
    """

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")
    
    df = pd.read_csv(path)

    if "text" not in df.columns:
        raise ValueError(f"Expected 'text' column in the dataset")
    
    return df


def compute_embeddings(texts: List[str], model_name: str) -> np.ndarray:
    """
    compute embeddings using chosen model from SentenceTransformer
    
    :param texts: the text data
    :type texts: List[str]
    :param model_name: chosen model name
    :type model_name: str
    :return: embeddings for the texts
    :rtype: ndarray[_AnyShape, dtype[Any]]
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        texts,
        show_progress_bar = True,
        convert_to_numpy = True,
        normalize_embeddings = True
    )

    return embeddings



def cluster_embeddings(embeddings: np.ndarray, n_clusters: int) -> np.ndarray:
    """
    cluster the embeddings of the texts
    
    :param embeddings: computed embeddings
    :type embeddings: np.ndarray
    :param n_clusters: number of desired clusters
    :type n_clusters: int
    :return: computed labels
    :rtype: ndarray[_AnyShape, dtype[Any]]
    """
    kmeans = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_STATE,
        n_init=10
    )

    # we get the labels for the embedding clusters
    labels = kmeans.fit_predict(embeddings)
    return labels


def save_results(df: pd.DataFrame, labels: np.ndarray, out_path: Path) -> None:
    """
    Persist the results
    
    :param df: dataframe
    :type df: pd.DataFrame
    :param labels: number of desired clusters 
    :type labels: np.ndarray
    :param out_path: persistence path
    :type out_path: Path
    """
    df = df.copy()
    df['cluster_id'] = labels
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)



############################
# Main function
############################

def main() -> None:
    df = load_dataset(DATA_PATH)

    # fill null values with empty string, if any 
    texts = df["text"].fillna("").tolist()

    # we compute embeddings for the texts of each row in the record
    embeddings = compute_embeddings(texts, EMBEDDING_MODEL_NAME)

    # clusterize the embeddings of the texts
    labels = cluster_embeddings(embeddings, N_CLUSTERS)

    # persisting the result
    save_results(df, labels, OUT_PATH)

    print(f"CLustered {len(df)} emails into {N_CLUSTERS} clusters")
    print(f"Saved result to {OUT_PATH}")



if __name__ == "__main__":
    main()