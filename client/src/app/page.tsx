"use client";
import React, { useState, useRef } from "react";
import { Label } from "./components/ui/label";
import { Input } from "./components/ui/input";
import { cn } from "@/utils/cn";
import { IconMicrophone } from "@tabler/icons-react"; // Import the microphone icon
import axios from 'axios';

export default function SignupFormDemo() {
  const [formData, setFormData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    password: "",
    voice_data: null, // Add voice_data field for storing the audio file
  });
  const [recording, setRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const audioRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleStartRecording = () => {
    audioChunks.current = [];
    setRecordingTime(0);
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      audioRecorder.current = new MediaRecorder(stream);
      audioRecorder.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunks.current.push(e.data);
        }
      };
      audioRecorder.current.start();
      setRecording(true);
      startRecordingTimer();
    }).catch((err) => {
      console.error("Error accessing microphone:", err);
    });
  };

  const handleStopRecording = () => {
    if (audioRecorder.current && audioRecorder.current.state !== 'inactive') {
      audioRecorder.current.stop();
      audioRecorder.current.onstop = () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        setFormData((prevFormData) => ({
          ...prevFormData,
          voice_data: audioBlob,
        }));
        setRecording(false);
        stopRecordingTimer();
        console.log(formData);
        // alert("Recording done successfully"); // Show recording success message
        // Call submitForm function after recording is done
      };
    }
  };

  const startRecordingTimer = () => {
    const timerInterval = setInterval(() => {
      setRecordingTime((prevTime) => prevTime + 1);
    }, 1000); // Update recording time every second
    return () => clearInterval(timerInterval); // Cleanup function to clear the interval
  };

  const stopRecordingTimer = () => {
    setRecordingTime(0); // Reset recording time when stopped
  };

  const submitForm = async () => {
    try {
        const formDataObj = new FormData();
        formDataObj.append('firstname', formData.firstname);
        formDataObj.append('lastname', formData.lastname);
        formDataObj.append('email', formData.email);
        formDataObj.append('password', formData.password);

        const response = await axios.post("http://127.0.0.1:5000/register", formDataObj);
        console.log("Form submitted:", response.data);

        // Handle successful form submission here
        // Redirect to another route using window.location.href
        window.location.href = "http://127.0.0.1:8501"; // Change "/success" to your desired route
    } catch (error) {
        console.error("Error submitting form:", error);
        // Handle error here
    }
};


  return (
    <div className="max-w-md w-full mx-auto rounded-none md:rounded-2xl p-4 md:p-8 shadow-input bg-white dark:bg-black mt-12">
      <h2 className="font-bold text-xl text-neutral-800 dark:text-neutral-200">
        Welcome to Aura
      </h2>
      <p className="text-neutral-600 text-sm max-w-sm mt-2 dark:text-neutral-300">
        Sign Up to Aura
      </p>

      <form className="my-8">
        <div className="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2 mb-4">
          <LabelInputContainer>
            <Label htmlFor="firstname">First name</Label>
            <Input name='firstname' id="firstname" placeholder="Tyler" type="text" onChange={handleChange} value={formData.firstname} />
          </LabelInputContainer>
          <LabelInputContainer>
            <Label htmlFor="lastname">Last name</Label>
            <Input name='lastname' id="lastname" placeholder="Durden" type="text" onChange={handleChange} value={formData.lastname} />
          </LabelInputContainer>
        </div>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="email">Email Address</Label>
          <Input name='email' id="email" placeholder="projectmayhem@fc.com" type="email" onChange={handleChange} value={formData.email} />
        </LabelInputContainer>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="password">Password</Label>
          <Input name='password' id="password" placeholder="••••••••" type="password" onChange={handleChange} value={formData.password} />
        </LabelInputContainer>
        <LabelInputContainer className="mb-4">
          {recording ? (
            <button type="button" className="bg-red-500 hover:bg-red-600 text-white rounded-full w-12 h-12 flex justify-center items-center" onClick={handleStopRecording}>
              <span>Stop</span>
            </button>
          ) : (
            <div className="flex items-center space-x-3">
              <button type="button" className="bg-blue-500 hover:bg-blue-600 text-white rounded-full w-12 h-12 flex justify-center items-center" onClick={handleStartRecording}>
                <IconMicrophone size={24} />
              </button>
              <Label>Click to Record</Label>
            </div>
          )}
          <span className="ml-2">{formatTime(recordingTime)}</span> {/* Display live recording time */}
        </LabelInputContainer>

        <button type="button" onClick={submitForm} className="bg-gradient-to-br relative group/btn from-red-900 dark:from-zinc-900 dark:to-zinc-900 to-red-700 block dark:bg-zinc-800 w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]">
          Sign up &rarr;
        </button>

        <div className="bg-gradient-to-r from-transparent via-neutral-300 dark:via-neutral-700 to-transparent my-8 h-[1px] w-full" />
      </form>
    </div>
  );
}

const formatTime = (seconds: number) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`; // Format time as MM:SS
};

const LabelInputContainer = ({ children, className }: { children: React.ReactNode; className?: string; }) => {
  return (
    <div className={cn("flex flex-col space-y-2 w-full", className)}>
      {children}
    </div>
  );
};