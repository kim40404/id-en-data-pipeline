# Bilingual Dataset Cleaner (ID-EN)

An enterprise-grade data pipeline to clean, normalize, and validate Indonesian-English bilingual datasets using Polars and Great Expectations.

## Pipeline Steps
1. **Load:** Download raw datasets from Hugging Face.
2. **Clean:** Remove duplicates and handle missing values.
3. **Normalize:** Standardize text formatting.
4. **Validate:** Run Great Expectations to ensure 100% data quality.
5. **Export:** Push the cleaned dataset back to Hugging Face.
