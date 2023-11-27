from flask import Flask, render_template, request, jsonify
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import os
import json
import html  # HTML modülünü ekleyin

app = Flask(__name__)

# OpenAI API anahtarını ekleyin
os.environ["OPENAI_API_KEY"] = "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"
openai_api_key = os.environ.get("OPENAI_API_KEY", None)

# Veri yükleme ve indeks oluşturma
root_dir = "C:\\Users\\sanemk\\Desktop\\colab\\CHATBOT\\content\\gdrive\\MyDrive"
pdf_folder_path = os.path.join(root_dir, 'data')

# openai_api_key ve lang parametrelerini tanımlayın
loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn), openai_api_key=openai_api_key, lang='tr') for fn in os.listdir(pdf_folder_path)]
index = VectorstoreIndexCreator().from_loaders(loaders)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query_text = request.form['query']
    result = index.query(query_text)
    
    # HTML modülünü kullanarak Unicode karakterleri düzgün bir şekilde işleyin
    result_html = html.escape(result)
    
    return jsonify({'result': result_html})

if __name__ == '__main__':
    app.run(debug=True)
