from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool
#save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    diagnosis: str
    recommendations: list[str]
    sources: list[str]

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
parser= PydanticOutputParser(pydantic_object=ResearchResponse)

prompt= ChatPromptTemplate.from_messages(
    [
        (
        "system",
        """
        You are a car mechanic that will help diagnose issues and give handy car advice.
        Answer the user query and use the necessary tools.
        Wrap the output in this format and provide no other text \n{format_instructions}
        """
        ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
    ]

).partial(format_instructions=parser.get_format_instructions())
#response = llm.invoke("How do I fix spark plugs?")
#print(response)

tools = [search_tool, wiki_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor= AgentExecutor(agent=agent, tools=tools, verbose=True)
query= input("Hey there! What question do you have about your car?")
raw_response = agent_executor.invoke({"query" : query})

try:
    structured_response=parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response.topic)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)