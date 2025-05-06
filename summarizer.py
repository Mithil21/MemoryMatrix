from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Summarizer:
    def __init__(self, model_name="models\summarize"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def summarize(self, text, max_new_tokens=100):
        try:
            print("Summarizing text...")
            prompt = f"Summarize the following in 70 words:\n{text.strip()}"
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
            output = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                repetition_penalty=1.1
            )
            return self.tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            return f"An error occurred during summarization: {e}"
