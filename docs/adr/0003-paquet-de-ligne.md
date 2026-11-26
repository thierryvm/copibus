# 0003 — Paquet de ligne : calendrier, tracés, quais (lignes 64 et 65)

- **Date :** 2026-11-25
- **Statut :** acceptée
- **Vérification de phase 0 :** 6 (voir `docs/PRD-v2.md` §9)

## Question

Peut-on tirer du GTFS statique TEC un « paquet de ligne » autonome (arrêts, parcours, horaires, calendrier réel, tracés, quais) assez petit pour le téléphone et assez fiable pour guider un chauffeur ?

## Ce qui a été testé

- GTFS statique TEC téléchargé le 25/11/2026 via Belgian Mobility, rangé dans `data/raw/` (ignoré par git).
- Script `spikes/tec-line-package/build_package.py` (Python lancé avec `-I`) : pour un `route_id`, il regroupe les courses en parcours (suite d'arrêts), factorise les profils horaires, garde les services (jours, dates ajoutées ou retirées), simplifie les tracés et mesure l'écart arrêt / tracé.
- Lignes pilotes : `gr:tec:L0064-24183` et `gr:tec:L0065-24185`.

## Résultats

Vérifié (rapport `data/raw/tec/packages/report.json`) :

| | L0064 | L0065 |
|---|---|---|
| Courses | 329 | 942 |
| Parcours | 12 | 44 |
| Profils horaires | 49 | 148 |
| Arrêts | 115 | 149 |
| Services (calendriers) | 23 | 23 |
| Taille brute (JSON) | 83 Ko | 236 Ko |
| Taille gzip | 13,1 Ko | 26,6 Ko |
| Taille xz | 10 Ko | 19,3 Ko |

- Tracés simplifiés de 500 à 1 650 points vers 130 à 390 points par parcours.
- Écart maximal entre un arrêt et le tracé : **17,7 m**, sans arrêt répété. C'est la vraie preuve de l'alignement : le contrôle « avance dans le bon sens » du script ne peut pas échouer par construction.
- Les **quais** sont dans la colonne `platform_code` de `stops.txt` (254 arrêts sur 46 571), et le nom de l'arrêt les répète (exemple : `platform_code` « D », nom « LIEGE Gare des Guillemins - Quai D » à l'aller ; « C » au retour). Confirmé par Thierry sur le terrain pour les lignes 64 et 65.
- Le calendrier est fourni par période (« Mercredi », « Sem-N-3 »…) avec dates de début et de fin.
- Plusieurs parcours de la L0065 sont identiques (mêmes arrêts, même longueur) : ils peuvent être fusionnés.

Supposé, non vérifié :

- Que ce calendrier suffit pour savoir quelles courses roulent un jour donné : le générateur copie les services mais ne résout encore aucune date. À tester sur un jour précis.
- Que `platform_code` couvre tous les arrêts à quais. Il n'est rempli que pour 254 arrêts : un quai réel peut manquer ailleurs.
- Que le tracé TEC suit la voirie réelle à chaque carrefour (pas encore comparé à OpenStreetMap).

## Décision

- Le paquet de ligne est un fichier par `route_id`, compressé (gzip), de l'ordre de **13 à 27 Ko** par ligne. On peut en embarquer des dizaines sans souci.
- Format : arrêts, parcours, profils horaires, services et courses en table compacte (colonnes + lignes), tracés simplifiés.
- Ajouter la **fusion des parcours identiques** au générateur.
- Le quai est lu dans `platform_code` quand il est rempli. Sinon, il est lu dans le nom de l'arrêt quand celui-ci finit par « - Quai X » (X = 1 à 3 lettres ou chiffres) : vérifié le 26/11/2026, 87 arrêts TEC sont dans ce cas sur 325 noms de ce type (exemple : « MARLOIE Gare - Quai 1 »). Un nom de rue comme « HUY Quai d'Arona » ne correspond pas au motif. Sans l'un ni l'autre, l'app n'affiche pas de quai (on n'invente rien).

## Conséquences

- Portée de la décision : Calage OSM, consignes de carrefour et rejeu des traces restent à faire.
- PRD §9 point 6 : paquet et calendrier validés. Restent à faire, plus tard (chantier B ou phase 1) : calage sur OSM, consignes aux carrefours, rejeu de traces GPS réelles.
- Les identifiants de service changent à chaque nouvelle publication GTFS : le paquet doit porter la date de sa source et être régénéré à chaque publication.
- À revérifier à la prochaine publication TEC : tailles, écart arrêt / tracé, présence des quais.
