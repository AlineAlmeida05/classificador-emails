import cohere
from flask import Flask, request, render_template, jsonify
import os
import PyPDF2
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

co = cohere.Client('IxVcL0zkh1v158H2nEHvxYAkEy3yFdI0jWYHTzk8')

classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

def preprocess_text(text):
    stop_words = set(stopwords.words('portuguese'))
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w.lower() not in stop_words]
    return ' '.join(words)

def extract_text(file):
    if file.filename.endswith('.pdf'):
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    else:
        return file.read().decode('utf-8')

def limitar_texto(texto, max_tokens=512):
    palavras = texto.split()
    if len(palavras) > max_tokens:
        return ' '.join(palavras[:max_tokens])
    return texto

def gerar_resposta_cohere(texto, categoria):
    prompt = f"Email recebido:\n{texto}\nCategoria: {categoria}\nGere uma resposta automática breve e educada em português do Brasil para este email."
    try:
        response = co.chat(
            message=prompt,
            temperature=0.7
        )
        return response.text.strip()
    except Exception as e:
        return f"Erro Cohere: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = ""
    if 'emailFile' in request.files and request.files['emailFile'].filename != '':
        file = request.files['emailFile']
        text = extract_text(file)
    elif 'emailText' in request.form and request.form['emailText'].strip() != '':
        text = request.form['emailText']
    else:
        return jsonify({'error': 'Nenhum texto fornecido.'}), 400

    texto_limitado = limitar_texto(text)
    processed = preprocess_text(texto_limitado)
    result = classifier(processed)[0]
    categoria = "Produtivo" if result['label'] in ['4 stars', '5 stars'] else "Improdutivo"

    resposta = gerar_resposta_cohere(text, categoria)

    return jsonify({'categoria': categoria, 'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)