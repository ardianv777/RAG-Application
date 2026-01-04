from langgraph.graph import StateGraph, END


class RagSystem:
    """Mengelola workflow pengambilan dan pembuatan jawaban"""
    
    def __init__(self, document_store):
        self.document_store = document_store
        self.chain = self._build_workflow()
    
    def _build_workflow(self):
        """Function untuk membangun LangGraph"""
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self._retrieve_step)
        workflow.add_node("answer", self._answer_step)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()
    
    def _retrieve_step(self, state: dict) -> dict:
        """Langkah 1: Mengambil dokumen yang relevan"""
        query = state["question"]
        results = self.document_store.search_documents(query)
        state["context"] = results
        return state
    
    def _answer_step(self, state: dict) -> dict:
        """Langkah 2: Menghasilkan jawaban dari konteks yang diambil"""
        context = state["context"]
        
        if context:
            # Take snippet from the first document
            answer = f"I found this: '{context[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        
        state["answer"] = answer
        return state
    
    def ask(self, question: str) -> dict:
        """Function untuk menjalankan workflow untuk menjawab pertanyaan"""
        result = self.chain.invoke({"question": question})
        return result