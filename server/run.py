from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pveagle
from pvrecorder import PvRecorder
import time
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speaker_profiles.db'
db = SQLAlchemy(app)
access_key=os.environ.get('PICOVOICE_API')

class SpeakerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f"SpeakerProfile('{self.name}', '{self.profile_data}')"

@app.route('/enroll', methods=['GET','POST'])
def enroll_speaker():
    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
        recorder = PvRecorder(device_index=-1, frame_length=eagle_profiler.min_enroll_samples)
        recorder.start()  # Start recording
        enroll_percentage = 0.0
        while enroll_percentage < 100.0:
            audio_frame = recorder.read()  # Read audio frame from recorder
            enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
            print(f"Enrollment progress: {enroll_percentage}%")
        recorder.stop()  # Stop recording
        speaker_profile = eagle_profiler.export()
        # Save the speaker profile to the database
        new_speaker = SpeakerProfile(name="SpeakerName", profile_data=speaker_profile)
        db.session.add(new_speaker)
        db.session.commit()
        return jsonify({"message": "Speaker enrolled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
if __name__ == "__main__":
    app.run(debug=True)
