from flask import Flask, request, jsonify
from flask_cors import CORS

from process import process_files, query_collection

app = Flask(__name__)
CORS(app)


@app.route('/process', methods=['POST'])
def process():
    documents = request.files.getlist('documents')
    process_files(documents)
    response = {'success': True}
    return jsonify(response)


@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('text')
    results = query_collection(query)
    return jsonify(results)



if __name__ == '__main__':
# Cambia el número de puerto a tu elección, por ejemplo, 5000
    app.run(host='0.0.0.0', port=5000)
    app.run()
