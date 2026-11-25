# Phase 0 — plan et suivi

Démarrée le 25 novembre 2026. But : lever les inconnues techniques avant d'écrire l'app. Chaque vérification (numérotée comme dans `docs/PRD-v2.md` §9) se termine par un ADR dans `docs/adr/` et une PR.

## Chantiers

| Chantier | Vérifications | Qui | État |
|---|---|---|---|
| **A. Données TEC** | 6 paquet de ligne (64, 65 : calendrier, tracés, quais), 9 lignes au même numéro, 10 temps réel aux arrêts | Claude, seul | fait (ADR 0003, 0004, 0005 ; inventaire à valider par Thierry) |
| **B. Carte et itinéraires** | 7 tuiles hors ligne (PMTiles du couloir), 12 routage Valhalla en mode bus | Claude, seul | fait (ADR 0006, 0007 ; stockage OPFS et lecture hors ligne sur l'iPhone passent au chantier E) |
| **C. Socle** | 1 Supabase local, 3 conditions Belgian Mobility (licence, quotas) | Claude, seul (Docker démarré) | fait (ADR 0001, 0002) |
| **D. Navettes SNCB** | 12 GTFS SNCB (lignes `BUS`), travaux Infrabel | Claude, seul | fait (ADR 0008 ; pas de contact SNCB / Keolis) |
| **E. Banc d'essai iPhone** | 4 PWA sur iPhone 14, 11 notifications et Raccourcis | Claude prépare une page de test ; Thierry l'ouvre sur son iPhone (environ 15 min) | après A–D |
| **F. OCR des feuilles de service** | 8 | Claude, avec les exemples du lundi 30/11 | 30/11/2026 |
| **G. E-mails** | 2 | en attente du nom de l'app | bloqué |

## Ce dont Claude a besoin de Thierry (le moins possible)

1. **Compte développeur Belgian Mobility** et sa clé : à créer par Thierry (mot de passe personnel). La clé va dans le coffre DevContext `perso` sous le nom `devctx/perso/bmc-key`. Sans clé, on avance avec l'accès anonyme (exploration).
2. **Jeton Supabase** du compte gmail (org `copibus`) dans le coffre DevContext, au moment de brancher le cloud (pas avant le pilote).
3. **Tests sur l'iPhone 14** : ouvrir une page de test et toucher quelques boutons (chantier E).
4. **Exemples de feuilles de service** le 30/11 (chantier F).
5. **Pas de contact** avec la SNCB ni Keolis (décision du 25/11/2026). Tout autre envoi externe demande l'accord de Thierry.

## Règles de travail

- Un chantier = une branche `feature/phase0-<sujet>` = une PR, avec la revue de code et, si réseau, secrets ou données personnelles, la revue sécurité Opus.
- Les sondes vont dans `spikes/<sujet>/`, les données téléchargées dans `data/raw/` (ignoré par git).
- Résultat honnête : un échec documenté vaut mieux qu'un faux succès.
