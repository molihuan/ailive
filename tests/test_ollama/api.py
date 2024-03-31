import ollama
response = ollama.chat(model='qwen:4b-chat', messages=[
  {
    'role': 'user',
    'content': '你好',
  },
])
print(response['message']['content'])