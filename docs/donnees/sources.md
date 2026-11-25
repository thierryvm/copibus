# Sources de données

Liste des sources utilisées en phase 0. **Aucune clé ni aucun identifiant de compte ici** : le dépôt est public. Les clés sont dans le coffre DevContext et les identifiants dans `.claude/infra.local.md` (non versionné).

Dernière vérification : 25/11/2026.

## 1. Belgian Mobility (clé requise)

- Adresse : `https://api-management-opendata-production.azure-api.net`
- Authentification : en-tête `bmc-partner-key` (clé du compte Standard, chargée en mémoire seulement). L'autre adresse, `api.belgianmobility.io`, répond 401 avec cette clé.
- Toujours appeler en **GET** : une requête HEAD répond 404 sur les flux temps réel, même quand le flux existe.
- Mise à jour du temps réel : environ toutes les 30 s. Quota : voir ADR 0002.
- Attribution obligatoire dans l'app : « Belgian Mobility Company ».

| Flux | Chemin | Taille relevée |
|---|---|---|
| TEC, GTFS statique | `/api/gtfs/feed/tec/static` | 92,7 Mo |
| TEC, GTFS-RT trip-update | `/api/gtfs/feed/tec/rt/trip-update` | 0,9 à 4 Mo |
| TEC, GTFS-RT alert | `/api/gtfs/feed/tec/rt/alert` | 3,2 Mo |
| TEC, GTFS-RT vehicle-position | `/api/gtfs/feed/tec/rt/vehicle-position` (au singulier ; le pluriel répond 404) | 0,1 Mo |
| TEC, SIRI Vehicle Monitoring | `/api/siri/feed/tec/vehicle-monitoring?format=json` | 0,1 Mo |
| TEC, SIRI Situation Exchange | `/api/siri/feed/tec/situation-exchange?format=json` | 2,3 Mo |
| TEC, SIRI Estimated Timetable | `/api/siri/feed/tec/estimated-timetable?format=json` | 8,7 à 13 Mo |
| SNCB, GTFS statique | `/api/gtfs/feed/nmbssncb/static` | 7,2 Mo |
| SNCB, GTFS-RT trip-update | `/api/gtfs/feed/nmbssncb/rt/trip-update` | 0,2 Mo |
| SNCB, GTFS-RT alert | `/api/gtfs/feed/nmbssncb/rt/alert` | 0,1 Mo |

Les flux GTFS-RT sont servis en **JSON**, pas en protobuf (ADR 0005).

## 2. Sources sans clé (exploration seulement)

- **Ancienne passerelle anonyme TEC (SIRI)** : `https://api-management-discovery-production.azure-api.net/api/siri/feed/tec/{vehicle-monitoring|situation-exchange|estimated-timetable}?format=json`. Utile pour explorer ; pas de garantie de durée, on ne bâtit rien dessus.
- **GTFS SNCB anonyme** : `https://sncb-opendata.hafas.de/gtfs/static/c21ac6758dd25af84cca5b707f3cb3de`. Contient environ 75 lignes de **bus de remplacement** (`route_type` 700), publiées environ 5 semaines à l'avance. Les arrêts sont des gares ; pas de tracés.
- **Infrabel, travaux** : jeu `langetermijnplanning-tcr-spoornetwerk` sur `https://opendata.infrabel.be` (API Explore v2.1). Donne les travaux planifiés sur le réseau ferré, sans information sur les bus.

## 3. Faits vérifiés dans ces données

- Une ligne TEC s'identifie par son `route_id`, jamais par son seul numéro (ADR 0004). Lignes pilotes : 64 = `gr:tec:L0064-24183`, 65 = `gr:tec:L0065-24185`, 727 = `gr:tec:L0727-23616`. Plusieurs « 65 » existent en Wallonie, confirmé par Thierry sur le terrain.
- Les quais sont dans `stops.platform_code` (254 arrêts sur 46 571). À Guillemins, les 64 et 65 partent du quai D et déposent au quai C.
- La course 64-3 (07 h 47 Guillemins quai D, 08 h 58 Aywaille Gare SNCB) correspond exactement à une course du GTFS. La 64 fait une boucle dans Banneux.

## Règles d'usage

- Fichiers téléchargés dans `data/raw/` (ignoré par git), lus par des scripts Python lancés avec `-I`.
- Les horaires, arrêts et quais viennent uniquement de ces sources : l'IA ne les invente jamais.
- La clé reste côté serveur : le téléphone n'appelle jamais Belgian Mobility directement (ADR 0002, 0005).
