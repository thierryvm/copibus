# 0005 — Temps réel aux arrêts

- **Date :** 2026-11-25
- **Statut :** acceptée (pour la phase de conception ; le temps réel reste hors du MVP, décision D15)
- **Vérification de phase 0 :** 10 (voir `docs/PRD-v2.md` §9)

## Question

Les flux temps réel TEC (SIRI et GTFS-RT) donnent-ils des retards fiables et frais pour les lignes pilotes ? Par quelle adresse les appeler ?

## Ce qui a été testé

- Clé Belgian Mobility (compte Standard) chargée depuis le coffre DevContext dans une variable, jamais affichée ni écrite.
- Adresse qui fonctionne : la passerelle Azure de Belgian Mobility, en-tête `bmc-partner-key`. L'autre adresse (`api.belgianmobility.io`) répond **401** avec cette clé.
- Flux appelés le 25/11/2026, en soirée :
  - SIRI Estimated Timetable (ET) et Vehicle Monitoring (VM), plusieurs relevés ;
  - GTFS-RT `trip-update`, `vehicle-position` et `alert` (servis en **JSON**, pas en protobuf), relevé de 21 h 42.
- Scripts `spikes/tec-realtime/analyze.py` (SIRI) et `analyze_gtfsrt.py` (GTFS-RT), lancés avec `python -I`. Données dans `data/raw/` (ignoré par git).

## Résultats

Vérifié, SIRI :

- ET : environ 2 000 courses, dont seulement **313 à 327** avec des heures prévues ; **1 043** marquées supprimées. Jointure avec le GTFS : ligne 100 %, course 100 %, arrêt 99,2 %. Retard p90 : 300 à 360 s. Chaque appel pèse environ **13 Mo**.
- Lignes pilotes dans ET : **0 à 1** course suivie sur 8 prévues.
- VM : **810 à 842** véhicules. Âge de la position : médiane 4 à 16 s ; pas entre deux relevés 30 à 77 s. Lignes pilotes : **6 courses sur 7 à 8** ont une position.

Vérifié, GTFS-RT :

- `trip-update` répond **200** avec la clé (contre 404 sans clé). 1 286 courses : 208 prévues, **1 078 supprimées** (sans détail par arrêt), ce qui recoupe SIRI.
- 7 207 mises à jour d'arrêt : 5 869 « pas de donnée », 1 176 prévues, 162 arrêts sautés.
- 87 courses seulement portent un retard : médiane 0 s, p90 180 s, de −480 s à 1 020 s.
- Aucun horodatage utile par course : on ne peut mesurer la fraîcheur que par l'en-tête du flux.
- Lignes pilotes : **1** course avec mise à jour.
- `vehicle-position` : 139 véhicules seulement (contre 810 à 842 en SIRI VM), tous retrouvés dans `trip-update`.
- `alert` : 3,4 Mo.

Supposé, non vérifié :

- Que les comptes « lignes pilotes » sont justes. Deux biais possibles : le script SIRI calcule minuit dans le fuseau du relevé (décalage d'une heure si le relevé est en UTC) ; le script GTFS-RT ne reconnaît une course pilote que par son `routeId`, pas par son `tripId`. À corriger au prochain relevé.
- Que l'horodatage par course vaut vraiment 0 : le script ne distingue pas 0 d'une valeur absente. La conclusion ne change pas (fraîcheur lue dans l'en-tête du flux).

- Que la faible couverture vient de l'heure tardive. Il faut un relevé en heure de pointe.
- Que les suppressions massives sont réelles et pas un artefact du flux.
- Si le quota de 12 000 appels par jour (ADR 0002) compte par clé ou par adresse IP, et ce que renvoie un dépassement (code 429, en-têtes).

## Décision

- Adresse retenue : la passerelle Azure avec l'en-tête `bmc-partner-key`. La clé reste côté serveur (ADR 0002).
- Source principale du retard : les **positions de véhicules SIRI VM**, projetées sur le tracé du paquet de ligne (ADR 0003) et comparées à l'horaire. Les heures prévues (SIRI ET, GTFS-RT) servent de contrôle quand elles existent.
- Les suppressions sont affichées avec prudence (« annoncée supprimée ») tant qu'on ne les a pas confrontées au terrain.
- Un seul appel serveur partagé, avec cache, pour tous les utilisateurs : pas d'appel direct depuis le téléphone.
- Le temps réel reste hors du MVP (D15) et arrive avec M5 / M6.

## Conséquences

- PRD §9 point 10 : mise à jour (200 avec clé sur la passerelle Azure, couverture faible des prévisions, VM retenu).
- À refaire avant M5 : un relevé en heure de pointe un jour de semaine, et un test de quota (429).
- Risque : si TEC réduit le flux VM, le retard calculé disparaît. L'app doit alors retomber sur l'horaire théorique, clairement signalé.
