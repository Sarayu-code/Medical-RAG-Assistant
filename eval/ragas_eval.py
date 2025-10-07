import json, os
from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy
from ragas import evaluate
from app.rag import retriever_singleton, synthesize_answer
from app.guardrails import instruction_prompt
from app.rag import format_context

def load_eval(path="eval/eval_questions.jsonl"):
    rows = []
    with open(path, "r") as f:
        for line in f:
            q = json.loads(line)["query"]
            docs = retriever_singleton.retrieve(q, k=6)
            context = [d.page_content for d in docs]
            answer = synthesize_answer(q, docs, instruction_prompt())
            rows.append({"question": q, "contexts": context, "answer": answer})
    return Dataset.from_list(rows)

if __name__ == "__main__":
    ds = load_eval()
    result = evaluate(ds, metrics=[faithfulness, answer_relevancy])
    print(result)
