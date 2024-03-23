from dal import *


#加载embedding
vectorstore_from_db = Chroma(
    persist_directory = db_path,         # Directory of db
    embedding_function = embedding   # Embedding model
)
retriever = vectorstore_from_db.as_retriever()
# print(retriever)



#################### 问答推理 ##################
#创建prompt模板
template = """Answer the question a full sentence, based only on the following context and tel me the answer in Chinese:
{context}
Question: {question}
"""

template_cn = """请根据以下上下文完整地回答问题，并用中文告诉我答案:
{context}
{question}
"""

#由模板生成prompt
prompt = ChatPromptTemplate.from_template(template) 

retriever=vectorstore_from_db.as_retriever()
output_parser = StrOutputParser()

 
#创建chain
chain = RunnableMap({
    "context": lambda x: retriever.get_relevant_documents(x["question"]),
    "question": RunnablePassthrough()
}) | prompt | llm | output_parser
 
while True:
    q_input = input("请输入问题：")
    query = {"question": q_input}
    print(chain.invoke(query))
    
    # vectorstore_from_db.delete_collection()