import streamlit as st
import os
from utils import *
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import os
import openai
import pveagle
from pvrecorder import PvRecorder
import ast
import json
from openai import OpenAI
import time
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from tools import search_tool, weather_tool, calculator_tool, filter_emails_tool, draft_emails_tool, send_emails_tool, create_calender_events_tool, list_calender_events_tool
from agents import Agents
from tasks import Tasks
from crewai import Crew
from datetime import datetime, timedelta


float_init()

tools = [
    {
        'type': 'function',
        'function': {
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
    },
    {
        'type': 'function',
        'function': {
            'name': 'calculator_tool',
            'description': "Performs a specified mathematical operation like sum, minus, multiplication, division, etc. The input to this tool should be a mathematical expression, a couple examples are `200*7` or `5000/2*10`",
            'parameters': {
                'type': 'object',
                'properties': {
                    'operation': {
                        'description': 'The mathematical operations to perform',
                        'type': 'string'
                    }
                },
                'required': ['operation']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'filter_emails_tool',
            'description': "Use to filter out non-essential emails like newsletters and promotional content from Gmail."
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'draft_emails_tool',
            'description': "Use this tool only to draft an email for the user. Do not use it for sending an email.",
            'parameters': {
                'type': 'object',
                'properties': {
                    'message': {
                        'description': 'The message for the draft email',
                        'type': 'string'
                    },
                    'to': {
                        'description': 'The receivers of the email',
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'Email of each individual receiver'
                        }
                    },
                    'subject': {
                        'description': 'The subject of the email',
                        'type': 'string'
                    },
                    'cc': {
                        'description': 'Additional recipients who will receive a copy of the email (carbon copy)',
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'Email of each individual receiver'
                        }
                    },
                    'bcc': {
                        'description': 'Blind carbon copy; additional recipients who will receive a copy of the email without other recipients being aware',
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'Email of each individual receiver'
                        }
                    }

                },
                'required': ['message', 'to', 'subject']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'send_emails_tool',
            'description': "Use this tool when the user requests you to send an email. This tool creates and sends the email to the proper receipent",
            'parameters': {
                'type': 'object',
                'properties': {
                    'message': {
                        'description': 'The message for the email to be sent',
                        'type': 'string'
                    },
                    'to': {
                        'description': 'The receivers to whom the mail is to be sent',
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'Email of each individual receiver'
                        }
                    },
                    'subject': {
                        'description': 'The subject of the email',
                        'type': 'string'
                    },
                    'cc': {
                        'description': 'Additional recipients who will receive a copy of the email (carbon copy)',
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'Email of each individual receiver'
                        }
                    },
                    'bcc': {
                        'description': 'Blind carbon copy; additional recipients who will receive a copy of the email without other recipients being aware',
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'Email of each individual receiver'
                        }
                    }

                },
                'required': ['message', 'to', 'subject']
            }
        }
    },
        {
        'type': 'function',
        'function': {
            'name': 'create_calender_events_tool',
            'description': "Adds an event to the calender given the start datetime, end datetime and a summary of the event",
            'parameters': {
                'type': 'object',
                'properties': {
                    'start_datetime': {
                        'description': 'The start datetime of the event. Example: 2024-02-18T10:30:00',
                        'type': 'string'
                    },
                    'end_datetime': {
                        'description': 'The end datetime of the event. Example: 2024-02-18T10:30:00',
                        'type': 'string'
                    },
                    'summary': {
                        'description': 'The title of the event.',
                        'type': 'string'
                    },
                    'location': {
                        'description': 'The location of the event.',
                        'type': 'string'
                    },
                    'description': {
                        'description': 'The description of the event. Optional.',
                        'type': 'string'
                    },

                },
                'required': ['start_datetime', 'end_datetime', 'summary']
            }
        }
    },
        {
        'type': 'function',
        'function': {
            'name': 'list_calender_events_tool',
            'description': "Lists all the event from the user's personal calender between a start datetime and end datetime",
            'parameters': {
                'type': 'object',
                'properties': {
                    'start_datetime': {
                        'description': f"The start datetime of the event. Example: 2024-02-18T10:30:00. Today's datetime:{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}. Use the today's datetime if the user asks to create an event today.",
                        'type': 'string'
                    },
                    'end_datetime': {
                        'description': f"The end datetime of the event. Example: 2024-02-18T10:30:00. Today's datetime {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')} -- to be used when the user asks to create an event today",
                        'type': 'string'
                    },
                },
                'required': ['start_datetime', 'end_datetime']
            }
        }
    },
]


available_tools = {
    'search_tool': search_tool,
    'weather_tool': weather_tool,
    'calculator_tool': calculator_tool,
    'filter_emails_tool': filter_emails_tool,
    'draft_emails_tool': draft_emails_tool,
    'send_emails_tool': send_emails_tool,
    "create_calender_events_tool": create_calender_events_tool,
    "list_calender_events_tool": list_calender_events_tool
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
            elif tool_name=='calculator_tool':
                operation = json.loads(tool_args)['operation']
                output = tool_to_use(operation=operation)
            elif tool_name=='filter_emails_tool':
                output = tool_to_use()
            elif tool_name=='draft_emails_tool':
                message = json.loads(tool_args)['message']
                to = json.loads(tool_args)['to']
                subject = json.loads(tool_args)['subject']
                if 'cc' in json.loads(tool_args):
                    cc = json.loads(tool_args)['cc']
                    if 'bcc' in json.loads(tool_args):
                        bcc = json.loads(tool_args)['bcc']
                        output = tool_to_use(message=message, to=to, subject=subject, cc = cc, bcc=bcc)
                    else:
                        output = tool_to_use(message=message, to=to, subject=subject, cc = cc)
                else:
                    output = tool_to_use(message=message, to=to, subject=subject)                
            elif tool_name=='send_emails_tool':
                message = json.loads(tool_args)['message']
                to = json.loads(tool_args)['to']
                subject = json.loads(tool_args)['subject']
                if 'cc' in json.loads(tool_args):
                    cc = json.loads(tool_args)['cc']
                    if 'bcc' in json.loads(tool_args):
                        bcc = json.loads(tool_args)['bcc']
                        output = tool_to_use(message=message, to=to, subject=subject, cc = cc, bcc=bcc)
                    else:
                        output = tool_to_use(message=message, to=to, subject=subject, cc = cc)
                else:
                    output = tool_to_use(message=message, to=to, subject=subject) 
            elif tool_name=='list_calender_events_tool':
                start_datetime = json.loads(tool_args)['start_datetime']               
                end_datetime = json.loads(tool_args)['end_datetime']     
                output = tool_to_use(start_date = start_datetime, end_date=end_datetime)  
            elif tool_name=='create_calender_events_tool':
                start_datetime = json.loads(tool_args)['start_datetime']               
                end_datetime = json.loads(tool_args)['end_datetime']    
                summary = json.loads(tool_args)['summary']  
                if 'location' in json.loads(tool_args):
                    location = json.loads(tool_args)['location']
                    if 'description' in json.loads(tool_args):
                        description = json.loads(tool_args)['description']
                        output = tool_to_use(start_date = start_datetime, end_date=end_datetime, summary = summary, location=location, description=description)  
                    else:
                        output = tool_to_use(start_date = start_datetime, end_date=end_datetime, summary = summary, location=location)  

                else:
                    output = tool_to_use(start_date = start_datetime, end_date=end_datetime, summary = summary)  
  
                    
            if output:
                tools_outputs.append(
                    {'tool_call_id': tool_call_id, 'output': output})

    return CLIENT.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run_id, tool_outputs=tools_outputs)


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

# Initialize session state for managing chat messages
def initialize_session_state():
    assistant = CLIENT.beta.assistants.create(
        name="Aura",
        instructions="You are a helpful voice assistant. Think carefully about the user's request and assist the user. Make the best use of the tools provided to you. DO NOT use the tools if it is not required and you can answer the user by yourself.",
        model="gpt-3.5-turbo-1106",
        tools=tools
)
    thread = CLIENT.beta.threads.create()
    voice_state = False
    if 'assistant_id' not in st.session_state:
        st.session_state['assistant_id'] = assistant.id
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = thread.id
    if 'voice_state' not in st.session_state:
        st.session_state['voice_state'] = voice_state 
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
                print('RUN ERROR',run.message)
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
           
