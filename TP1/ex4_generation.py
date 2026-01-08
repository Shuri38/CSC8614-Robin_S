import torch
import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Seed pour reproductibilité
SEED = 42
torch.manual_seed(SEED)

# Charger modèle et tokenizer
device = torch.device("cpu")
model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Phrase de départ
prompt = "The future of artificial intelligence is"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

outputs = model.generate(
    **inputs,
    max_length=50,       # longueur totale de la séquence générée
    do_sample=False      # décodage glouton / greedy
)

text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(text)

def generate_once(seed):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

for s in [1, 2, 3, 4, 5]:
    print("SEED", s)
    print(generate_once(s))
    print("-" * 40)

def generate_with_penalty(seed, repetition_penalty=None):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        repetition_penalty=repetition_penalty
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

# Seed identique pour comparaison
seed = 1
text_no_penalty = generate_with_penalty(seed, repetition_penalty=None)
text_with_penalty = generate_with_penalty(seed, repetition_penalty=2.0)

print("=== Sans pénalité ===")
print(text_no_penalty)
print("-" * 40)
print("=== Avec répétition_penalty=2.0 ===")
print(text_with_penalty)
print("-" * 40)

def generate_with_temp(seed, temperature=None):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=temperature,
        top_k=50,
        top_p=0.95
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

# Seed identique pour comparaison
seed = 1
text_low_temp = generate_with_temp(seed,temperature=0.1)
text_high_temp= generate_with_temp(seed,temperature=2.0)

print("=== Température basse ===")
print(text_no_penalty)
print("-" * 40)
print("=== Température haute ===")
print(text_with_penalty)
print("-" * 40)


out_beam = model.generate(
    **inputs,
    max_length=50,
    num_beams=5,
    early_stopping=True
)
txt_beam = tokenizer.decode(out_beam[0], skip_special_tokens=True)
print(txt_beam)

for num_beams in [5, 10, 20]:
    start = time.time()
    out = model.generate(
        **inputs,
        max_length=50,
        num_beams=num_beams,
        early_stopping=True
    )
    elapsed = time.time() - start
    txt = tokenizer.decode(out[0], skip_special_tokens=True)
    print(f"num_beams={num_beams}, temps={elapsed:.2f}s")
    print(txt)
    print("-" * 40)
