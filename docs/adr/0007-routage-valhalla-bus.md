# 0007 — Routage Valhalla en mode bus, et où l'héberger

- **Date :** 2026-11-25
- **Statut :** acceptée (en partie : gabarit du véhicule et hébergement réel restent à faire)
- **Vérification de phase 0 :** 12, partie routage (voir `docs/PRD-v2.md` §9)

## Question

Valhalla, réglé pour un bus, retrouve-t-il le parcours réel des lignes 64 et 65 quand on lui donne les arrêts dans l'ordre ? Donne-t-il des consignes de conduite en français ? Que faut-il pour le faire tourner ?

## Ce qui a été testé

- Image Docker `ghcr.io/valhalla/valhalla:latest`, en local seulement (`127.0.0.1:8002`), arrêtée après le test.
- Données : extrait OpenStreetMap de la Belgique chez Geofabrik (`belgium-latest.osm.pbf`, 700 Mo, somme de contrôle vérifiée).
- Script `spikes/valhalla/compare_routes.py` (Python lancé avec `-I`). Pour un parcours du paquet de ligne (ADR 0003), il demande un itinéraire bus passant par tous les arrêts dans l'ordre, puis mesure l'écart entre le tracé Valhalla et le tracé TEC, dans les deux sens.
- Parcours testés : le plus long de chaque sens, pour `gr:tec:L0064-24183` et `gr:tec:L0065-24185` (66 à 71 arrêts, 34 à 36 km).

## Résultats

Vérifié (rapport `data/raw/valhalla/compare-report.json`) :

- Construction des données routières de toute la Belgique : **7 min 17 s**, **447 Mo** de tuiles (plus 134 Mo de fichiers de fuseaux et de frontières).
- Temps de réponse : 0,09 à 0,58 s par itinéraire de 70 arrêts.
- La limite par défaut est de 50 points par itinéraire bus : il a fallu la porter à 100 (`service_limits.bus.max_locations`).

| Parcours | Longueur TEC | Longueur Valhalla | Écart médian | Part à plus de 30 m |
|---|---|---|---|---|
| 64 aller | 34,9 km | 37,5 km | 1,1 m | 5,6 % |
| 64 retour | 35,8 km | 37,9 km | 1,2 m | 6,1 % |
| 65 aller | 36,1 km | **54,9 km** | 2,1 m | 33 % |
| 65 retour | 33,6 km | **56,5 km** | 2,5 m | 38 % |

- Le tracé TEC est presque entièrement couvert par Valhalla : 95 % de ses points sont à moins de 8 m.
- Sur la 65, **un seul tronçon** fausse tout : de « REMOUCHAMPS Grottes » à « REMOUCHAMPS Gare », 580 m pour le TEC, **16 km** pour Valhalla. Le reste du parcours colle.
- Sur la 64, Valhalla ajoute 2 à 2,6 km de détours locaux (écart maximal 330 m).
- Les consignes sont en français et précises, par exemple « Tournez à droite dans Quai des Ardennes/N633 » ou « Entrez dans le rond-point et prenez la 2e sortie vers Aywaille ». On compte 57 à 112 manœuvres par parcours.

Supposé, non vérifié :

- Cause du détour de 16 km : sans doute une restriction dans OpenStreetMap (sens unique, accès bus, virage interdit) près de la gare de Remouchamps. Pas encore regardé sur la carte.
- Les réglages de gabarit (hauteur, largeur, longueur, poids) n'ont pas été testés : tous les essais utilisent le bus par défaut.
- Hébergement : les limites ci-dessous viennent de la documentation connue des services, pas d'un essai. Aucun compte n'a été créé ni activé.
  - Vercel Functions, Cloudflare Workers et Supabase Edge Functions ne peuvent pas faire tourner Valhalla : c'est un programme natif qui a besoin de ses 450 Mo de tuiles sur disque et de plusieurs centaines de Mo de mémoire.
  - Il faut une petite machine ou un conteneur permanent (2 Go de mémoire, 1 Go de disque environ).

## Décision

1. **Le tracé de référence reste celui du TEC.** Valhalla ne remplace jamais le parcours officiel : il sert à produire les consignes de carrefour et à calculer les déviations.
2. Les consignes de la ligne sont calculées **à la fabrication du paquet de ligne**, sur notre poste ou en CI, pas sur le téléphone ni à la demande. Le paquet les embarque : le guidage marche hors ligne.
3. **Garde-fou obligatoire** : pour chaque tronçon entre deux arrêts, si Valhalla dépasse le TEC de plus de 50 % (et de plus de 300 m), on garde le tracé TEC sans consigne et on signale le tronçon. Sur la 65, ce contrôle aurait isolé Remouchamps.
4. Les itinéraires passent par lots de 50 arrêts au plus, ou la limite est relevée dans notre configuration.
5. Le **calcul de déviation à la demande** (route barrée) a besoin d'un serveur Valhalla. Il est repoussé au module M5b. Le choix de l'hébergeur (une petite machine payante) revient à Thierry.
6. Hébergement des fichiers statiques (PMTiles de l'ADR 0006, paquets de ligne) : avec l'app elle-même au départ (14 Mo, mis en cache une fois). Cloudflare R2, sans frais de sortie, est une option pour plus tard, **seulement avec l'accord de Thierry** (R2 n'est pas activé).

## Conséquences

- Le générateur de paquet de ligne (ADR 0003) doit appeler Valhalla, découper par tronçons et appliquer le garde-fou.
- Attribution : « © OpenStreetMap » (ODbL). Valhalla est sous licence MIT.
- À faire avant le module M5b :
  - comprendre le détour de Remouchamps, et le signaler dans OpenStreetMap s'il s'agit d'une erreur ;
  - tester le gabarit d'un bus TEC ;
  - chiffrer l'hébergement.
- La 727 n'a pas été testée.
