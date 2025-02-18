import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith.evaluation import evaluate, LangChainStringEvaluator

'''
Prerequisite:
pip install -U langchain langsmith
export LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
export LANGCHAIN_API_KEY=<your-api-key>
export OPENAI_API_KEY=<your-api-key>
'''

os.environ.setdefault("LANGCHAIN_ENDPOINT","https://api.smith.langchain.com")
os.environ.setdefault("LANGCHAIN_API_KEY","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")
os.environ.setdefault("OPENAI_API_KEY","sk-proj-dp9jBb9HIkAU8MD9A49jT3BlbkFJSB7eMhysGcI6KPNDcZRm")

# Target task definition
prompt = ChatPromptTemplate.from_messages([
  ("system", "Please review the answer against FusionU-Net: U-Net with Enhanced Skip Connection for Pathology Image Segmentation research paper."),
  ("user", "Briefly describe the implementation details of FusionU-Net.")
])
chat_model = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | chat_model | output_parser

# The name or UUID of the LangSmith dataset to evaluate on.
# Alternatively, you can pass an iterator of examples
data = "team1_advanced_rag_langsmith_dataset"

# A string to prefix the experiment name with.
# If not provided, a random string will be generated.
experiment_prefix = "team1_advanced_rag_langsmith_dataset"

# List of evaluators to score the outputs of target task
evaluators = [
  LangChainStringEvaluator("cot_qa"),
  LangChainStringEvaluator("labeled_criteria", config={"criteria": "relevance"}),
  LangChainStringEvaluator("labeled_criteria", config={"criteria": "conciseness"}),
  LangChainStringEvaluator("labeled_criteria", config={"criteria": "coherence"}),
  LangChainStringEvaluator("labeled_criteria", config={"criteria": "detail"})
]

# Evaluate the target task
results = evaluate(
  chain.invoke,
  data=data,
  evaluators=evaluators,
  experiment_prefix=experiment_prefix,
)