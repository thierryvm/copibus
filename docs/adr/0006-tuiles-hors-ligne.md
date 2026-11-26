# 0006 — Tuiles de carte hors ligne (PMTiles du couloir)

- **Date :** 2026-11-25
- **Statut :** acceptée
- **Vérification de phase 0 :** 7 (voir `docs/PRD-v2.md` §9)

## Question

Combien pèse la carte vectorielle du couloir des lignes 64 et 65 (Liège, Aywaille, Remouchamps, Banneux) si on l'embarque dans le téléphone, et jusqu'à quel niveau de zoom faut-il aller ?

## Ce qui a été testé

- Archive mondiale Protomaps (format PMTiles v3, données OpenStreetMap) du 24/11/2026 : `https://build.protomaps.com/20261124.pmtiles`.
- Script `spikes/map-tiles/measure_pmtiles.py` (Python lancé avec `-I`, bibliothèque standard seulement). Il lit l'en-tête et les répertoires de l'archive par requêtes HTTP partielles, cherche chaque tuile du rectangle et additionne leur taille, **sans télécharger l'archive**. Il ne compte qu'une fois les tuiles identiques, comme le ferait un extrait.
- Rectangle du couloir : longitude 5,50 à 5,85, latitude 50,44 à 50,66.

## Résultats

Vérifié (rapport `data/raw/tiles/corridor-report.json`) :

| Zoom maximal | Taille cumulée |
|---|---|
| 9 | 2,2 Mo |
| 10 | 2,8 Mo |
| 11 | 3,9 Mo |
| 12 | 5,7 Mo |
| 13 | 8,6 Mo |
| **14** (289 tuiles à ce niveau) | **13,9 Mo** |
| 15 (1 089 tuiles, maximum de l'archive) | 27,3 Mo |

- Toutes les tuiles du rectangle existent dans l'archive.
- Passer du zoom 14 au zoom 15 double la taille.

Supposé, non vérifié :

- Que le zoom 14, agrandi par le moteur de carte (les tuiles vectorielles se redessinent net au-delà de leur niveau), suffit pour la conduite. C'est l'usage courant de Protomaps, mais il faut le voir à l'écran.
- Que l'iPhone garde 14 Mo dans l'OPFS sans les effacer. À tester au chantier E (PWA sur iPhone 14).
- La taille exacte d'un extrait fait par l'outil officiel `pmtiles extract` : ce calcul n'en compte pas les répertoires (quelques Ko).

## Décision

- Carte hors ligne du couloir : **PMTiles jusqu'au zoom 14, environ 14 Mo**, agrandi au-delà par le moteur de carte.
- L'extrait est produit une fois par nos soins (outil `pmtiles extract`) et régénéré quelques fois par an ; il est servi comme un fichier statique.
- Attribution obligatoire dans l'app : « © OpenStreetMap » (licence ODbL) et Protomaps.

## Conséquences

- Portée de la décision : Stockage OPFS et lecture hors ligne sur l'iPhone restent à tester au chantier E.
- 14 Mo par couloir : on peut en embarquer plusieurs, mais pas toute la Wallonie. Un chauffeur télécharge le couloir de son dépôt.
- Hébergement du fichier : voir ADR 0007 (rien n'est créé ni activé sans l'accord de Thierry).
- À revérifier au chantier E : stockage OPFS, lecture sans réseau, rendu au zoom 16 et plus.
