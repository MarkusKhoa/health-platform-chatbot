from llama_index.core import SummaryIndex, Document, Settings, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline , IngestionCache
from llama_index.core.schema import TextNode
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import SummaryExtractor
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from config import STORAGE_PATH, CACHE_FILE_PATH, INDEX_STORAGE_PATH
from prompts import SUMMARY_PROMPT

import openai
import os

def ingest_data():
    docs = SimpleDirectoryReader(input_files=STORAGE_PATH,
                                 filename_as_id=True).load_data(show_progress=True,
                                                                 num_workers=-1)
    for object in docs[0]:
        print(object)
    
    try:
        ingestion_cache = IngestionCache.from_persist_path(CACHE_FILE_PATH)
        print(f"Running cache file to load data")
    except:
        ingestion_cache = ""
        print("Cache file not found. Loading data without caching...")
    
    ingestion_pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(chunk_size=500, chunk_overlap=20),
            SummaryExtractor(summaries=['self'], prompt_template = SUMMARY_PROMPT),
            OpenAIEmbedding()
        ], cache = ingestion_cache)
    
    nodes = ingestion_pipeline.run(show_progress = True,
                                   documents = docs, num_workers = -1)
    ingestion_pipeline.cache.persist(CACHE_FILE_PATH)
    return nodes

def indexing_builders(nodes):
    # In case the there is already an indexed storage
    try:
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_PATH)
        vector_index = load_index_from_storage (storage_context, index_id="vector")
        print ("Indices storage loaded successfully.")
    except:
        print("Indices storage is not available. Running from scratch.")
        storage_context = StorageContext.from_defaults()
        vector_index = VectorStoreIndex(nodes, storage_context=storage_context,
                                        index_id = "vector")
        vector_index.set_index_id("vector")
        storage_context.persist(INDEX_STORAGE_PATH)
    
    return storage_context, vector_index