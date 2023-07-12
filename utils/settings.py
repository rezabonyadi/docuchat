from chromadb.config import Settings

db_persist_directory = 'db/'

CHROMA_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=db_persist_directory,
        anonymized_telemetry=False
)

