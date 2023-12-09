import pyterrier as pt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

pt.init()

# Define the URL to fetch data (hypothetical example)
source_url = "https://example.com/rare-coins"

# Fetch data from the website using PyTerrier
def fetch_data_from_website(url):
    dataset = pt.fetch_data(url)
    return dataset

# Fetch data from the source (hypothetical data)
data = fetch_data_from_website(source_url)

# Preprocess fetched data
texts = [item['description'].lower() for item in data]
tfidf_vectorizer = TfidfVectorizer()
text_features = tfidf_vectorizer.fit_transform(texts)

prices = np.array([item['price'] for item in data]).reshape(-1, 1)
price_scaler = StandardScaler()
prices_scaled = price_scaler.fit_transform(prices)

feature_vectors = np.hstack((text_features.toarray(), prices_scaled))

# Calculate cosine similarity matrix
similarity_matrix = cosine_similarity(feature_vectors)

# Function to recommend similar coins based on user query
def recommend_coins(user_query, data, tfidf_vectorizer, price_scaler, similarity_matrix, top_n=5):
    user_query = user_query.lower()
    query_vector = tfidf_vectorizer.transform([user_query])
    query_features = np.hstack((query_vector.toarray(), np.array([[0]])))

    query_similarity = cosine_similarity(query_features, feature_vectors)
    top_similar_indices = np.argsort(query_similarity[0])[::-1][:top_n]

    recommended_coins = [data[i]['description'] for i in top_similar_indices]
    return recommended_coins

# User query
user_query = "rare gold coin"

# Get recommendations using fetched data
recommendations = recommend_coins(user_query, data, tfidf_vectorizer, price_scaler, similarity_matrix)
print("Recommended coins:", recommendations)
