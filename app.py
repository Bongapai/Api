# Import necessary libraries
from flask import Flask, request, jsonify
from pymongo import MongoClient
import face_recognition
import os

app = Flask(__name__)

# Set your MongoDB URI and database name here
MONGO_URI = "mongodb+srv://63310257:Newproject01@cluster01.oqzvrvv.mongodb.net/"
DB_NAME = 'face_database'
COLLECTION_NAME = 'face'

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Face Recognition
def get_face_embeddings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_embeddings = face_recognition.face_encodings(image, face_locations)
    return face_embeddings

# API Development
@app.route('/api/identify_face', methods=['POST'])
def identify_face():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    user_image = request.files['image']

    # user_image_name = os.path.splitext(user_image.filename)[0]
    user_image_name, _ = os.path.splitext(os.path.basename(user_image.filename))
    user_image_name = user_image_name.split('_')[0]

    user_image_embeddings = get_face_embeddings(user_image)

    if not user_image_embeddings:
        return jsonify({'error': 'No face found in the provided image'}), 400

    # Compare with stored face embeddings in MongoDB
    for entry in db.faces.find():
        # Use face_recognition.api.compare_faces for direct face comparison
        matches = face_recognition.api.compare_faces([entry['embedding']], user_image_embeddings[0], tolerance=0.5)
        if any(matches):
            return jsonify({'label_predict': entry['label'], 'label_actual': user_image_name})

    return jsonify({'label_predict': 'Unknown', 'label_actual': user_image_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))