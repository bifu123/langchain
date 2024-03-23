################ 量化后数据保存路径 ###
db_path = "./chroma_db"
#####################################

################ 源文档路径 ##########
data_path = "./data"
#####################################


################ gemini api key #####
GOOGLE_API_KEY = "YOUR GEMINI API KEY"
#gemini api key的申请地址：https://makersuite.google.com/app/prompts/new_freeform ，条件：拥有google帐号
#####################################



################ 模型配置 ############
#本地量化模型
embedding_ollama_conf = {
    "base_url": "http://192.168.66.24:11434", 
    "model": "nomic-embed-text"
}
#goole量化模型
embedding_google_conf = {
    "model": "models/embedding-001"
} 
#本地语言模型 
llm_ollama_conf = {
    "base_url": "http://192.168.66.26:11434", 
    "model": "llama2-chinese"
}
#线上google gemini语言模型
llm_gemini_conf = {
    "model": "gemini-pro",
    "temperature": 0.7
} 
#####################################




################ 模型选择 ############
model_choice = {
    "embedding":"goole", # embedding: ollama | google
    "llm": "gemini" # llm: ollama | gemini
}
#####################################





