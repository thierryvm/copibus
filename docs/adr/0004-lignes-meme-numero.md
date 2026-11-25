# 0004 — Lignes qui portent le même numéro

- **Date :** 2026-11-25
- **Statut :** proposée (l'inventaire de la zone pilote attend la validation de Thierry)
- **Vérification de phase 0 :** 9 (voir `docs/PRD-v2.md` §9)

## Question

Combien de lignes TEC partagent un numéro, lesquelles posent problème dans la zone pilote, et comment l'app doit-elle désigner une ligne sans ambiguïté ?

## Ce qui a été testé

- GTFS statique TEC du 25/11/2026 (`data/raw/`, ignoré par git).
- Scripts `spikes/tec-same-number/inventory.py` (inventaire de tous les numéros) et `overlap.py` (lignes qui passent dans la zone pilote : latitude 50,44 à 50,66, longitude 5,5 à 5,85).

## Résultats

Vérifié :

- **852** lignes (`route_id`) pour **538** numéros différents.
- **137** numéros sont partagés, ce qui touche **451** lignes. Un même numéro peut couvrir jusqu'à **7** lignes.
- Certaines lignes existent en **deux versions** de `route_id` dans la même publication (L0145, L0703, L0708) : le suffixe du `route_id` (par exemple `-24183`) change d'une version à l'autre.
- Dans la zone pilote, **487** lignes passent. La seule vraie ambiguïté de numéro y est le **« 10 »** : `gr:tec:L0010-24146` (Sclessin – Flémalle, 22 arrêts) et `gr:tec:X9100-23956` (Manhay – Aywaille – Remouchamps, 41 arrêts).

Supposé :

- Que le suffixe du `route_id` change à chaque nouvelle version de ligne. Vu sur trois lignes, pas suivi sur plusieurs publications.

## Décision

- L'app identifie toujours une ligne par son `route_id`, jamais par son seul numéro (règle déjà inscrite dans le PRD).
- Quand un numéro est partagé, l'app affiche aussi les terminus ou la zone (« 10 Sclessin – Flémalle »).
- Comme le suffixe peut changer, on mémorise la ligne par son **code stable** (par exemple `L0065`) et on vérifie à chaque nouvelle publication que la version (`-24185`) existe encore. Si elle a changé, l'app le signale au lieu de basculer en silence.

## Conséquences

- PRD §9 point 9 : inventaire fait ; il reste la validation de Thierry sur le terrain, en particulier le « 10 » et les lignes en double version.
- Le générateur de paquets (ADR 0003) doit enregistrer le code stable et la version séparément.
- À revérifier à la prochaine publication TEC : est-ce que les suffixes ont bougé ?
