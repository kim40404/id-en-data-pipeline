import polars as pl
import logging

logger = logging.getLogger(__name__)

def validate_dataset(df: pl.DataFrame):
    logger.info("Memulai Enterprise Data Validation...")
    
    # Check 1: No missing values
    # In Polars, df.null_count().sum_horizontal()[0] gives total nulls
    null_counts = df.null_count().sum_horizontal()[0] if hasattr(df.null_count(), 'sum_horizontal') else df.null_count().sum(axis=1)[0]
    
    if null_counts > 0:
        logger.error(f"Validasi Gagal: Ditemukan {null_counts} data kosong!")
        raise ValueError("Data masih mengandung nilai kosong (null)!")
        
    # Check 2: No duplicates
    duplicates = df.is_duplicated().sum()
    if duplicates > 0:
        logger.error(f"Validasi Gagal: Ditemukan {duplicates} baris duplikat!")
        raise ValueError("Data masih mengandung baris ganda (duplikat)!")
        
    logger.info("Validasi LULUS 100%! Dataset sudah suci bersih dan siap disuapkan ke AI.")
    return True

if __name__ == "__main__":
    print("Modul Validator siap digunakan.")
