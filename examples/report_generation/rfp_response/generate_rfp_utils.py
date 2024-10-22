from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core import SummaryIndex
from llama_cloud.client import LlamaCloud
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
from llama_index.core.tools import FunctionTool
from llama_index.core.schema import NodeWithScore, Document
from llama_index.llms.openai import OpenAI
from typing import Optional, List

import os
from pathlib import Path


def generate_tools(
    index_name: str, 
    index_id: str,
    project_name: str, 
    organization_id: Optional[str] = None,
    api_key: Optional[str] = None,
    data_out_dir: str = "data_out_rfp",
    llama_cloud_base_url: str = "https://api.cloud.llamaindex.ai"
) -> List[FunctionTool]:
    """Generate tools."""
    api_key = api_key or os.environ["LLAMA_CLOUD_API_KEY"]
    index = LlamaCloudIndex(
      name=index_name, 
      project_name=project_name,
      organization_id=organization_id,
      api_key=api_key
    )
    
    # setup client
    client = LlamaCloud(
        token=api_key,
        base_url=llama_cloud_base_url
    )
    pipeline_docs = client.pipelines.list_pipeline_documents(index_id)
    summary_llm = OpenAI(model="gpt-4o-mini")
    
    # generate summaries and attach as metadata on the docs
    if "summary" not in pipeline_docs[0].metadata:
        for pipeline_doc in pipeline_docs:
            doc = Document.from_cloud_document(pipeline_doc)
            index = SummaryIndex([doc])
            response = index.as_query_engine(llm=summary_llm).query(
                "Generate a short 1-2 line summary of this file to help inform an agent on what this file is about."
            )
            print(f">> Generated summary: {str(response)}")
            # file_dicts[f]["summary"] = str(response)
            # change the metadata of the document
            pipeline_doc.metadata["summary"] = str(response)
        
        # upsert new documents to vector database
        upserted_docs = client.pipelines.upsert_batch_pipeline_documents(index_id, request=pipeline_docs)
    


    # generate tools
    DOC_RETRIEVE_PREFIX = """\
    Synthesizes an answer to your question by feeding in in the entire relevant document as context. Best used for higher-level summarization options.
    Do NOT use if answer can be found in a specific chunk of a given document. Use the chunk_query_engine instead for that purpose.
    
    Document: {file_name}
    """
    
    CHUNK_RETRIEVE_PREFIX = """\
    Synthesizes an answer to your question by feeding in relevant chunks of a document as context. Best used for questions that are more pointed in nature.
    Do NOT use if the question asks seems to require a general summary of any given document. Use the doc_query_engine instead for that purpose.
    
    Document: {file_name}
    """
    
    
    # function tools
    def generate_tool(
        file: str, 
        file_description: Optional[str] = None,
        retrieve_document: bool = False
    ):
        """Return a function that retrieves only within a given file."""
        filters = MetadataFilters(
            filters=[
                MetadataFilter(key="file_path", operator=FilterOperator.EQ, value=file),
            ]
        )
    
        def chunk_retriever_fn(query: str) -> str:
            retriever = index.as_retriever(similarity_top_k=5, filters=filters)
            nodes = retriever.retrieve(query)
    
            full_text = "\n\n========================\n\n".join(
                [n.get_content(metadata_mode="all") for n in nodes]
            )
    
            return full_text
    
        # define name as a function of the file
        fn_name = Path(file).stem + "_retrieve"
    
        tool_description_tmpl = DOC_RETRIEVE_PREFIX if retrieve_document else CHUNK_RETRIEVE_PREFIX
        tool_description = tool_description_tmpl.format(file_name=file)
        if file_description is not None:
            tool_description += f"\n\nFile Description: {file_description}"
    
        tool = FunctionTool.from_defaults(
            fn=chunk_retriever_fn, name=fn_name, description=tool_description
        )
    
        return tool
    
    
    # generate tools - include both chunk-level and document-level retrieval
    tools = []
    for pipeline_doc in pipeline_docs:
        # chunk-level tool
        file_name = pipeline_doc.metadata["file_name"]
        summary = pipeline_doc.metadata["summary"]
        tools.append(generate_tool(file_name, file_description=summary))
        # document-level tool
        tools.append(
            generate_tool(
                file_name, 
                file_description=summary,
                retrieve_document=True
            )
        )
    return tools