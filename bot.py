import os
import re
from dotenv import load_dotenv

from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()

# Set API Keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ZAPIER_NLA_API_KEY"] = os.getenv("ZAPIER_NLA_API_KEY")

# Define the system prompt template
template_1 = """
Do not generate user responses on your own and avoid repeating questions.

You are a helpful personal assistant. Every time you greet, you must say, "Hi, This is Sanchuka's Personal Assistance, How may I help you today?" Your only task is to help users schedule a service appointment with Sanchuka.
Sanchuka provides services like solution consulting, full-stack development, and AI/ML development. His availability is from 8 am to 5 pm IST every day.
Collect the following information one by one:
1. Full name
2. Service type
3. Location
4. Date and time
5. Email address

Display the collected information in this format:
Full Name: 
Service Type:
Location:
Date and Time (in 24-hour IST format):
Email Address:

{chat_history}
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template_1)
human_template = "{query}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# Initialize the chat model and memory
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize Zapier tools
zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
tools = toolkit.get_tools()

# Chat Chain: Process user queries
def gpt_response(query):
    chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory)
    response = chain.run(query)
    return response

# Extract user info from the conversation
def extract_information(conversation, pattern):
    for line in conversation:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

# Main bot response function
def bot_response(query):
    # Get the GPT response from the model
    response = gpt_response(query)

    # Extract the required information
    pattern_name = r'Full Name:\s*(.*)'
    pattern_service = r'Service Type:\s*(.*)'
    pattern_location = r'Location:\s*(.*)'
    pattern_datetime = r'Date and Time:\s*(.*)'
    pattern_email = r'Email Address:\s*(.*)'

    conversation = [response]

    name = extract_information(conversation, pattern_name)
    service = extract_information(conversation, pattern_service)
    location = extract_information(conversation, pattern_location)
    datetime = extract_information(conversation, pattern_datetime)
    email = extract_information(conversation, pattern_email)

    # Check if all information is collected
    if name and service and location and datetime and email:
        details = f"""
        Here are the details collected:
        Full Name: {name}
        Service Type: {service}
        Location: {location}
        Date and Time: {datetime}
        Email Address: {email}
        
        Thank you for connecting.
        """
        return details

    # Otherwise, return the model's response to continue the conversation
    return response
