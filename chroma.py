
import chromadb
import json


chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=["元龙居士的头发是白的", "元龙居士今年45岁了"],
    metadatas=[{"source": "doc1"}, {"source": "doc2"}],
    ids=["id1", "id2"]
)

results = collection.query(
    query_texts=["元龙居士的头发是什么颜色?"],
    n_results=2
)

# 格式化输出 JSON 数据
formatted_data = json.dumps(results, indent=4, ensure_ascii=False)
print(formatted_data)
