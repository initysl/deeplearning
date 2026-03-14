# Goal: Build a sentiment analysis  model that classifies movie/product reviews as positive or negative.
from datasets import load_dataset
from collections import Counter
import re

dataset = load_dataset("imdb")

def clean_text(text):
    # Remove special characters and numbers
    text = re.sub(r"<br\s*/?>", " ", text)  # Replace <br> tags with space
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower().strip()
    return text

# Tokenize all reviews
def tokenize(text):
    return clean_text(text).split()

# Build vocabulary from taining set 
counter = Counter()
for sample in dataset["train"]:
    counter.update(tokenize(sample["text"])) # type: ignore

# Keep only top 10,000 most frequent words
VOCAB_SIZE = 10000
vocab = ["<PAD>", "<UNK>"] + [word for word, _ in counter.most_common(VOCAB_SIZE - 2)]
word2idx = {word: idx for idx, word in enumerate(vocab)}

print(f"Vocabulary size: {len(vocab)}")
print(f"Example — 'good': {word2idx.get('good')}")

sample = dataset["train"][0]["text"]
cleaned_sample = clean_text(sample)
# print("Cleaned Text:", cleaned_sample[:200])