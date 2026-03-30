from langchain_community.llms import Ollama

# Initialize the LLaMA model
llm = Ollama(model="llama3.1")

# Test with a sample prompt
response = llm.invoke("Tell me a joke")
print(response)