## Expérience NER 25/03/2025

Dans le cadre du projet Paraboles et du traitement des fichiers ALTO XML issus de la BnF en un fichier TEI. 

Nécessaire de traiter les titres, qui sont sous la forme "Traduction de la Parabole de l’Enfant prodigue en patois de Marennes, Charente-Inférieure, envoyée, en 1818, par M. Guillotin FOUGERÉ, sous-préfet, (m. i.)" pour récupérer des informations de métadonnées: Langues, personnes, lieux, date (et peut être occupation?). 

La structuration des titres varient suffisamment pour ne pas permettre l'utilisation des regex pour récupérer ces informations mais le NER peut peut être fonctionner pour éviter une récupération manuelle complète.

## Premier essai avec le modèle de base de spacy

Emploi du modèle spacy fr_core_news_sm et test nlp peu concluant. Aucune personne n'est trouvée sur le corpus et les lieux reconnus sont assez mauvais.
```
Person: [], Location:['Liège']
Person: [], Location:['Wallon']
Person: [], Location:[]
Person: [], Location:['Wallon']
Person: [], Location:[]
Person: [], Location:['canton d’Arras']
Person: [], Location:['Ardennois']
Person: [], Location:['Patois', 'Onville']
Person: [], Location:['Lorrain']
Person: ['Parabole de l’Enfant Prodigue'], Location:[]
Person: [], Location:[]
Person: [], Location:['Sarladais']
Person: [], Location:['Limousin']
Person: ['Aurillac'], Location:[]
Person: [], Location:['Rodez']
```

## Fine Tunning du modèle
Décision de tester le fine tunning du modèle fr_core_news_sm avec des exemples issus de l'édition des paraboles à traiter.
- train: 10 titres pris dans une tentative de représenter la diversité des structures des titres présents dans l'édition. ( voir ner_train.txt)
- eval: 5 titres. ( voir ner_eval.txt). 

Utilisation du tutoriel: https://github.com/dreji18/NER-Training-Spacy-3.0/tree/main avec annotation des données avec l'outil https://arunmozhi.in/ner-annotator/

```
^C(venv-parabole) jjanes@ptb-020008625:~/Documents/github_rep/parabole/ner$ python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./eval.spacy
ℹ Saving to output directory: output
ℹ Using CPU

=========================== Initializing pipeline ===========================
✔ Initialized pipeline

============================= Training pipeline =============================
ℹ Pipeline: ['tok2vec', 'ner']
ℹ Initial learn rate: 0.001
E    #       LOSS TOK2VEC  LOSS NER  ENTS_F  ENTS_P  ENTS_R  SCORE 
---  ------  ------------  --------  ------  ------  ------  ------
  0       0          0.00     36.70    0.00    0.00    0.00    0.00
 66     200         16.25    933.98   47.06   50.00   44.44    0.47
143     400          0.00      0.00   58.82   62.50   55.56    0.59
243     600          0.00      0.00   58.82   62.50   55.56    0.59
343     800          0.00      0.00   58.82   62.50   55.56    0.59
512    1000          0.00      0.00   58.82   62.50   55.56    0.59
712    1200          0.00      0.00   58.82   62.50   55.56    0.59
912    1400          0.00      0.00   58.82   62.50   55.56    0.59
1112    1600          0.00      0.00   58.82   62.50   55.56    0.59
1312    1800          0.00      0.00   58.82   62.50   55.56    0.59
1512    2000          0.00      0.00   58.82   62.50   55.56    0.59
✔ Saved pipeline to output directory
output/model-last

```


## Evaluation du modèle

Comparaison de fr_core_news_sm sur l'eval et du nouveau modèle produit:
```spacy evaluate model eval.spacy```

| model | NER P | NER R | NER F | LOC P | LOC R| LOC F | PER P | PER R | PER F |
|----- |----|---|----|---|---|---|---|---|--|
| fr_core_news_sm | 23,53|44,44|30,77|50|66,67|57,14|0|0|0|
|fine tuned model | 62,50|55,56|58,82|66,67|66,67|66,67|50,00|33,33|40,00|

Une belle amélioration des reconnaissance des personnes et plus de précision pour la reconnaissance des lieux, juste avec 10 titres dans le corpus de train.
Proposition: production d'un train de 25-30 titres pour fine tunner un model plus précis - voir le résultat si amélioration et traitement des 170 paraboles avec ce model?

