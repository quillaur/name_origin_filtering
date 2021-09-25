# name_origin_filtering
Cette application utilise selenium pour aller rechercher le nom de famille de votre choix (dans un département donné) sur https://www.pagesjaunes.fr/pagesblanches et https://www.118712.fr/.
Un lien vers https://forebears.io/ est également disponible pour obtenir plus de renseignements sur le nom de famille en question.

L'application est disponible à cette adresse: https://share.streamlit.io/quillaur/name_origin_filtering/main/main.py

Un match entre le nom de famille donnée en input et les noms dans les annuaires est fait de la façon suivante:
- input = "Quillet" 
- matches = "Quillet Aurélien" / "Aurélien Quillet" / "Albert, Aurélien Quillet" / "Albert Quillet Aurélien"