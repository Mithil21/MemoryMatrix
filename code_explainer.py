from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class CodeExplainer:
    def __init__(self, model_path="models/code"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device_map="auto")

    def explain(self, code, max_tokens=150):
        try:
            prompt = f"Explain the following code in simple terms:\n\n{code[:800]}\n\nExplanation:"
            output = self.pipe(prompt, max_new_tokens=max_tokens, temperature=0.7, top_p=0.95)
            return output[0]["generated_text"].split("Explanation:")[-1].strip()
        except Exception as e:
            return f"⚠️ Error explaining code: {e}"
