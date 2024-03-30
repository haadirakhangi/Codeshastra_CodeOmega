from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pveagle
from pvrecorder import PvRecorder
import time
import os
from flask_socketio import SocketIO, emit
import wave

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speaker_profiles.db'
db = SQLAlchemy(app)
access_key=os.environ.get('PICOVOICE_API')



class SpeakerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_data = db.Column(db.LargeBinary, nullable=False)

    def _repr_(self):
        return f"SpeakerProfile('{self.name}', '{self.profile_data}')"



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

def read_speaker():
    

# @app.route('/enroll', methods=['GET']) #HASTANSHHHHH; 
# def enroll_speaker():
#     audio_frames = split_audio_into_frames("test.wav", 1000)  # Split audio into 1-second frames
#     eagle_profiler = pveagle.create_profiler(access_key=access_key)
#     enroll_percentage = 0.0
#     while enroll_percentage < 100.0:  # Read audio frame from recorder
#         enroll_percentage, feedback = eagle_profiler.enroll(audio_frames[0])
#         print(f"Enrollment progress: {enroll_percentage}%")
#         print(feedback)
#     speaker_profile = eagle_profiler.export()
#     print(speaker_profile)
#     # Save the speaker profile to the database
#     # new_speaker = SpeakerProfile(name="Hatim", profile_data=speaker_profile)
#     # db.session.add(new_speaker)
#     # db.session.commit()
#     return jsonify({"message": "Speaker enrolled successfully"}), 200

@app.route('/enroll', methods=['GET']) #HASTANSHHHHH; 
def enroll_new_member(speaker_profiles, speaker_names):
    """
    Enroll a new member and update the speaker profiles and names dictionaries.
    """
    global eagle_profiler, recorder

    speaker_name = input("Enter name for the new speaker: ")

    # Set up the PvRecorder with the minimum enrollment samples
    DEFAULT_DEVICE_INDEX = -1
    recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle_profiler.min_enroll_samples
    )

    # Start recording
    recorder.start()

    try:
        # Enroll the speaker
        enroll_percentage = 0.0
        while enroll_percentage < 100.0:
            audio_frame = recorder.read()
            enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
            print(f"Enrollment progress: {enroll_percentage}%")
            print(feedback)

        # Export the speaker profile
        speaker_profile = eagle_profiler.export()

        # speaker_profile = eagle_profiler.export()
        a=speaker_profile.to_bytes()
        print(a)
        with open(f'{speaker_name}.txt', 'wb') as f:
            f.write(a)

        # Add the new speaker profile and name to dictionaries
        speaker_id = len(speaker_profiles)
        speaker_profiles[speaker_id] = speaker_profile
        speaker_names[speaker_profile] = speaker_name

        print(f"Enrollment completed for speaker {speaker_name}.")
    
    finally:
        # Stop recording and clean up resources
        recorder.stop()
        # recorder.delete()


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
                    recognized_speaker = SpeakerProfile.query.filter_by(profile_data=recognized_profile_data).first()
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
if _name_ == "_main_":
    app.run(debug=True)