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
    words = [lemmatizer.lemmatize(w) for w in words if w.lower() not in stop_words]
    return ' '.join(words)

# Extração de texto de arquivos
def extract_text(file):
    if file.filename.endswith('.pdf'):
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    return file.read().decode('utf-8')

# Limitar tamanho do texto
def limitar_texto(texto, max_tokens=512):
    palavras = texto.split()
    return ' '.join(palavras[:max_tokens]) if len(palavras) > max_tokens else texto

# Gerar resposta automática com Cohere
def gerar_resposta_cohere(texto, categoria):
    prompt = (
        f"Email recebido:\n{texto}\n"
        f"Categoria: {categoria}\n"
        f"Gere uma resposta automática breve e educada em português do Brasil para este email."
    )
    try:
        response = co.chat(message=prompt, temperature=0.7)
        return response.text.strip()
    except Exception as e:
        return f"Erro Cohere: {str(e)}"

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota de processamento
@app.route('/process', methods=['POST'])
def process():
    text = ""
    file = request.files.get('emailFile')
    email_text = request.form.get('emailText', '').strip()

    if file and file.filename != '':
        text = extract_text(file)
    elif email_text:
        text = email_text
    else:
        return jsonify({'error': 'Nenhum texto fornecido.'}), 400

    texto_limitado = limitar_texto(text)
    processed = preprocess_text(texto_limitado)
    result = classifier(processed)[0]
    categoria = "Produtivo" if result['label'] in ['4 stars', '5 stars'] else "Improdutivo"
    resposta = gerar_resposta_cohere(text, categoria)

    return jsonify({'categoria': categoria, 'resposta': resposta})

