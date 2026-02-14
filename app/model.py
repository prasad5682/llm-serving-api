from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from threading import Lock
import os
MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/tiny-gpt2")

# MODEL_NAME = "sshleifer/tiny-gpt2"

_tokenizer = None
_model = None
_lock = Lock()


def get_model():
    global _tokenizer, _model

    if _model is None:
        with _lock:
            if _model is None:
                _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
                _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    return _tokenizer, _model


def generate_text(prompt: str, max_new_tokens: int):
    tokenizer, model = get_model()

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)
