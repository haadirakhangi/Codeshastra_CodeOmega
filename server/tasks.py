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
