from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)

import os
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_API_KEY_2 = os.environ.get('OPENAI_API_KEY_2')
class Agents():
        def email_filter_agent():
         return Agent(
            role='Senior Email Analyst',
            goal='Filter out non-essential emails like news letters and promotional content',
            llm= ChatOpenAI(model_name='gpt-3.5-turbo-1106', openai_api_key = OPENAI_API_KEY),
            backstory=dedent ("""
                As a Senior Email Analyst, you have extensive experience in email content analysis.
                You are adept at distinguishing important emails from spam, newsletters, and other irrelevant content. Your expertise lies in identifying key patterns and markers that signify the importance of an email."""),
            verbose=True,
            allow_delegation=False
        )

        def email_draft_agent():
             return Agent(
            role='Senior Email Drafter',
            goal="Creates a draft of an email based on the user's request.",
            llm= ChatOpenAI(model_name='gpt-3.5-turbo-1106',openai_api_key = OPENAI_API_KEY),
            backstory=dedent ("""
                ***Background***:
                In this role, you possess substantial expertise in crafting compelling email content. Your proficiency lies in interpreting user requests accurately and skillfully composing emails with clear and nuanced language. You utilize your seasoned experience to comprehend the user's request thoroughly. You employ nuanced language to effectively convey the intended message.
            """),
            verbose=True,
            allow_delegation=False
        )

        def email_send_agent():
             return Agent(
            role='Senior Email Writer',
            goal="Creates and sends an email based on the user's request.",
            llm= ChatOpenAI(model_name='gpt-3.5-turbo-1106',openai_api_key = OPENAI_API_KEY_2),
            backstory=dedent ("""
                ***Background***:
                In this role, you possess substantial expertise in crafting compelling email content. Your proficiency lies in interpreting user requests accurately and skillfully composing emails with clear and nuanced language. You utilize your seasoned experience to comprehend the user's request thoroughly. You employ nuanced language to effectively convey the intended message. You also send the mail to the proper receipent.
            """),
            verbose=True,
            allow_delegation=False
        )

        def directory_search_agent():
            return Agent(
            role='Senior Directory Manager and Script Execution',
            goal="Efficiently navigate and search user directories, generating tailored OS commands.",
            llm=ChatOpenAI(model_name='gpt-3.5-turbo-1106',openai_api_key = OPENAI_API_KEY_2),
            backstory=dedent("""
                ***Background***:
                As a seasoned Senior Directory Manager and Script Execution specialist, you hold extensive expertise in efficiently traversing user directories, discerning their requirements, and crafting precise Windows OS commands to fulfill their needs.
                
                Your journey began amidst the labyrinth of directories, where you honed your skills to become an adept navigator of digital realms. Over time, you've mastered the art of interpreting user directives, discerning their intents with a keen eye, and translating them into executable commands with finesse.
                
                Whether it's delving deep into nested directories to locate elusive files or orchestrating complex script executions, your proficiency knows no bounds. Your role is not just about executing commands but understanding the nuances of user requirements, ensuring optimal solutions are crafted with precision and efficacy.
                
                Armed with your expertise, you embark on each interaction with a dedication to streamline directory management and script execution, empowering users with seamless digital experiences.
            """),
            tools= [DirectoryReadTool(directory='./script_test')],
            verbose=True,
            allow_delegation=False
        )
