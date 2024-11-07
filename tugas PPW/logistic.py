# Import necessary libraries
import pandas as pd
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Make sure you have the necessary nltk resources
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load the dataset (replace 'your_data.csv' with the path to your actual file)
df = pd.read_csv('berita_kompas.csv')

# Function to preprocess the text
def preprocess_text(text):
    # Step 1: Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Step 2: Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Step 3: Tokenize text
    words = word_tokenize(text.lower())
    
    # Step 4: Remove stopwords
    stop_words = set(stopwords.words('indonesian'))  # Use 'english' for English stopwords
    words = [word for word in words if word not in stop_words]
    
    # Join words back into a single string
    return ' '.join(words)

# Apply preprocessing to the 'isi' column
df['cleaned_isi'] = df['isi'].apply(preprocess_text)

# Step 1: Vectorize the 'cleaned_isi' column using TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=5000)  # Limit features to top 5000 for simplicity
X = vectorizer.fit_transform(df['cleaned_isi'])

# Step 2: Encode the 'kategori' column as the target variable
y = df['kategori']

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Step 5: Make predictions on the test set
y_pred = model.predict(X_test)

# Step 6: Evaluate the model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')

# Step 7: Show a classification report
print(classification_report(y_test, y_pred))
