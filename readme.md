> Code d'origine: (https://github.com/Armand-G/AGD_Scrap

Boomjour !

Cet outil permet de scrap (en français récupérer), les liens de personnages contenus dans le wiki AG&D.
Chaque liens est ensuite visité pour définir si il y a un lien entre personnages.
Par exemple: comme William est marié avec JC, il est fait mention de William sur la page de JC et inversement.

Le script génère 2 csv(un pour les pages et un pour les liens).

Les 2 csv peuvent ensuite etre visualisés:
 - avec Gephi (open source) Gephi https://gephi.org/users/download/
 - avec D3 [exemple](https://observablehq.com/d/23181d191ff327d5)

Vous pouvez vous aussi vous amuser avec ce logiciel, il y a des tutos en ligne et c'est très bien fait !

Pour faire fonctionner le script : 

pip install requirements.txt

python scrap.py

Et voilà !

Ce travail ne serait pas possible sans tous ceux qui contribuent au wiki, merci à eux !

Des questions ? 
 - tchouchki_ sur discord (auteur d'origine)
 - kailhou sur discord

A bientot
