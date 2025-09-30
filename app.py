import os
import cohere
import PyPDF2
import nltk
from flask import Flask, request, render_template, jsonify
from transformers import pipeline
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Baixar recursos do NLTK
nltk.download('stopwords')
nltk.download('wordnet')

# Inicializar Flask
app = Flask(__name__)

# Inicializar Cohere com chave segura
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

# Inicializar classificador
classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Pré-processamento de texto
def preprocess_text(text):
    stop_words = set(stopwords.words('portuguese'))
    lemmatizer = WordNetLemmatizer()
    words = text.split
