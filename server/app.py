import streamlit as st
import os
from utils import *
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import os
import openai
import ast
import json
from openai import OpenAI
import time
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from tools import search_tool, weather_tool

float_init()

tools = [
    {
        'type': 'function',
        'function': 
         {
              'name': 'search_tool',
              'description': 'Get information about anything from the internet',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'query': {
                          'description': 'The query to use to search on the internet',
                          'type': 'string'
                          }
                      },
                    'required': ['query']
                  }
              }
        },
    {
        'type': 'function',
        'function': {
            'name': 'weather_tool',
            'description': 'Fetch current temperature for given coordinates.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'latitude': {
                        'description': 'Latitude of the location to fetch weather data for',
                        'type': 'number'
                        },
                    'longitude': {
                        'description': 'Longitude of the location to fetch weather data for',
                        'type': 'number'
                        }
                    },
                  'required': ['latitude', 'longitude']
                }
            }
        }
]

available_tools = {
    'search_tool': search_tool,
    'weather_tool': weather_tool,
}

def wait_on_run(run_id, thread_id):
        while True:
            run = CLIENT.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id,
            )
            print('RUN STATUS', run.status)
            time.sleep(0.5)
            if run.status in ['failed', 'completed', 'requires_action']:
                return run

def submit_tool_outputs(thread_id, run_id, tools_to_call):
    tools_outputs = []
    with st.spinner("Taking Action..."):     
        for tool in tools_to_call:
            output = None
            tool_call_id = tool.id
            tool_name = tool.function.name
            tool_args = tool.function.arguments
            print('TOOL CALLED:', tool_name)
            print('ARGUMENTS:', tool_args)
            tool_to_use = available_tools.get(tool_name)
            if tool_name =='search_tool':
                query = json.loads(tool_args)['query']
                output = tool_to_use(query)
            elif tool_name=='weather_tool':
                latitude = json.loads(tool_args)['latitude']
                longitude = json.loads(tool_args)['longitude']
                output = tool_to_use(latitude=latitude, longitude=longitude)
            if output:
                tools_outputs.append(
                    {'tool_call_id': tool_call_id, 'output': output})

    return CLIENT.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run_id, tool_outputs=tools_outputs)

# Initialize session state for managing chat messages
def initialize_session_state():
    assistant = CLIENT.beta.assistants.create(
        name="Aura",
        instructions="You are a helpful voice assistant. Think carefully about the user's request and assist the user. Make the best use of the tools provided to you.",
        model="gpt-3.5-turbo-1106",
        tools=tools
)
    thread = CLIENT.beta.threads.create()

    if 'assistant_id' not in st.session_state:
        st.session_state['assistant_id'] = assistant.id
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = thread.id
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How may I assist you today?"}]

initialize_session_state()

st.title("OpenAI Conversational Chatbot 🤖")
# Create a container for the microphone and audio recording
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

   
if audio_bytes:
    assistant_id = st.session_state['assistant_id']
    thread_id = st.session_state['thread_id']
    with st.spinner("Transcribing..."):
        # Write the audio bytes to a temporary file
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Convert the audio to text using the speech_to_text function
        transcript = speech_to_text(webm_file_path)

        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)
            
 
if st.session_state.messages[-1]["role"] != "assistant":
    message = CLIENT.beta.threads.messages.create(
        thread_id= thread_id,
        role="user",
        content= st.session_state.messages[-1]['content'],
    )
    run = CLIENT.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id= assistant_id,
    )
    run = wait_on_run(run.id, thread_id)
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            if run.status == 'failed':
                print(run.error)
            elif run.status == 'requires_action':
                run = submit_tool_outputs(thread_id, run.id, run.required_action.submit_tool_outputs.tool_calls)
                run = wait_on_run(run.id,thread_id)
            messages = CLIENT.beta.threads.messages.list(thread_id= thread_id,order="asc")
            content = None
            for thread_message in messages.data:
                content = thread_message.content
            chatbotReply = content[0].text.value
            print('CHATBOT REPLY', chatbotReply)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(chatbotReply)
            autoplay_audio(audio_file)
        st.write(chatbotReply)
        st.session_state.messages.append({"role": "assistant", "content": chatbotReply})
        os.remove(audio_file)
           