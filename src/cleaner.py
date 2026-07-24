import polars as pl
import logging
from datasets import load_dataset

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatasetCleaner:
    def __init__(self, hf_repo: str):
        self.hf_repo = hf_repo
        
    def run_pipeline(self):
        logger.info(f"Mulai menyedot data dari {self.hf_repo}...")
        
        # 1. Download dari Hugging Face
        hf_dataset = load_dataset(self.hf_repo, split="train")
        df = pl.from_arrow(hf_dataset.data.table)
        logger.info(f"Berhasil mengunduh {df.shape[0]} baris data kotor.")
        
        # 2. Proses Cleaning
        logger.info("Mulai proses pembersihan (menghapus duplikat & baris kosong)...")
        df_clean = df.drop_nulls().unique()
        logger.info(f"Dataset bersih tersisa: {df_clean.shape[0]} baris. Membuang {df.shape[0] - df_clean.shape[0]} baris sampah.")
        
        return df_clean

    def export_and_push(self, df_clean: pl.DataFrame, target_repo: str):
        from datasets import Dataset
        logger.info(f"Mengekspor dataset dan mem-push ke Hugging Face ({target_repo})...")
        
        # Convert Polars DataFrame to Hugging Face Dataset
        final_dataset = Dataset.from_pandas(df_clean.to_pandas())
        
        # Push to Hub
        final_dataset.push_to_hub(target_repo)
        logger.info("Sukses! Dataset berhasil di-push ke Hugging Face.")

if __name__ == "__main__":
    cleaner = DatasetCleaner(hf_repo="Kimsang766/agentic-ai-instructions-id-en")
    clean_df = cleaner.run_pipeline()
    
    # Validasi sebelum export
    from validator import validate_dataset
    if validate_dataset(clean_df):
        # Push ke repository baru (tambahkan -cleaned)
        cleaner.export_and_push(clean_df, target_repo="Kimsang766/agentic-ai-instructions-id-en-cleaned")
    
    print("Pipeline selesai.")
