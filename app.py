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
    words = text.split()
    processed = [lemmatizer.lemmatize(w.lower()) for w in words if w.lower() not in stop_words]
    return " ".join(processed)

# Rota de exemplo (você pode adaptar conforme sua lógica)
@app.route("/")
def home():
    return "Aplicação Flask rodando com sucesso no Render!"

# Rodar servidor Flask na porta esperada pelo Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
