from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
# Load model & tokenizer
model_name = "./models/gpt2_mental_health_ft"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# === Texts to evaluate ===
texts = [
    "What is a panic attack?",
    "How to manage stress?"
]


# === Perplexity calculation ===
def calculate_ppl(text, stride=512):
    encodings = tokenizer(text, return_tensors="pt")
    encodings = {k: v.to(device) for k, v in encodings.items()}

    seq_len = encodings['input_ids'].size(1)
    nlls = []
    prev_end_loc = 0

    for begin_loc in range(0, seq_len, stride):
        end_loc = min(begin_loc + stride, seq_len)
        trg_len = end_loc - prev_end_loc

        input_ids = encodings['input_ids'][:, begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs.loss * trg_len
        nlls.append(neg_log_likelihood)
        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    ppl = torch.exp(torch.stack(nlls).sum() / seq_len)
    return ppl.item()


# === Evaluate texts ===
for text in texts:
    ppl = calculate_ppl(text)
    print(f"Text: {text}\nPerplexity: {ppl:.2f}\n")