import re
def clean_decode(output_ids, tokenizer):
    text = tokenizer.decode(output_ids, skip_special_tokens=True)
    text = text.split("Assistant:")[-1].strip()

    replacements = {
        "Â": "", "Ã": "", "Æ": "", "Ċ": "", "Ġ": "",
        "ΓÇÖ": "'", "ΓÇô": "-", "ΓÇó": "•", "ΓÇ£": '"', "ΓÇ¥": '"',
        "┬á": " ", "|": "", "Â\xa0": " ", "à": ""
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s,.\'\"!?-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    sentences = re.split(r'(?<=[.!?])\s+', text)
    cleaned = []
    for s in sentences:
        if any(word in s.lower() for word in ["sorry", "guilt", "it was really me"]):
            continue
        cleaned.append(s)
        if len(cleaned) >= 2:
            break
    text = " ".join(cleaned).strip()

    return text[0].upper() + text[1:] if text else text