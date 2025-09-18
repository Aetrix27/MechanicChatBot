from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool
import json
#save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    diagnosis: str
    recommendations: list[str]
    sources: list[str]

def askQuestion(query: str):
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    parser= PydanticOutputParser(pydantic_object=ResearchResponse)

    prompt= ChatPromptTemplate.from_messages(
        [
            (
            "system",
            """
            You are a car mechanic that will help diagnose issues and give handy car advice.
            Answer the user query and use the necessary tools. You must ONLY output valid JSON. Do not include any text outside the JSON.
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
    raw_response = agent_executor.invoke({"query" : query})

    try:
        output_text = raw_response["output"][0]["text"]
        parsed = json.loads(output_text)             # now it's a dict
        
        
        output_strings=[topic,diagnosis,recommendations]
        recommendations_str = "\n".join(recommendations)
        diagnosis_str = "\n".join(recommendations)
        topic_str = "\n".join(recommendations)

        #.strip("'\"").encode().decode("unicode_escape")

        #structured_response = parser.parse(output_text)
        topic = parsed["topic"]
        diagnosis = parsed["diagnosis"]
        recommendations = parsed["recommendations"]
        return str(topic+"\n"+diagnosis+"\n"+recommendations)
    except Exception as e:
        return "Error parsing response", e, "Raw Response - ", raw_response