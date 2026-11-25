# Vérifications techniques — 24 novembre 2026

Tests réalisés sur les données publiques TEC (Belgian Mobility Open Data), en accès anonyme, sans code d'application. Scripts de sonde gardés hors du dépôt.

## GTFS statique TEC

- URL du PRD valide : `.../api/gtfs/feed/tec/static` → zip de 97 Mo (915 Mo décompressé), version du 23/11/2026, valable jusqu'au 9 février 2027. Un seul agency : `LETEC`. 852 lignes, 46 571 arrêts, 229 904 courses.
- `shapes.txt` présent (240 Mo) et **dense** : sur 12 lignes de la zone pilote, écart médian de 10 à 16 m entre deux points. Les tracés suivent bien les routes : le guidage sur l'itinéraire est faisable à partir des données publiques.
- `block_id` renseigné sur 99,96 % des courses : permet d'enchaîner les courses d'un même bus. À confronter à un vrai planning (un service conducteur ne correspond pas forcément à un bloc).
- Vérifié le 25/11/2026 : `trip_headsign` est rempli sur 100 % des courses (destination affichée de chaque course, ex. « FLEMALLE Centre Culturel ») et `route_long_name` donne le parcours (65 = « Liège - Aywaille - Remouchamps », 64 = « Liège - Banneux - Aywaille », 63 = « Liège - Esneux - Comblain-au-Pont », 142 = « Esneux - Trois-Ponts - Gouvy », E69 = « Liège - Bastogne - Arlon »). **Piège :** le numéro de ligne n'est pas unique en Wallonie (quatre lignes « 65 », six lignes « 10 ») : toujours identifier une ligne par son `route_id` et filtrer par zone.
- Aucune information sur l'exploitant réel (sous-traitant) ni sur les dépôts : ce référentiel sera à construire par nous.
- 26 lignes desservent la zone pilote (Sprimont, Florzé, Aywaille, Remouchamps, Louveigné, Banneux, Comblain, Flémalle), dont 63, 64, 65, 727, 362, 142, 165, 10, E69, 87, 88, 89, 92, 342, 442.

## Planning employeur (captures de l'app Keolis, 25/11/2026)

Captures dans `docs/cadrage/exemples/` (dossier à exclure de git : données personnelles de Thierry).

- Planning par jour : code de service (« 201 », « 207 », suffixe « NSA »), « SERDIV », « Non travaillé », heures de début et de fin.
- Un service = liste de tâches : heure, lieu (« Banneux.Dépôt », « Liège, Gare des Guillemins Quai D »), **type** (`COM` = course commerciale, `HLP` = haut-le-pied), **ligne** interne (« T105S », différente du numéro public), durée, **véhicule** (« 505050 »), **numéro de course** (« 64-3 » = ligne publique 64), observations (« Obs : 67|12*45 »), coupures (« Coupure 7 mn »).
- Synthèse : `TTE`, `TD`, `Amplitude` (201 : 07:28 / 08:25 / 11:15 ; 207 : 05:24 / 05:38 / 12:23).
- **Lien planning ↔ GTFS vérifié (25/11/2026) :** la course « 64-3 » du service 201 (départ 07:47 de Liège Gare des Guillemins quai D, arrivée 08:58 à Aywaille Gare SNCB) correspond exactement à une course GTFS de la ligne 64 Liège–Banneux–Aywaille (même départ, même arrivée, 66 arrêts). La ligne 64 fait une **boucle dans Banneux** (mêmes arrêts à l'aller et au retour), point d'attention pour le guidage.
- **Services coupés** confirmés : 207 = 07:29-08:34 puis 15:19-19:52 au dépôt de Banneux.
- À clarifier au fil du temps (l'app Keolis est nouvelle, Thierry ne connaît pas encore tous les codes) : sens exact de `TTE`, `TD`, des codes « Obs », de « T105S » et de « NSA ». Le véhicule « 505050 » serait le numéro complet du bus (hypothèse de Thierry, 25/11) ; lien avec la référence SIRI (`V5220_3197`) à établir.

## Temps réel SIRI

- **Vehicle Monitoring** (`?format=json`) : 200, 249 Ko. À 19:42, 419 bus suivis, dont 77 dans la zone Liège–Ourthe–Amblève. Âge des positions : médiane 10 s, p90 12 s (mieux que les 30 s annoncés). Champs : ligne, sens, course, position, cap, référence véhicule (`V5220_3197`, à comparer aux numéros de parc).
- Liens avec le GTFS : **100 %** des courses et des lignes se retrouvent après normalisation des identifiants (`:` et `-` remplacés par `_`).
- Bus en circulation au moment du test sur les lignes pilotes 65, 63, 10, E69, 87, 88, 89. `OperatorRef` vaut toujours `tec` : impossible de distinguer un bus sous-traitant dans le flux, mais la ligne 65 est bien couverte.
- **Situation Exchange** : 2 293 perturbations, la moitié avec arrêts ou localisation. Beaucoup ont une fin de validité en 2200 (perturbations « permanentes ») : filtrage nécessaire. Exemples sur les lignes pilotes : 63 (44), 10 (30), 65 (14), 88 (12).
- **Estimated Timetable** : 200, 10 Mo par appel : trop lourd à interroger souvent sans filtrage côté serveur.

## Points négatifs

- Les URL GTFS-RT du PRD (`opendata-discovery-gtfs-realtime...`) ne résolvent pas en DNS : obsolètes. Le SIRI suffit.
- L'accès anonyme est prévu pour l'exploration ; un compte développeur gratuit et une clé (`bmc-partner-key`) seront nécessaires avant usage réel. Quotas non encore lus.

## Supabase

- Le projet `jdnukbpkjyyyjpuwgxhv` est la base de production de **Terminal Learning** (org `yitotclnoikooytmyqlg`, eu-west-1). Il ne doit pas accueillir cette app : projet dédié recommandé.

## Nom

- Copibus : aucun produit ni société homonyme trouvé par recherche web ; nom proche dans le secteur : Cobus Industries (bus d'aéroport, Allemagne). Marques BOIP/EUIPO non vérifiées. Le nom n'est pas encore décidé ; `copibus` est un nom de dossier provisoire.
