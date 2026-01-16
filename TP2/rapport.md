
# TP2 


(i) Nom / Prénom : Robin SLESINSKI

(ii) Commande d’installation et d’activation :

```bash
# Création de l'environnement
python -m venv env_tp2

# Activation de l'environnement (Mac/Linux)
source env_tp2/bin/activate

# Installation des dépendances
pip install torch tiktoken numpy pandas matplotlib
```
(iii) Versions logicielles principales :

```bash
Python : 3.9+ (ou 3.10+)

PyTorch : 2.0+

Tiktoken : 0.5+

Pandas : 2.0+
```

Question 2 : Configuration du modèle (settings)L'objet settings (ou hparams) est un dictionnaire contenant les hyperparamètres structurels essentiels à la reconstruction de l'architecture GPT-2. Pour la version "124M", il définit notamment la taille du vocabulaire (50 257), la longueur maximale du contexte (1 024), la dimension d'embedding (768), ainsi que le nombre de têtes d'attention et de couches (12 chacune).

Question 3 : Poids du modèle (params)L'objet params est un dictionnaire imbriqué stockant les poids réels et entraînés du modèle. Les clés de premier niveau (comme wte pour les embeddings ou h pour les couches cachées) pointent vers des tenseurs PyTorch ou des tableaux NumPy. Par exemple, la matrice params['wte'] possède une forme de $[50257, 768]$, associant chaque token du vocabulaire à son vecteur de dimension correspondante.

Question 4 : Mappage de la configurationLe mappage est indispensable car la nomenclature d'OpenAI dans settings (ex: n_vocab) diffère de celle attendue par la classe GPTModel dans gpt_utils.py (ex: vocab_size). Cette étape permet de traduire les clés, d'ajuster les paramètres de régularisation comme le drop_rate et d'activer le qkv_bias, garantissant ainsi que le modèle s'initialise avec une structure compatible avec les poids chargés.

Question 5.1 : Mélange et ReproductibilitéL'utilisation de df.sample(frac=1, random_state=123) assure un mélange intégral du dataset avant la division. Cela brise tout tri initial par classe (évitant un entraînement sur une seule catégorie) et garantit la reproductibilité des résultats. La graine aléatoire fixe permet d'obtenir un mélange identique à chaque exécution, facilitant ainsi le débogage et la comparaison des performances.

Question 5.2 : Analyse du déséquilibre des classesLe jeu de données est fortement déséquilibré, avec environ 86,6% de messages sains ("ham") contre seulement 13,4% de spams. Ce déséquilibre fait peser un risque de biais de prédiction : le modèle pourrait obtenir une forte précision globale en prédisant systématiquement "ham", tout en échouant à détecter les spams (faible rappel). Dans ce contexte, l'accuracy devient une métrique trompeuse, rendant l'usage du score F1 ou de la matrice de confusion indispensable.

Question 7 : Dimensionnement des BatchesAvec un dataset d'entraînement de 4 457 échantillons et un batch_size de 16, nous obtenons 278 batches par époque. Ce nombre résulte de la division entière du dataset par la taille des lots. L'activation de l'option drop_last=True écarte les 9 échantillons restants pour maintenir des lots de taille constante, ce qui stabilise le calcul des gradients et optimise les performances de l'entraînement.

Question 8.3 : Stratégie de "Freezing" (Gel des couches)Le gel des couches internes via requires_grad = False permet de préserver les connaissances linguistiques pré-entraînées de GPT-2 tout en évitant l'oubli catastrophique. Cette technique de Transfer Learning stabilise l'apprentissage en empêchant les erreurs initiales de la nouvelle tête de classification de dégrader les couches profondes. Enfin, cela réduit drastiquement le coût computationnel, un atout majeur pour l'entraînement sur des machines aux ressources limitées.

Question 1O : L'évolution des métriques démontre que le modèle traverse une phase d'apprentissage significative. À l'Époque 1, le modèle est inefficace malgré une précision globale élevée (86 %), car son score sur les spams est de 0 % : il se contente de prédire systématiquement la classe majoritaire. À l'Époque 2, grâce aux poids compensatoires (class_weights), on observe un basculement : le modèle apprend à identifier les spams avec succès (92 %), bien que cela dégrade temporairement la précision globale.

À l'Époque 3, le modèle atteint un point d'équilibre optimal. La perte se stabilise et la précision sur les spams se maintient à un niveau élevé (89 %) tout en redressant la précision globale à 82 %. Le fait que les performances sur le jeu de test soient extrêmement proches de celles du jeu d'entraînement prouve que le modèle généralise bien et ne fait pas de sur-apprentissage (overfitting). Le fine-tuning est donc une réussite : le modèle est passé d'une stratégie de "prédiction par défaut" à une réelle capacité de distinction sémantique entre les deux classes.
