from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
phrase = "Artificial intelligence is metamorphosing the world!"

# Obtenir les IDs des tokens
token_ids = tokenizer.encode(phrase)

print("Token IDs:", token_ids)


from transformers import GPT2Tokenizer
phrase2 = "GPT models use BPE tokenization to process unusual words like antidisestablishmentarianism."

# Tokenisation
tokens2 = tokenizer.tokenize(phrase2)
print(tokens2)

# Extraire les tokens correspondant au mot long
long_word = "antidisestablishmentarianism"
long_tokens = tokenizer.tokenize(" " + long_word)  # espace important pour GPT-2

print("Sous-tokens du mot long :", long_tokens)
print("Nombre de sous-tokens :", len(long_tokens))

