from flask import Flask, request, jsonify
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from unidecode import unidecode
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # CORS politikalarını etkinleştir
# OpenAI API anahtarı
os.environ["OPENAI_API_KEY"] = "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"
openai_api_key = os.environ.get("OPENAI_API_KEY", None)

# Veri yükleme ve indeks oluşturma
root_dir = "C:\\Users\\sanemk\\Desktop\\colab\\CHATBOT\\content\\gdrive\\MyDrive"
pdf_folder_path = os.path.join(root_dir, 'data')



loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn), openai_api_key=openai_api_key, lang='tr') for fn in os.listdir(pdf_folder_path)]
index = VectorstoreIndexCreator().from_loaders(loaders)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        try:
            data = request.json
            query_text = data['query']

            result = index.query(query_text)

            # Encode as UTF-8 and then decode
            result_ascii = unidecode(result)

            return jsonify({'result': result_ascii})

        except Exception as e:
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)