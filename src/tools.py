from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core import StorageContext, load_index_from_storage
from config import INDEX_STORAGE_PATH

storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_PATH)
vector_index = load_index_from_storage(storage_context, index_id="vector")

query_engine = vector_index.as_query_engine(similarity_top_k = 5)
query_tool = QueryEngineTool(query_engine=query_engine,
                             metadata=ToolMetadata(description=("""Provide knowledge about mental disease information
                                                                regarding to the DMS-5 data standard. Must use context of
                                                                the questions as input for tool.
                                                                """
                                                                )))

# def save_evaluation_results(score, content, total_prediction_num, username):
#     current_time = 
