from datasets import load_dataset
import pandas as pd

dataset = load_dataset("benstaf/FNSPID-filtered-nasdaq-100", split="train")
df = dataset.to_pandas()
df = df.drop("Unnamed: 0", axis=1)

cols = ["Date", "Article_title", "Stock_symbol", "Url", "Article"]
df = df[cols]
df = df.sort_values("Date", ascending=False)

# Convert column names to lowercase
df.columns = df.columns.str.lower()

print("Original data info:")
print(df.info())

# Remove rows with null values in any of the columns
print(f"\nBefore removing nulls: {len(df):,} rows")
df_clean = df.dropna().copy()
print(f"After removing nulls: {len(df_clean):,} rows")
print(f"Removed {len(df) - len(df_clean):,} rows with null values")

# Additional filtering: Remove articles with empty or null body content
print(f"\nBefore filtering empty articles: {len(df_clean):,} rows")
df_clean = df_clean[
    (df_clean['article'].notna()) &
    (df_clean['article'].str.strip() != '')
].copy()
print(f"After filtering empty articles: {len(df_clean):,} rows")
print(f"Removed {len(df.dropna()) - len(df_clean):,} rows with empty article body")

# Remove duplicate article titles
print(f"\nBefore removing duplicates: {len(df_clean):,} rows")
df_clean = df_clean.drop_duplicates(subset=['article_title'], keep='first').copy()
print(f"After removing duplicates: {len(df_clean):,} rows")
print(f"Removed duplicate article titles")

print(f"\nStock symbols in dataset:")
print(df_clean["stock_symbol"].unique()[:20])

print(f"\nFiltered dataset:")
print(df_clean.head())
print(df_clean.info())

sm_size = 5000
# Sample for working with smaller dataset
if len(df_clean) > sm_size:
    sm_df = df_clean.sample(n=sm_size, random_state=42)  # Added random_state for reproducibility
else:
    sm_df = df_clean.copy()

print(f"\nSample dataset info:")
print(sm_df.info())

# Optional: Check for any remaining data quality issues
print(f"\nData quality check on sample:")
print(f"Empty Article titles: {sm_df['article_title'].str.strip().eq('').sum()}")
print(f"Empty Articles: {sm_df['article'].str.strip().eq('').sum()}")
print(f"Articles shorter than 50 chars: {(sm_df['article'].str.len() < 50).sum()}")

# Analyze article lengths
print(f"\nArticle length analysis:")
article_lengths = sm_df['article'].str.len()
print(f"Article length statistics:")
print(f"  Min length: {article_lengths.min():,} characters")
print(f"  Max length: {article_lengths.max():,} characters")
print(f"  Mean length: {article_lengths.mean():.0f} characters")
print(f"  Median length: {article_lengths.median():.0f} characters")
print(f"  95th percentile: {article_lengths.quantile(0.95):.0f} characters")
print(f"  99th percentile: {article_lengths.quantile(0.99):.0f} characters")

# Show distribution of article lengths
print(f"\nArticle length distribution:")
print(f"  < 1,000 chars: {(article_lengths < 1000).sum():,} articles")
print(f"  1,000 - 5,000 chars: {((article_lengths >= 1000) & (article_lengths < 5000)).sum():,} articles")
print(f"  5,000 - 10,000 chars: {((article_lengths >= 5000) & (article_lengths < 10000)).sum():,} articles")
print(f"  10,000 - 20,000 chars: {((article_lengths >= 10000) & (article_lengths < 20000)).sum():,} articles")
print(f"  >= 20,000 chars: {(article_lengths >= 20000).sum():,} articles")

# Truncate articles that are too long for embeddings
# Common embedding model limits:
# - OpenAI text-embedding-ada-002: ~8,000 tokens (~32,000 chars)
# - OpenAI text-embedding-3-small: ~8,000 tokens (~32,000 chars)
# - OpenAI text-embedding-3-large: ~8,000 tokens (~32,000 chars)
# - Sentence transformers: varies, often 512-4096 tokens

MAX_ARTICLE_LENGTH = 20000  # Adjust this based on your embedding model's limits
print(f"\nTruncating articles longer than {MAX_ARTICLE_LENGTH:,} characters...")

# Count articles that will be truncated
articles_to_truncate = (sm_df['article'].str.len() > MAX_ARTICLE_LENGTH).sum()
print(f"Articles that will be truncated: {articles_to_truncate:,}")

if articles_to_truncate > 0:
    # Create a copy for truncation
    sm_df_truncated = sm_df.copy()

    # Truncate long articles
    sm_df_truncated['article'] = sm_df_truncated['article'].apply(
        lambda x: x[:MAX_ARTICLE_LENGTH] + "..." if len(x) > MAX_ARTICLE_LENGTH else x
    )

    # Show before/after statistics
    original_lengths = sm_df['article'].str.len()
    truncated_lengths = sm_df_truncated['article'].str.len()

    print(f"\nTruncation results:")
    print(f"  Original max length: {original_lengths.max():,} characters")
    print(f"  Truncated max length: {truncated_lengths.max():,} characters")
    print(f"  Articles truncated: {articles_to_truncate:,}")
    print(f"  Average reduction: {(original_lengths - truncated_lengths).mean():.0f} characters")

    # Use truncated version for export
    sm_df = sm_df_truncated
else:
    print("No articles needed truncation.")

# Also truncate the full dataset if needed
print(f"\nTruncating full dataset if needed...")
full_articles_to_truncate = (df_clean['article'].str.len() > MAX_ARTICLE_LENGTH).sum()
print(f"Full dataset articles that will be truncated: {full_articles_to_truncate:,}")

if full_articles_to_truncate > 0:
    df_clean_truncated = df_clean.copy()
    df_clean_truncated['article'] = df_clean_truncated['article'].apply(
        lambda x: x[:MAX_ARTICLE_LENGTH] + "..." if len(x) > MAX_ARTICLE_LENGTH else x
    )
    df_clean = df_clean_truncated

# Export to Parquet files
print(f"\nExporting data to Parquet files...")

# Export full filtered dataframe
full_filename = "data/fin_news_articles.parquet"
df_clean.to_parquet(full_filename, index=False)
print(f"Exported full filtered dataset to: {full_filename}")

# Export small sample dataframe
sample_filename = f"data/fin_news_articles_{sm_size}.parquet"
sm_df.to_parquet(sample_filename, index=False)
print(f"Exported sample dataset to: {sample_filename}")

print(f"\nExport complete!")
print(f"Full dataset: {len(df_clean):,} rows")
print(f"Sample dataset: {len(sm_df):,} rows")
