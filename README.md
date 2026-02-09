# msgvault - ML Experiments on Archived Email Data

This repository contains a small, time-boxed ML experiment using msgvault as a Data Source to explore semantic grouping of unstructured email data.


## Goal 

This exercise explores how unstructured email data archived via msgvault can be used for lightweight semantic analysis, and how quickly meaningful insights can be extracted using simple, interpretable ML techniques.


## What I tried 

- Used msgvault as a local data source to extract a sample of archived emails.
- Built a lightweight ML pipeline to:
    - construct text representations from email subject + snippet 
    - compute semantic embeddings
    - cluster emails using K-Means
- Performed cluset inspection to understand dominating cluster themes and noise.


## Why this approach

- Email data is unstructured and unlabeled, making unsupervised methods appropriate for such scenarios.
- Sentence embeddings provide a strong semantic signal with minimal feature engineering.
- K-means was chosen for its simplicity and interpretability under time constraints.
- The experiment was intentionally kept small (~300 emails) to remain focused and pragmatic.


## Results 

- Emails grouped into 6 semantically interpretable cluster such as:
    - e-commerce transactions
    - product recommendations
    - urgency / action-required messages
    - educational notifications
    - promotional emails 
- One mixed cluster emerged, which is expected given short snippets and broadly informational content.

Detailed examples and plots are available in the [`results/`](results/) directory.


## What I learned 

- Even with limited context (subject + snippet), embeddings capture intent effectively.
- Unsupervised clustering on real email data naturally produces both clean and mixed clusters.
- Data quality (encoding artifacts, truncated snippets, mixed threads) plays a major role in the outcomes.
- Clear scoping and inspections are critical when labels are unavailable.


## Data Handling Note

This repository does not include any raw or processed email data.
Both the msgvault database and derived CSV files are excluded to
avoid committing personal or sensitive information.

Running the scripts locally will regenerate the processed datasets.

---

## How to Run

1. Place a copy of your local `msgvault.db` in:
```bash
data/raw/msgvault.db
```

2. Create a virtual enviroment and install dependencies:
```bash
uv init msgvault-ml
uv pip install -r requirements.txt
```

3. Extract emails:
```bash
uv run python -m scripts.extract_emails
```

4. Generate embeddings and clusters:
```bash
uv run python -m scripts.embed_and_cluster
```

4. Inspect results:
- Open `notebooks/cluster_inspections.ipynb`
- View files under `results/`

---

## Repo Structure

```pgsql

msgvault-ml/
├── README.md                     # primary entry point
├── docs/
│   └── msgvault_exploration.md   # earlier system exploration
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── extract_emails.py
│   └── embed_and_cluster.py
├── notebooks/
│   └── cluster_inspection.ipynb
├── results/
│   ├── cluster_examples.md
│   └── cluster_distribution.png
├── requirements.txt
└── .gitignore

```

---

## Additional Notes

For details on msgvault setup, architecture observations, and system explorations, see [`docs/msgvault_exploration.md`](docs/msgvault_exploration.md).