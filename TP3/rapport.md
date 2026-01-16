
# TP3

Pour le SETUP, on a pris la valeur 42 de seed, qui permet la reproductibilité.

# Exercice 1

Question 1 :

On observe une modification structurelle majeure : alors que le modèle original utilise des couches nn.Linear standards, le modèle modifié encapsule ces couches dans un module LinearWithLoRA. Ce dernier contient à la fois la couche linéaire initiale (gelée) et une nouvelle structure nommée lora (le module LoRALayer défini précédemment). Cette transformation est visible partout dans le bloc de transformateur, notamment au niveau des mécanismes d'attention (W_query, W_key, etc.) et des couches du FeedForward.

Question 2 :

Le modèle compte environ 164 millions de paramètres au total, mais suite à l'injection de LoRA, seuls 1 327 104 paramètres sont réellement entraînés. Cela représente une fraction de seulement 0,81 % de paramètres activés. Ce chiffre démontre l'efficacité de la méthode : vous pouvez adapter un modèle complexe à une nouvelle tâche (comme la détection de spams) en ne mettant à jour qu'une infime partie de ses poids, ce qui réduit considérablement les besoins en mémoire et en calcul.

Question 3 : La comparaison montre que le second modèle est plus petit (passant de 164,4M à 125,8M de paramètres totaux), ce qui correspond généralement au passage d'une version "Medium" à "Small" du GPT. Bien que le nombre absolu de paramètres LoRA reste quasi identique (~1,3M), leur proportion relative augmente logiquement, passant de 0,81 % à 1,06 %. En résumé, l'impact structurel de LoRA est mathématiquement plus "visible" sur un modèle léger, car les adaptateurs représentent une part plus importante d'un réseau globalement moins dense.

Question 4 :

La perte (loss) affiche une chute brutale dès les 10 premiers batchs (passant de 6.55 à 0.14), suivie de quelques pics isolés qui témoignent de l'adaptation du modèle à des exemples plus complexes. La tendance globale est une stabilisation rapide vers des valeurs très faibles. L'exactitude finale de 90,69 % dès la première époque est excellente et tout à fait raisonnable pour une tâche de classification binaire (Spam vs Ham). Compte tenu du fait que le modèle GPT de base possède déjà une compréhension fine du langage, LoRA permet ici de transférer efficacement cette capacité vers la tâche spécifique de détection avec une grande précision et en un temps record.

Question 5: 

L'exactitude sur l'ensemble de test (96,66 %) est excellente et montre que le modèle a très bien généralisé. En la comparant à l'exactitude de l'ensemble d'entraînement (90,69 %), on observe un fait intéressant : la performance est meilleure sur les données de test.

Cela s'explique généralement par deux facteurs : d'une part, la "Loss" a continué de chuter tout au long de l'époque (atteignant des valeurs très basses vers la fin), signifiant que le modèle était bien plus performant au dernier batch qu'au premier. D'autre part, l'exactitude de l'entraînement est une moyenne sur toute la durée de l'époque alors que le modèle est encore en train d'apprendre, tandis que le test reflète l'état final, "stabilisé", de l'apprentissage. Il n'y a donc aucun signe de surapprentissage (overfitting) ; au contraire, l'adaptation LoRA s'avère particulièrement robuste.

Textes testés : 

# TODO: add the text you want to test.
classify_text("There is a big cash prize for you, call immediately.", model, tokenizer, device)
classify_text("Hey, are we still meeting for lunch tomorrow?", model, tokenizer, device)
classify_text("Hytale beta keys are finally out! Click here to claim yours before they are all gone.", model, tokenizer, device)

Text: 'There is a big cash prize for you, call immediately.'
Prediction: HAM (Normal) (Confidence: 0.97)
------------------------------
Text: 'Hey, are we still meeting for lunch tomorrow?'
Prediction: HAM (Normal) (Confidence: 1.00)
------------------------------
Text: 'Hytale beta keys are finally out! Click here to claim yours before they are all gone.'
Prediction: HAM (Normal) (Confidence: 0.92)
------------------------------