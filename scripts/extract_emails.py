import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional
import unicodedata
import re


# ------------------
# Configuration
# ------------------

DB_PATH = Path("data/raw/msgvault.db")
OUT_PATH = Path("data/processed/emails_sample.csv")
EMAIL_LIMIT = 300

QUERY = """
SELECT
    id,
    conversation_id,
    sent_at,
    subject,
    snippet,
    is_from_me
FROM messages
WHERE message_type = 'email'
    AND deleted_at IS NULL
    AND (subject IS NOT NULL OR snippet IS NOT NULL)
ORDER BY sent_at DESC
LIMIT ?;
"""



# ------------------------
# Helpets
# -------------------------


def clean_text(text: str) -> str:
    """
    Normalize unicode forms and many invisible oddities safely
    deals with MOJIBAKEs and excessive spacing
    
    Returns:
        a clean string
    """
    if not text:
        return ""
    
    # normalize unicode forms
    text = unicodedata.normalize("NFKC", text)

    # Remove non-printable characters
    text = "".join(ch for ch in text if ch.isprintable())

    # remove excessive spacing
    text = re.sub(r"\s+", " ", text).strip()

    return text



def build_text(subject: Optional[str], snippet: Optional[str]) -> str:
    """
    Combines subject and snippet while handling NULLs 
    
    Returns:
        text: str
    """

    subject = subject or ""
    snippet = snippet or ""

    text = f"Subject: {subject}\n\n{snippet}"

    return clean_text(text)



def extract_emails(db_path: Path, limit: int) -> pd.DataFrame:
    """
    Extract a sample of emails from the msgvault SQLite DB.
    The database is treated as read only

    Returns:
        df: Dataframe
    """

    if not db_path.exists():
        raise FileNotFoundError(f"Database is not found at {db_path}")
    
    # db connection and query 
    with sqlite3.connect(db_path) as con:
        df = pd.read_sql_query(QUERY, con, params=(limit,))

    # check whether the query returned data or not
    if df.empty:
        raise ValueError(f"Query returned no data. Check DB contents or filters.")

    # instead of taking all the content, we'll cluster on the basis of
    # subject + snippet as considering email content
    df['text'] = df.apply(
        lambda row: build_text(row['subject'], row['snippet']),
        axis = 1 # to choose row 
    )

    return df


def save_dataset(df: pd.DataFrame, out_path: Path) -> None:
    """
    Save the dataset as csv in persitent disk
    """

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)



################
# Main Function
################

def main() -> None:
    df = extract_emails(DB_PATH, EMAIL_LIMIT)
    save_dataset(df, OUT_PATH)

    print(f"Extracted {len(df)} emails to {OUT_PATH}")


if __name__ == "__main__":
    main()