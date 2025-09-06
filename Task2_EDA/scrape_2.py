import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df = pd.read_csv("data/processed/quotes_clean.csv")

print("Dataset Overview:")
print(df.info())
print("\nDescriptive Stats:")
print(df.describe(include="all"))

author_wc = df.groupby("author")["word_count"].mean().sort_values(ascending=False)

print("\nAverage word count per author:")
print(author_wc.head())

plt.figure(figsize=(10, 5))
author_wc.head(10).plot(kind="bar", color="skyblue")
plt.title("Top 10 Authors by Average Quote Length")
plt.ylabel("Average Word Count")
plt.xlabel("Author")
plt.xticks(rotation=45)
plt.show()

df["num_tags"] = df["tags_list"].apply(lambda x: len(eval(x)) if isinstance(x, str) else 0)

corr, p_corr = stats.pearsonr(df["word_count"], df["num_tags"])
print(f"\nCorrelation between quote length and number of tags: r={corr:.2f}, p={p_corr:.4f}")

plt.figure(figsize=(8, 5))
sns.scatterplot(x="word_count", y="num_tags", data=df, alpha=0.6)
plt.title("Quote Length vs. Number of Tags")
plt.xlabel("Word Count")
plt.ylabel("Number of Tags")
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df["word_count"], bins=20, kde=True, color="green")
plt.title("Distribution of Quote Lengths")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.show()
