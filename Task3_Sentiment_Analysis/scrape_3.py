import pandas as pd
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score,recall_score,f1_score,precision_score
import warnings
from sklearn.exceptions import UndefinedMetricWarning

df = pd.read_csv("data/processed/quotes_clean.csv")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()

df["clear_text"] = df["text"].apply(clean_text)

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.05:
        return "positive"
    elif polarity < -0.05:
        return "negative"
    else:
        return "neutral"

df["sentiment"] = df["clear_text"].apply(get_sentiment)

X = df["clear_text"]
y = df["sentiment"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

warnings.filterwarnings('ignore', category=UndefinedMetricWarning)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

df.to_csv("data/processed/quotes_with_sentiment.csv", index=False)
print("\nSaved with sentiment at data/processed/quotes_with_sentiment.csv")