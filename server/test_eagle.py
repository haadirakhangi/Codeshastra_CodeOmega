import pveagle
from pvrecorder import PvRecorder

# Global variables for EagleRecognizer, PvRecorder, and EagleProfiler
eagle_recognizer = None
recorder = None
eagle_profiler = None

def read_speaker_profiles(speaker_profile_files):
    """
    Read speaker profiles from files and return a dictionary of speaker profiles and names.
    """
    speaker_profiles = {}
    speaker_names = {}

    for count, file_path in enumerate(speaker_profile_files):
        with open(file_path, 'rb') as f:
            profile_bytes = f.read()

        speaker_profile = pveagle.EagleProfile.from_bytes(profile_bytes)

        speaker_id = count
        speaker_profiles[speaker_id] = speaker_profile
        # speaker_names[speaker_profile] = input(f"Enter name for speaker {speaker_id}: ")

    return speaker_profiles, speaker_names

# def initialize_recognizer(access_key, speaker_profile_files):
    """
    Initialize the EagleRecognizer, PvRecorder, and EagleProfiler.
    """
    global eagle_recognizer, recorder, eagle_profiler

    # Read speaker profiles from files
    speaker_profiles, speaker_names = read_speaker_profiles(speaker_profile_files)

    # Create an EagleRecognizer instance
    try:
        eagle_recognizer = pveagle.create_recognizer(
            access_key=access_key,
            speaker_profiles=list(speaker_profiles.values()) # Pass the list of speaker profiles
        )
    except pveagle.EagleError as e:
        print(f"Error creating EagleRecognizer: {e}")
        return None

    # Get the required frame length from the EagleRecognizer
    frame_length = eagle_recognizer.frame_length

    # Set up the PvRecorder for recognition
    DEFAULT_DEVICE_INDEX = -1
    recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=frame_length  # Use the frame length required by the recognizer
    )

    # Create an EagleProfiler instance
    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
    except pveagle.EagleError as e:
        print(f"Error creating EagleProfiler: {e}")
        return None

    return speaker_profiles, speaker_names

def initialize_recognizer(access_key, speaker_profile_files,speaker_names):
    """
    Initialize the EagleRecognizer, PvRecorder, and EagleProfiler.
    """
    global eagle_recognizer, recorder, eagle_profiler

    # Read speaker profiles from files
    speaker_profiles, _ = read_speaker_profiles(speaker_profile_files)

    try:
        # Create an EagleRecognizer instance
        eagle_recognizer = pveagle.create_recognizer(
            access_key=access_key,
            speaker_profiles=list(speaker_profiles.values()) # Pass the list of speaker profiles
        )

        # Get the required frame length from the EagleRecognizer
        frame_length = eagle_recognizer.frame_length

        # Set up the PvRecorder for recognition
        DEFAULT_DEVICE_INDEX = -1
        recorder = PvRecorder(
            device_index=DEFAULT_DEVICE_INDEX,
            frame_length=frame_length  # Use the frame length required by the recognizer
        )

        # Create an EagleProfiler instance
        eagle_profiler = pveagle.create_profiler(access_key=access_key)

    except pveagle.EagleError as e:
        print(f"Error initializing recognizer: {e}")
        return None

    return speaker_profiles, speaker_names


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

def menu(speaker_profiles, speaker_names):
    """
    Display a menu and perform actions based on user input.
    """
    global eagle_recognizer, recorder

    while True:
        print("\nMenu:")
        print("1. Enroll a new member")
        print("2. Check who is speaking")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            enroll_new_member(speaker_profiles, speaker_names)
        elif choice == "2":
            try:
                recorder.start()
                print("Recorder Started")
                prev_score=None
                while True:
                    audio_frame = recorder.read()
                    scores = eagle_recognizer.process(audio_frame)
                    if scores!=prev_score:
                        print(scores)
                    prev_score=scores
                    highest_score = max(scores)
                    if highest_score > 0.5: # Adjust the threshold as needed
                        recognized_speaker_profile = list(speaker_names.keys())[scores.index(highest_score)]
                        recognized_speaker_name = speaker_names.get(recognized_speaker_profile)
                        print(f"Recognized speaker: {recognized_speaker_name}")
            finally:
                # Ensure resources are cleaned up
                recorder.stop()
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def main():
    # Replace with your actual access key
    access_key = "EPstqJaO6yGaeqsFhct1V1diEM0HvysEpmoxo04Os6mXFsEIA6Cj1A=="

    # Replace with the paths to the speaker profile files
    speaker_profile_files = ['Vedant.txt','Mehek.txt','Hastyy.txt']
    speaker_names = {0: 'Vedant', 1: 'Mehek', 2: 'Hastyy'}

    # Initialize speaker profiles and names dictionaries
    speaker_profiles, speaker_names = initialize_recognizer(access_key, speaker_profile_files, speaker_names)
    print("-------Done with init-------")
    print(speaker_profiles)
    print(speaker_names)
    if speaker_profiles and speaker_names:
        # Start the menu
        menu(speaker_profiles, speaker_names)
    else:
        print("Initialization failed.")
if __name__ == "__main__":
    main()
