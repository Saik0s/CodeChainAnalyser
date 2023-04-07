
from langchain.agents import Tool
import os

def get_folder_content(path: str) -> str:
    try:
        dir_contents = os.listdir(path)
        mapped_list = list(map(str, dir_contents))
        for i in range(len(mapped_list)):
            if os.path.isdir(path + '/' + mapped_list[i]):
                mapped_list[i] += '/'
        joined_string = '\n'.join(mapped_list)
        return joined_string
    except Exception as e:
        return str(e)

def folder_content_tool() -> Tool:
    return Tool(name="folder_content", description="Get the contents of a folder, requires full path to the folder", func=get_folder_content)


def get_folder_tree_structure(path: str) -> str:
    import os
    def build_tree_structure(folder_path, relative_path, ignore_folders=False):
        tree_structure = ""
        folder_contents = os.listdir(folder_path)
        for content in folder_contents:
            content_path = os.path.join(folder_path, content)
            if os.path.isdir(content_path) and content not in ['SwiftPackageManager', '.tuist-bin', '.git']:
                if not ignore_folders:
                    tree_structure += relative_path + content + "/\n"
                tree_structure += build_tree_structure(content_path, relative_path + content + "/", ignore_folders)
            elif content.endswith('.swift') and os.path.isfile(content_path):
                tree_structure += relative_path + content + "\n"
        return tree_structure


    try:
        tree_structure = build_tree_structure(path, path + "/", ignore_folders=True)
        return tree_structure
    except Exception as e:
        return str(e)

def folder_tree_structure_tool() -> Tool:
    return Tool(name="folder_tree_structure", description="Get the tree structure of a folder, requires full path to the folder", func=get_folder_tree_structure)


def get_file_content(path: str) -> str:
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)


def file_content_tool() -> Tool:
    return Tool(name="file_content", description="Get the contents of a file, requires full path to the file", func=get_file_content)


def get_long_file_summary(path: str) -> str:
    content = get_file_content(path)

    from langchain.docstore.document import Document
    from langchain import OpenAI, PromptTemplate, LLMChain
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.chains.mapreduce import MapReduceChain
    from langchain.prompts import PromptTemplate
    from langchain.chains.summarize import load_summarize_chain

    llm = OpenAI(temperature=0)
    text_splitter = CharacterTextSplitter(separator="\n}\n")
    texts = text_splitter.split_text(content)
    docs = [Document(page_content=t) for t in texts]
    PROMPT = PromptTemplate(
        template="""Analyze and write explanation for the following code:


        ```
        {text}
        ```


        EXPLANATION:""",
        input_variables=["text"]
    )
    COMBINE_PROMPT = PromptTemplate(
        template="""Analyze and write explanation for the following code explanations:


        ```
        {text}
        ```


        EXPLANATION:""",
        input_variables=["text"]
    )
    chain = load_summarize_chain(OpenAI(temperature=0, max_tokens=2000), chain_type="map_reduce",
                                 return_intermediate_steps=True, map_prompt=PROMPT, combine_prompt=COMBINE_PROMPT)
    output = chain({"input_documents": docs}, return_only_outputs=True)
    return output["output_text"]

def long_file_summary_tool() -> Tool:
    return Tool(name="long_file_summary", description="Get the summary of the content a long file, requires full path to the file", func=get_long_file_summary)
