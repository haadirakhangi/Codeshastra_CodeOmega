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

        def email_draft_agent():
             return Agent(
            role='Senior Email Drafter',
            goal="Creates a draft of an email based on the user's request.",
            llm= ChatOpenAI(model_name='gpt-3.5-turbo-1106'),
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
            llm= ChatOpenAI(model_name='gpt-3.5-turbo-1106'),
            backstory=dedent ("""
                ***Background***:
                In this role, you possess substantial expertise in crafting compelling email content. Your proficiency lies in interpreting user requests accurately and skillfully composing emails with clear and nuanced language. You utilize your seasoned experience to comprehend the user's request thoroughly. You employ nuanced language to effectively convey the intended message. You also send the mail to the proper receipent.
            """),
            verbose=True,
            allow_delegation=False
        )