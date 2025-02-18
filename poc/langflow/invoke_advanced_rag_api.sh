curl -X POST \
  http://18.232.184.248:7860/api/v1/run/e71306b6-e8df-4bdf-a871-03ec5049b4a8?stream=false \
  -H 'Content-Type: application/json'\
  -d '{"input_value": "How can the Clips be defined?",
  "output_type": "chat",
  "input_type": "chat",
  "tweaks": {
  "TextInput-R97Ag": {},
  "Prompt-YJndQ": {},
  "ChatInput-Wzq9A": {},
  "MemoryComponent-7bzTr": {},
  "OpenAIModel-l8vdA": {},
  "ChatOutput-awYSO": {},
  "AstraDB-ziXER": {},
  "OpenAIEmbeddings-9KcHT": {},
  "File-tN0Zd": {},
  "SplitText-tDnBJ": {},
  "AstraDBSearch-6W5fb": {}
}}'
  