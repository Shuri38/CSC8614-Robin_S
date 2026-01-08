from transformers import GPT2Model

import plotly.express as px
from sklearn.decomposition import PCA

# Charger le modèle GPT-2 pré-entraîné
model = GPT2Model.from_pretrained("gpt2")

# Récupérer la matrice des embeddings positionnels (learned positional embeddings)
position_embeddings = model.wpe.weight  # wpe = "word positional embeddings"

print("Shape position embeddings:", position_embeddings.size())

# Afficher quelques informations de configuration
print("n_embd (dimension des embeddings):", model.config.n_embd)
print("n_positions (longueur de contexte maximale):", model.config.n_positions)


# Extraire les 50 premières positions et convertir en numpy
positions = position_embeddings[:50].detach().cpu().numpy()

# Réduction dimensionnelle à 2D via PCA
pca = PCA(n_components=2)
reduced = pca.fit_transform(positions)

# Création du scatter plot avec Plotly
fig = px.scatter(
    x=reduced[:, 0],
    y=reduced[:, 1],
    text=[str(i) for i in range(len(reduced))],
    color=list(range(len(reduced))),
    title="Encodages positionnels GPT-2 (PCA, positions 0-50)",
    labels={"x": "PCA 1", "y": "PCA 2"}
)

# Sauvegarde en HTML
fig.write_html("TP1/positions_50.html")
print("Graphique sauvegardé sous TP1/positions_50.html")

# Extraire les 200 premières positions
positions_200 = position_embeddings[:200].detach().cpu().numpy()

# Réduction dimensionnelle à 2D via PCA
reduced_200 = PCA(n_components=2).fit_transform(positions_200)

# Scatter plot Plotly pour les 200 premières positions
fig_200 = px.scatter(
    x=reduced_200[:, 0],
    y=reduced_200[:, 1],
    text=[str(i) for i in range(len(reduced_200))],
    color=list(range(len(reduced_200))),
    title="Encodages positionnels GPT-2 (PCA, positions 0-200)",
    labels={"x": "PCA 1", "y": "PCA 2"}
)

# Sauvegarde en HTML
fig_200.write_html("TP1/positions_200.html")
print("Graphique sauvegardé sous TP1/positions_200.html")


