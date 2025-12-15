import re
import os
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from rag_pipeline import HFLLM

def create_bloom_evaluator():
    """
    Builds a RunnableSequence that evaluates an answer's cognitive depth
    based on Bloom's Taxonomy using the same HFLLM wrapper.
    """
    template = """
    You are an evaluator analyzing a student's answer using Bloom’s Taxonomy.
    Given the learning context and answer, classify it as one of these levels:
    - Remember
    - Understand
    - Apply
    - Analyze
    - Evaluate
    - Create

    Context:
    {context}

    Student Answer:
    {answer}

    Respond with ONLY the Bloom's level name.
    """

    prompt = PromptTemplate(
        input_variables=["context", "answer"],
        template=template
    )

    # Use the same LLM wrapper but conversational model (Zephyr or Phi)
    llm = HFLLM(model_id="HuggingFaceH4/zephyr-7b-beta", token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

    # Create runnable sequence (LangChain 0.2.x style)
    evaluator_chain = prompt | llm
    return evaluator_chain


def format_evaluation_output(question: str, answer: str, result) -> str:
    """Format the evaluation into a clean, readable tutor-style report for Streamlit or console."""

    # --- Ensure result is a string
    if isinstance(result, dict):
        result = result.get("text", str(result))
    elif not isinstance(result, str):
        result = str(result)

    # --- Clean out system tags and repeated instructions
    cleaned = re.sub(r"\[/?(STUDENT|ASST|ASS|STU)\]", "", result)
    cleaned = re.sub(r"(?i)you are an evaluator.*?taxonomy[\.\n]", "", cleaned)
    cleaned = re.sub(r"(?i)based on the given context.*?taxonomy[\.\n]", "", cleaned)
    cleaned = re.sub(r"(?i)given the learning context.*?:", "", cleaned)
    cleaned = re.sub(r"(?i)(context:|student answer:|question:)", "", cleaned)
    cleaned = re.sub(r"(?i)remember\s*/?\s*", "", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()

    # --- Detect Bloom’s level
    bloom_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    detected_level = next((lvl for lvl in bloom_levels if lvl.lower() in cleaned.lower()), "Unknown")

    # --- Final formatted report
    report = f"""
🧩 **Question:** {question}

💬 **Answer:**
{answer}

🎓 **AI Evaluation Report**
----------------------------------------
**Detected Bloom Level:** {detected_level}

🧠 **Feedback Summary:**
{cleaned}

----------------------------------------
_(Generated automatically by the Educational LLM Evaluator)_
"""
    return report