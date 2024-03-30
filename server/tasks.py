from crewai import Task
from textwrap import dedent

class Tasks ():
    def filter_emails_task(agent, emails):
        return Task(
            description=dedent(f"""\
                Analyze a batch of emails and filter out
                non-essential ones such as newsletters, promotional content and notifications.
                Use your expertise in email content analysis to distinguish
                important emails from the rest, pay attention to the sender and avoind invalid emails.
                Make sure to filter for the messages actually directed at the user and avoid notifications.
                EMAILS
                {emails}
                """),
            expected_output = "Your final answer MUST be a the relevant thread_ids and the sender, use bullet points.",
            agent = agent
        )
    def draft_emails_task(agent, message, subject):
        return Task(
            description=dedent(f"""\
                ***Objective***: Compose a well-structured email draft in response to the user's message.

                ***Instructions***:
                Using your expertise in email drafting, create a professional and effective email based on the user's provided message. Pay close attention to clarity, tone, and organization. Ensure that the email addresses all necessary points and follows standard email conventions.

                

                ***Guidelines***:

                1. Begin with an appropriate greeting and address the recipient(s) respectfully.
                2. Clearly articulate the purpose or response to the user's request.
                3. Use concise and professional language throughout the email.
                4. Provide any necessary additional information or follow-up actions.
                5. Close the email politely and include any relevant sign-offs or contact information.
                
                ***Message***:
                {message}
                
                ***Subject***:
                {subject}
                """),
            expected_output = "Your final answer MUST only be the main body of the drafted message following the described format.",
            agent = agent
        )
    
    def send_emails_task(agent, message, subject):
        return Task(
            description=dedent(f"""\
                ***Objective***: Send a well-structured email draft in response to the user's message. Make sure it is detailed and covers all aspect of the user's request

                ***Instructions***:
                Using your expertise in email drafting, create a professional and effective email based on the user's provided message. Pay close attention to clarity, tone, and organization. Ensure that the email addresses all necessary points and follows standard email conventions.

                ***Guidelines***:

                1. Begin with an appropriate greeting and address the recipient(s) respectfully.
                2. Clearly articulate the purpose or response to the user's request.
                3. Use concise and professional language throughout the email.
                4. Provide any necessary additional information or follow-up actions.
                5. Close the email politely and include any relevant sign-offs or contact information.
                
                ***Message***:
                {message}
                
                ***Subject***:
                {subject}
                """),
            expected_output = "Your final answer MUST only be the main body of the drafted message following the described format.",
            agent = agent
        )
    
