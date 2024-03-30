from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pveagle
from pvrecorder import PvRecorder
from utils import *
import os
# from flask_socketio import SocketIO, emit
import wave
from flask_bcrypt import Bcrypt


Voice_state=False


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speaker_profiles.db'
db = SQLAlchemy(app)
access_key=os.environ.get('PICOVOICE_API')
bcrypt = Bcrypt(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    voice_data = db.Column(db.LargeBinary, nullable=True)

    def _repr_(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"
    
# Create the database tables based on your models
# with app.app_context():
    # db.create_all()
# class SpeakerProfile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     profile_data = db.Column(db.LargeBinary, nullable=False)

#     def _repr_(self):
#         return f"SpeakerProfile('{self.name}', '{self.profile_data}')"

# Route for user registration

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = Users(firstname=data['firstname'], lastname=data['lastname'], email=data['email'], password=hashed_password)

    # Save a sample text file to large binary field
    file_content = b'This is a sample text file content.'
    new_user.voice_data = file_content

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    user = Users.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

def split_audio_into_frames(audio_file, frame_duration_ms):
    frames = []
    with wave.open(audio_file, 'rb') as wf:
        frame_size = int(frame_duration_ms * wf.getframerate() / 1000)  # Calculate frame size in samples
        while True:
            frame_data = wf.readframes(frame_size)
            if not frame_data:
                break
            frames.append(frame_data)
    return frames

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




# from faster_whisper import WhisperModel


# def WhisperShit():
#     model = WhisperModel(model_size, device="cpu", compute_type="int8")
        

#---------------------PORCUPINE-------------------------
import pvporcupine
from pvrecorder import PvRecorder

def get_mic_state():
    # Set up the PvRecorder with the minimum enrollment samples
    DEFAULT_DEVICE_INDEX = -1
    recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=512
    )


    porcupine = pvporcupine.create(
    access_key='V8ZLdwTq3DHObCXeTZjWPOJs1ciBCmjvjIJNE7O3HTDQQXD2kuBcog==',
    keyword_paths=['Hey-Aura_en_windows_v3_0_0.ppn']
    #   keywords=['picovoice', 'bumblebee','Hey Aura'],
    #   model_path='Hey-Aura_en_windows_v3_0_0.ppn'
    )


    recorder.start()
    while True:
        audio_frame = recorder.read()
        keyword_index = porcupine.process(audio_frame)

        if keyword_index == 0:
            print('Hey Aura detected')
            return 1
        else:
            # get_mic_state()
            return 0

#----------------Detect Voice for 5 secs-------------------

import pvcobra
def voice_activity_detection(access_key):
    # Initialize the Cobra engine
    cobra = pvcobra.create(access_key)
    
    # Initialize the recorder
    recorder = PvRecorder(frame_length=cobra.frame_length)
    recorder.start()
    print("Listening for voice activity...")
    voice_activity_detected = False
    start_time = time.time()

    while True:
        frame = recorder.read()
        # Process the frame with Cobra for voice activity detection
        voice_probability = cobra.process(frame)

        if voice_probability > 0.5: # Assuming a threshold of 0.5 for voice activity
            voice_activity_detected = True
            Voice_state=True
            print("Voice activity detected.")
            start_time = time.time()
        elif voice_activity_detected and time.time() - start_time > 5:
            print("No voice for 5 secs. \n Stopping...")
            Voice_state=False
            break

    # Stop the recorder
    recorder.stop()