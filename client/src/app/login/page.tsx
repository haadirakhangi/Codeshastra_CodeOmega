"use client";
import React, { useState, useRef } from "react";
import { Label } from "../components/ui/label";
import { Input } from "../components/ui/input";
import { cn } from "@/utils/cn";
import { IconMicrophone } from "@tabler/icons-react"; // Import the microphone icon
import axios from 'axios';

export default function SignupFormDemo() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    voice_data: null, // Add voice_data field for storing the audio file
  });


  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };



  const submitForm = async () => {
    try {
      const formDataObj = new FormData();
      formDataObj.append('email', formData.email);
      formDataObj.append('password', formData.password);
      
      const response = await axios.post("http://127.0.0.1:5000/login", formDataObj);
      console.log("Form submitted:", response.data);
      
      // Handle successful form submission here
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
        Login to Aura
      </p>

      <form className="my-8">
        <LabelInputContainer className="mb-4">
          <Label htmlFor="email">Email Address</Label>
          <Input name='email' id="email" placeholder="projectmayhem@fc.com" type="email" onChange={handleChange} value={formData.email}/>
        </LabelInputContainer>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="password">Password</Label>
          <Input name='password' id="password" placeholder="••••••••" type="password" onChange={handleChange} value={formData.password}/>
        </LabelInputContainer>
        <button type="button" onClick={submitForm} className="bg-gradient-to-br relative group/btn from-red-900 dark:from-zinc-900 dark:to-zinc-900 to-red-700 block dark:bg-zinc-800 w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]">
         Log In &rarr;
        </button>

        <div className="bg-gradient-to-r from-transparent via-neutral-300 dark:via-neutral-700 to-transparent my-8 h-[1px] w-full" />
      </form>
    </div>
  );
}

const LabelInputContainer = ({ children, className }: { children: React.ReactNode; className?: string; }) => {
  return (
    <div className={cn("flex flex-col space-y-2 w-full", className)}>
      {children}
    </div>
  );
};
