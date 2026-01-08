import torch
import math
from transformers import GPT2LMHeadModel, GPT2Tokenizer

device = torch.device("cpu")

model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

phrase = "L'intelligence artificielle est fascinante."
inputs = tokenizer(phrase, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits  # (1, seq_len, vocab)

# TODO: convertir en probabilités (softmax)
probs = torch.softmax(logits, dim=-1)

# On affiche P(token_t | tokens_) pour t>=1
input_ids = inputs["input_ids"][0]
for t in range(1, len(input_ids)):
    tok_id = input_ids[t].item()
    p = probs[0, t-1, tok_id].item()
    tok_txt = tokenizer.decode([tok_id])
    print(f"Token {t}: {repr(tok_txt)} -> prob={p:.3e}")

#Partie 4.b

log_probs = torch.log_softmax(logits, dim=-1)
input_ids = inputs["input_ids"][0]

# calcul de la log-proba totale
total_logp = 0.0
n = 0

for t in range(1, len(input_ids)):
    tok_id = input_ids[t].item()
    lp = log_probs[0, t-1, tok_id].item()
    total_logp += lp  # somme des log-probas
    n += 1           # nombre de tokens prédits

# log-proba négative moyenne
avg_neg_logp = - total_logp / n

# perplexité
ppl = math.exp(avg_neg_logp)

print("total_logp:", total_logp)
print("avg_neg_logp:", avg_neg_logp)
print("perplexity:", ppl)

prefix = "Artificial intelligence is"
inp = tokenizer(prefix, return_tensors="pt").to(device)

with torch.no_grad():
    out = model(**inp)
    logits2 = out.logits  # shape (1, seq_len, vocab_size)

# récupérer les logits du dernier token
last_logits = logits2[0, -1, :]  # dernier pas de temps
last_probs = torch.softmax(last_logits, dim=-1)

# 10 tokens les plus probables
topk = 10
vals, idx = torch.topk(last_probs, k=topk)

for p, tid in zip(vals.tolist(), idx.tolist()):
    print(repr(tokenizer.decode([tid])), f"{p:.3e}")