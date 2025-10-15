from transformers import GPT2LMHeadModel, GPT2Tokenizer
from app.utils import cleaning_decode
import os
def generate_text(question: str):
    # --- Load model dan tokenizer ---
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    model_dir = os.path.join(base_dir, "models", "gpt2_mental_health_ft")
    if not os.path.exists(model_dir):
        raise FileNotFoundError("Model not found in directory")

    model = GPT2LMHeadModel.from_pretrained(model_dir)
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id
    model.eval()

    # --- Cleaning noise ---
    if hasattr(tokenizer, "bos_token"):
        tokenizer.bos_token = None

    # --- Tokenizer setup ---
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id
    model.eval()

    prompt = f"""The following is a conversation between a user and a kind, empathetic mental health assistant.
    The assistant always replies naturally, concisely, and with emotional understanding.

    User: {question}
    Assistant:"""

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.4,
        no_repeat_ngram_size=3,
        pad_token_id=tokenizer.eos_token_id,
    )

    # --- Decode dan cleaning ---
    text = cleaning_decode.clean_decode(outputs[0], tokenizer)

    if "Assistant:" in text:
        text = text.split("Assistant:")[-1].strip()
    elif "User:" in text:
        text = text.split("User:")[-1].strip()

    return text