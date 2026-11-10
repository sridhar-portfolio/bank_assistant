from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def rag_function(query, db_path, index_name, api_key):
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)

    db=FAISS.load_local(folder_path=db_path, index_name=index_name, embeddings=embeddings, allow_dangerous_deserialization=True)

    retrieved_docs = db.similarity_search(query, k=2)
    
    # taking first two retrieved documents
    retrieved_context=retrieved_docs[0].page_content + retrieved_docs[1].page_content


    augmented_prompt=f"""

    Given the context below answer the question.

    Question: {query} 

    Context : {retrieved_context}

    Remember to answer only based on the context provided and not from any other source. 

    If the question cannot be answered based on the provided context, 
    say I cannot find that information in our official product disclosure documents. 
    Would you like me to connect you with a customer service representative?.

    """

    llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=api_key
    )

    messages=[("human",augmented_prompt)]

    ai_msg = llm.invoke(messages)

    response=ai_msg.content

    return retrieved_context, response