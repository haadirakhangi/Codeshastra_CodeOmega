from io import BytesIO
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pveagle
from pvrecorder import PvRecorder
from flask_socketio import SocketIO
from utils import *
import os
# from flask_socketio import SocketIO, emit
import wave
from flask_bcrypt import Bcrypt
from models import db, Users, Device
from flask_cors import CORS,cross_origin
from flask import send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speaker_profiles.db'
db.init_app(app)
CORS(app)
access_key=os.environ.get('PICOVOICE_API')
bcrypt = Bcrypt(app)

    
# Create the database tables based on your models
# with app.app_context():
#     db.create_all()
# class SpeakerProfile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     profile_data = db.Column(db.LargeBinary, nullable=False)

#     def _repr_(self):
#         return f"SpeakerProfile('{self.name}', '{self.profile_data}')"

# Route for user registration

def split_audio_into_frames(audio_file, frame_duration_ms):
    frames = []
    with wave.open(r'C:\Users\Hastansh\Desktop\CodeShastra\Codeshastra_CodeOmega\server\voices\nagmail.com_blob.wav', 'rb') as wf:
        frame_size = int(frame_duration_ms * wf.getframerate() / 1000)  # Calculate frame size in samples
        while True:
            frame_data = wf.readframes(frame_size)
            if not frame_data:
                break
            frames.append(frame_data)
    return frames


def enroll(path):
    audio_frames = split_audio_into_frames(path, 1000)  # Split audio into 1-second frames
    print(path)
    # if not audio_frames:
    #     print("No audio frames found.")
    #     return None
    
    eagle_profiler = pveagle.create_profiler(access_key=access_key)
    enroll_percentage = 0.0
    while enroll_percentage < 100.0 and audio_frames:  # Check audio_frames to avoid index out of range
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frames[0])
        print(f"Enrollment progress: {enroll_percentage}%")
        print(feedback)
    if audio_frames:  # Check again before exporting
        speaker_profile = eagle_profiler.export()
        speaker_profile.to_bytes()
        return speaker_profile
    else:
        print("Error: No audio frames available for enrollment.")
        return None


@app.route('/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    # Get data from the form
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    audio_blob = request.files['voice_data'] if 'voice_data' in request.files else None

    # Check if the form data is valid
    if not firstname or not lastname or not email or not password or not audio_blob:
        return jsonify({'error': 'Incomplete form data or missing audio blob'}), 400

    base_folder='voices'
    root_directory = os.getcwd() 

    os.makedirs(os.path.join(root_directory, base_folder), exist_ok=True)  # Create the base folder if it doesn't exist

    # Generate a unique filename using the email and a secure filename method
    filename = secure_filename(f"{email}_blob.wav")

    # Define the folder path to save audio files based on the base folder and user's email
    audio_folder = os.path.join(root_directory, base_folder)
    os.makedirs(audio_folder, exist_ok=True)  # Create the user's folder if it doesn't exist

    # Create the full file path by joining the audio folder and the generated filename
    file_path = os.path.join(audio_folder, filename)

    # Save the audio blob to the specified file path
    audio_blob.save(file_path)


    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_voice=enroll(file_path)
    # Create a new user with the provided data and save the audio file path
    new_user = Users(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=hashed_password,
        voice_data=user_voice  # Save the audio file path in the database
    )

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/get_audio/<user_id>', methods=['GET'])
def get_audio(user_id):
    # Assuming you have a User model with a voice_data field
    user = Users.query.get(user_id)
    if not user or not user.voice_data:
        return jsonify({'error': 'User not found or audio data missing'})

    # Serve the audio file as a response
    return send_file(BytesIO(user.voice_data), mimetype='audio/wav')

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    user = Users.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# def split_audio_into_frames(audio_file, frame_duration_ms):
#     frames = []
#     with wave.open(audio_file, 'rb') as wf:
#         frame_size = int(frame_duration_ms * wf.getframerate() / 1000)  # Calculate frame size in samples
#         while True:
#             frame_data = wf.readframes(frame_size)
#             if not frame_data:
#                 break
#             frames.append(frame_data)
#     return frames

def save_speaker(name,eagle_profiler):
    speaker_profile = eagle_profiler.export()
    a=speaker_profile.to_bytes()
    print(a)
    with open(f'{name}.txt', 'wb') as f:
        f.write(a)

# def read_speaker():
    

@app.route('/enroll', methods=['GET']) #HASTANSHHHHH; 
def enroll_speaker():
    audio_frames = split_audio_into_frames("test.wav", 1000)  # Split audio into 1-second frames
    eagle_profiler = pveagle.create_profiler(access_key=access_key)
    enroll_percentage = 0.0
    while enroll_percentage < 100.0:  # Read audio frame from recorder
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frames[0])
        print(f"Enrollment progress: {enroll_percentage}%")
        print(feedback)
    speaker_profile = eagle_profiler.export()
    print(speaker_profile)
    # Save the speaker profile to the database
    # new_speaker = SpeakerProfile(name="Hatim", profile_data=speaker_profile)
    # db.session.add(new_speaker)
    # db.session.commit()
    return jsonify({"message": "Speaker enrolled successfully"}), 200

@app.route('/recognize', methods=['POST'])
def recognize_speaker():
    try:
        eagle = pveagle.create_recognizer(access_key=access_key, speaker_profiles=[])
        recorder_r = PvRecorder(device_index=-1, frame_length=512)
        recorder_r.start()  # Start recording
        print("Recording for speaker recognition...")
        print()

        consecutive_recognitions = 0
        recognition_threshold = 4  # Number of consecutive recognitions to consider

        while True:
            audio_frame = recorder_r.read()  # Read audio frame from recorder
            scores = eagle.process(audio_frame)
            highest_score = max(scores)
            print(highest_score)
            print(f"Highest score: {highest_score}")  # Debugging line
            if highest_score > 0.5:
                consecutive_recognitions += 1
                if consecutive_recognitions >= recognition_threshold:
                    print("Speaker recognized for 4 seconds straight. Stopping recording.")
                    # Retrieve recognized speaker profile data from the database
                    recognized_profile_data = audio_frame  # Placeholder, replace with actual profile data
                    recognized_speaker = Users.query.filter_by(profile_data=recognized_profile_data).first()
                    if recognized_speaker:
                        recognized_speaker_name = recognized_speaker.name
                        print(f"Recognized speaker: {recognized_speaker_name}")
                        return jsonify({"message": "Speaker recognized successfully", "name": recognized_speaker_name}), 200
                    else:
                        print("Recognized speaker not found in the database.")
            else:
                consecutive_recognitions = 0
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        recorder_r.stop()
        eagle.delete()
if __name__== "__main__":
    app.run(debug=True)
    socketio.run(app, debug=True)