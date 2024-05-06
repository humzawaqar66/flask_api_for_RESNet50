from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer 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"}  # Replace with your actual API token

def query_model(image_data):
    response = requests.post(API_URL, headers=headers, data=image_data)
    return response.json()

@app.route('/predict', methods=['GET', 'POST'])

def predict():
    if request.method == 'GET':
        return jsonify({'error': "Send a POST request with an image to get predictions."})

    if request.method == 'POST':
        files = request.files.getlist('file')
        
        if len(files) > 1:
            return jsonify({'error': 'Multiple files selected,plz select one'})

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = files[0]

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        output = query_model(file.read())
        print(output)
        labels = []
        for i in output:
            labels.append(i['label'])
        return jsonify({'labels': labels})


if __name__ == '__main__':
    app.run(debug=True)