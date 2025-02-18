# embed langflow in application
from langflow.load import run_flow_from_json
TWEAKS = {
  "TextInput-d9uWe": {},
  "Prompt-pXJUm": {},
  "ChatInput-V3GiW": {},
  "MemoryComponent-92uim": {},
  "OpenAIModel-LNdHO": {},
  "ChatOutput-xhZQ6": {},
  "AstraDB-xeAMv": {},
  "OpenAIEmbeddings-mlo75": {},
  "File-bjRrw": {},
  "SplitText-QqwIs": {},
  "AstraDBSearch-0nsMH": {}
}

result = run_flow_from_json(flow="langflow_open_ai_astra_db_tutorial_work.json",
                            input_value="Please explain CLIP experiment short and simple.",
                            tweaks=TWEAKS)

print (result)

# from langflow import load_flow_from_json
#
# flow = load_flow_from_json("langflow_open_ai_astra_db_tutorial_work.json")
# # Now you can use it like any chain
# flow("Please explain CLIP experiment short and simple.")