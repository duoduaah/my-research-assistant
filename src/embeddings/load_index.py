import faiss
import pickle
from pathlib import Path
from src.config import Config

s3 = Config.get_s3_client()

downloaded_index_path = f"{Config.DOWNLOADS_DIR}/{Config.INDEX_FILENAME}"
downloaded_metadata_path = f"{Config.DOWNLOADS_DIR}/{Config.METADATA_FILENAME}"

def get_index_metadata():
    s3.download_file(Config.S3_BUCKET_NAME, Key=Config.S3_INDEX_KEY, Filename=downloaded_index_path)
    s3.download_file(Config.S3_BUCKET_NAME, Config.S3_METADATA_KEY, downloaded_metadata_path)

    downloaded_index = faiss.read_index(downloaded_index_path)
    with open(downloaded_metadata_path, "rb") as f:
        downloaded_metadata = pickle.load(f)

    return downloaded_index, downloaded_metadata