from tools.files import create_file_tool, create_folder_tool, overwrite_file_tool
from tools.folder_content import folder_content_tool, file_content_tool, long_file_summary_tool, folder_tree_structure_tool
from tools.webpage_text import get_requests_text_tool
import langchain_visualizer
from langchain.agents import initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType

llm = OpenAI(temperature=0, max_tokens=2000)

tools = []
# tools = load_tools(["searx-search", "llm-math"], llm=llm,
#                    searx_host="http://localhost:8080", unsecure=True)

# tools.append(get_requests_text_tool())

# tools.append(folder_content_tool())
# tools.append(file_content_tool())
tools.append(long_file_summary_tool())
tools.append(folder_tree_structure_tool())

tools.append(create_file_tool())
# tools.append(create_folder_tool())
# tools.append(overwrite_file_tool())

chat_llm = ChatOpenAI(
    # streaming=True,
    model_name='gpt-4',
    temperature=0,
    max_tokens=1500,
)
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=False)
agent = initialize_agent(tools, chat_llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, memory=memory)


async def code_analyser_agent():
    return agent.run(
        "Write a documentation in markdown of project structure, how does project work, data flows, user flows, screens and features for the ios app project located in folder with path /project/path"
    )

langchain_visualizer.visualize(code_analyser_agent)
