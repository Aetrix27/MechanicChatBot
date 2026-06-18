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
    try: 
        llm = ChatAnthropic(model="claude-opus-4-8")

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a car mechanic. Give clear, readable advice."),
            ("human", "{query}")
        ])

        chain = prompt | llm
        response = chain.invoke({"query": query})

        return response.content
    except Exception as e:
        return "Error parsing response", e, "Raw Response - ", response
    """
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
    """

