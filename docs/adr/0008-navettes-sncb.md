# 0008 — Navettes de remplacement SNCB : ce que les données ouvertes donnent

- **Date :** 2026-11-25
- **Statut :** acceptée
- **Vérification de phase 0 :** 12, partie données SNCB et Infrabel (voir `docs/PRD-v2.md` §9)

## Question

Quand un train est remplacé par des bus, les données ouvertes disent-elles assez tôt quels bus roulent, à quelle heure, entre quelles gares et où ils s'arrêtent ? Les travaux d'Infrabel permettent-ils de le savoir plus tôt ?

## Ce qui a été testé

- GTFS SNCB anonyme (`feed_version` 2026-11-25), lu par `spikes/sncb-replacement/analyze_sncb_bus.py` (Python lancé avec `-I`).
- Jeu Infrabel `langetermijnplanning-tcr-spoornetwerk` (licence CC0, 9 536 travaux, mis à jour le 28/08/2026), interrogé sans clé par l'API Explore v2.1, filtré sur les lignes 36, 42 et 43 et sur les dates des bus trouvés.

## Résultats

Vérifié (rapport `data/raw/sncb/bus-report.json`) :

- **75 lignes `BUS`** (`route_type` 700), **1 530 courses**, toutes datées. Elles roulent du **22/11 au 28/12/2026** : publiées environ 5 semaines à l'avance.
- **14 lignes** touchent notre région. Par exemple :

| Ligne SNCB | Trajet | Dates | Courses |
|---|---|---|---|
| 666 | Liège-Guillemins → Trois-Ponts (ligne 42 : Angleur, Esneux, Poulseur, Rivage, Aywaille, Coo) | 22/11 | 18 |
| 671 | Liège-Guillemins → Bomal (ligne 43 : Tilff, Esneux, Hamoir…) | 22/11 | 17 |
| 667 | Liège-Guillemins → Rivage | 5 et 6/12 | 34 |
| 678 | Verviers → Spa | 22/11 au 28/12 | 43 |

- Le **numéro de course du bus est le numéro du train remplacé** : les 35 numéros des lignes 666, 667 et 671 sont aussi ceux des IC Liège–Luxembourg (par exemple 5306, départ Guillemins 05 h 06, arrivée Trois-Ponts 06 h 55).
- Les arrêts sont **les gares elles-mêmes** (identifiant et coordonnées de la gare ou d'un quai, parfois un quai « VARIA »), **pas l'arrêt réel du bus** devant la gare. Pas de tracé, pas de sens (`direction_id` vide).
- Infrabel : les lignes 42 et 43 ont 165 travaux planifiés (dont 126 fermetures totales), mais **le premier commence en avril 2027**. Aucun ne couvre les bus du 22/11 ni des 5 et 6/12. Sur toute la Belgique, une seule fermeture totale tombe entre le 22/11 et le 7/12/2026, et elle est en Flandre.

Supposé, non vérifié :

- Le plan Infrabel ne contient que les gros chantiers planifiés de longue date ; les travaux de week-end décidés à quelques semaines ne s'y trouvent pas.
- Les bus SNCB de notre région sont conduits par des chauffeurs du TEC ou de Keolis : à confirmer par Thierry.

## Décision

1. **Source des navettes : le GTFS SNCB**, relu chaque jour. Il donne les dates, les heures, les gares et le numéro du train remplacé, environ 5 semaines à l'avance.
2. **Infrabel n'est pas une source d'alerte** pour le pilote : son plan ne voit pas les travaux à court terme. Il peut servir plus tard à annoncer les grands chantiers de 2027-2028, sans plus.
3. **L'arrêt réel devant chaque gare** ne vient d'aucune donnée ouverte. Il sera saisi sur le terrain (photo et point sur la carte), validé par un chauffeur, puis partagé (PRD, M11).
4. Les coordonnées des gares ne sont **jamais présentées comme l'arrêt du bus**.
5. **Les données TEC restent la référence** : quand une gare est aussi un arrêt TEC, l'app prend l'arrêt et le quai du GTFS TEC, et le GTFS SNCB ne sert qu'à dire qu'une navette existe.
6. Écrire à la SNCB ou à Keolis (format des feuilles de route, arrêts réels) reste un envoi externe : **seulement avec l'accord de Thierry**.

## Conséquences

- Le module M11 (après le MVP) lit le GTFS SNCB, filtre `route_type` 700 sur la région et relie chaque course à son numéro de train.
- Le tracé entre deux gares sera calculé par Valhalla en mode bus (ADR 0007), avec le même garde-fou, et présenté comme « à vérifier ».
- Attribution SNCB à ajouter dans l'app selon les conditions du flux.
- Rien n'est automatisé en phase 0 : le script reste une sonde.
