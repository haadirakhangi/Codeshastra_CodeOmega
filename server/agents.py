from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
class Agents():
        def email_filter_agent():
         return Agent(
            role='Senior Email Analyst',
            goal='Filter out non-essential emails like news letters and promotional content',
            llm= ChatOpenAI(model_name='gpt-3.5-turbo-1106'),
            backstory=dedent ("""
                As a Senior Email Analyst, you have extensive experience in email content analysis.
                You are adept at distinguishing important emails from spam, newsletters, and other irrelevant content. Your expertise lies in identifying key patterns and markers that signify the importance of an email."""),
            verbose=True,
            allow_delegation=False
        )