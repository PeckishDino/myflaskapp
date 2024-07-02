# backend.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from HandID import classify_image

app = Flask(__name__)
CORS(app)

# Function to process a folder of images
def process_image_folder(folder_path):
    predictions = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(folder_path, filename)
            predicted_person = classify_image(img_path)
            predictions.append({'image': filename, 'predicted_person': predicted_person})
    return predictions

@app.route('/identify', methods=['POST'])
@cross_origin()
def identify_images():
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data from request body
        folder_path = data.get('folder_path')  # Get folder_path from JSON data

        if not folder_path:
            return jsonify({'error': 'Missing folder_path in request body'}), 400

        if not os.path.isdir(folder_path):
            return jsonify({'error': 'Invalid folder_path'}), 400

        # Process the folder and get predictions
        predictions = process_image_folder(folder_path)

        # Return predictions as JSON response
        return jsonify(predictions)

    return jsonify({'error': 'Method Not Allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
