import os
from typing import Optional, List
from huggingface_hub import InferenceClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.runnables import Runnable

# ---- Runnable LLM wrapper ----
class HFLLM(Runnable):
    """Runnable-compatible wrapper for Hugging Face models (supports both chat & text endpoints)."""

    def __init__(self, model_id: str, token: Optional[str] = None,
                 max_new_tokens: int = 400, temperature: float = 0.3):
        self.model_id = model_id
        self.token = token
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.client = InferenceClient(model=model_id, token=token)

    def invoke(self, input, config=None, **kwargs) -> str:
        """Main callable interface for LangChain Runnable API."""
        try:
            # Convert input into plain text
            if hasattr(input, "to_string"):
                input = input.to_string()
            elif isinstance(input, dict):
                input = input.get("context") or input.get("answer") or input.get("question") or str(input)
            else:
                input = str(input)

            # Try chat first, then fallback to text generation
            try:
                messages = [{"role": "user", "content": input}]
                response = self.client.chat_completion(
                    model=self.model_id,
                    messages=messages,
                    temperature=self.temperature,
                )
                if isinstance(response, dict):
                    return response.get("generated_text") or \
                           response.get("choices", [{}])[0].get("message", {}).get("content", "")
                elif hasattr(response, "choices"):
                    return response.choices[0].message["content"]
            except Exception:
                # Fallback to text generation
                response = self.client.text_generation(
                    input,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                )
                if isinstance(response, dict):
                    return response.get("generated_text", str(response))
                return str(response)

        except Exception as e:
            return f"[Error during generation: {e}]"


# ---- Build FAISS Vector DB ----
def build_vector_db(documents, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks from {len(documents)} docs")

    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    db = FAISS.from_documents(chunks, embeddings)
    print("✅ FAISS vector DB created")
    return db


# ---- Create Retrieval-Augmented QA Chain ----
def create_qa_chain(vector_db):
    retriever = vector_db.as_retriever(search_kwargs={"k": 6})

    llm = HFLLM(
        model_id="meta-llama/Llama-3.2-1B-Instruct",  # ✅ works with chat_completion
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    )

    template = """
    You are an educational assistant. Use the context below to answer the question.
    If the context doesn’t contain the answer, say you don’t know.
    Context: {context}
    Question: {question}
    """

    prompt = PromptTemplate(input_variables=["context", "question"], template=template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        input_key="question",
        output_key="result",
    )

    print("✅ QA chain ready")
    return qa_chain