# Recherche : ce que font les autres applis (25 novembre 2026)

Trois recherches web menées le 25/11/2026 : les applis voyageurs, les applis pour chauffeurs, et ce que l'iPhone et les données TEC permettent techniquement. Une cinquantaine de sources ont été consultées. Beaucoup viennent du marketing des éditeurs : leurs chiffres de gain sont déclarés, pas vérifiés. Légende : **[V]** lu dans la source, **[I]** déduction.

## 1. Ce qu'il faut retenir

1. **Le guidage sur le tracé officiel, pour un chauffeur qui ne connaît pas la ligne, n'existe presque nulle part.** Seuls deux projets français visent ce cas : Regul'Bus (projet, pas de date) et Tott up / Flexnav (Hubup, commercial et fermé). Les GPS grand public (Sygic, CoPilot) calculent leur propre itinéraire et ignorent les arrêts. C'est le point fort de Copibus. [V]
2. **Aucun produit trouvé ne combine** détection automatique de la course (GPS + horaire), rappel de prise de service et alerte. La scène « tu as oublié de me lancer » est un espace libre. [V/I]
3. **Le grief n°1 des voyageurs, ce sont les horaires faux** : un horaire prévu affiché comme s'il était en direct fait rater des bus (Google Maps, Transit, Bus Checker). Il faut trois états impossibles à confondre : **en direct**, **prévu** et **supprimé**. [V]
4. **En roulant, presque tous les produits verrouillent l'écran** : DriverMate bloque l'app, Swiftly montre une interface minimale. En Belgique, l'article 8.4 du code de la route interdit de manipuler un écran qui n'est pas dans un support fixe, sauf à l'arrêt réel (174 €) ; un feu rouge ou un bouchon ne comptent pas comme un arrêt. Copibus suit déjà ce principe : zéro contact en conduite. [V]
5. **Sur iPhone (app web), EVE ne peut pas détecter l'arrivée à un arrêt quand l'app est fermée.** Elle peut en revanche envoyer une notification à l'heure prévue (Web Push, iOS 16.4+). La vraie détection d'arrivée, appelée « géorepérage », viendra avec l'app Android. [V]

## 2. Applis voyageurs : ce qu'on reprend

| Appli | À copier | Faiblesse connue |
|---|---|---|
| **Transit** | ondes qui pulsent = en direct, gris = horaire prévu, barré = supprimé ou arrêt sauté ; détection automatique des déviations (arrêts fermés marqués d'une croix) ; alertes limitées à des plages horaires | heures d'arrivée jugées fausses, batterie |
| **Google Maps** | ponctualité en couleur : vert à l'heure, orange en avance, rouge en retard, noir sans temps réel ; barre de trajet toujours visible en bas | horaires prévus présentés comme en direct |
| **Citymapper** | accueil à deux gros boutons ; trajet réel de la déviation en trait distinct | suggestions irréalistes |
| **Moovit** | alerte « descendez » par une vibration distincte ; compatible VoiceOver et TalkBack | temps réel incomplet, publicités |
| **Apple Maps** | « transports à proximité » : lignes proches avec départs et retards, lignes épinglées en haut | couverture limitée |
| **TEC (officielle)** | favoris (adresses, lignes, arrêts), position des bus | note 2,4/5 : lenteurs, bugs, bus cachés sur la carte |
| **De Lijn** | « mode simple » à gros boutons (mars 2026) ; affluence par course | rien sur les déviations ni le hors ligne |
| **OneBusAway** | bouton « l'heure affichée est fausse » qui envoie l'heure affichée, la source et l'écart | rappels parfois silencieux |

Sources principales : help.transitapp.com, support.google.com/maps/answer/6142130, yrt.ca (déviations Citymapper), apps.apple.com/be/app/tec/id1438618535, delijn.be, newmobility.news (mode simple De Lijn), github.com/CUTR-at-USF/onebusaway-android.

## 3. Applis chauffeurs : ce qu'on reprend

| Produit | À copier | Limite |
|---|---|---|
| **Pysae** (France) | guidage tour par tour, avance/retard, déviations envoyées par le régulateur, rapports d'incident prédéfinis liés à la course | déviations seulement dans l'offre Premium |
| **Swiftly Onboard** | état honnête « chrono indisponible » plutôt qu'un faux retard ; **passe tout seul en vue carte à l'approche d'une déviation**, avec l'ancien tracé grisé et les arrêts fermés | choix du trajet à la main |
| **Optibus Driver** | tâches du jour, notifications de changement de service, demandes d'échange et de congé dans l'app (−50 % d'appels au poste de contrôle selon l'éditeur) | pas de navigation |
| **Trapeze DriverMate** | verrouillage de l'écran quand le véhicule roule ; bilan de fin de journée | conçu pour le transport à la demande |
| **Flexnav (Hubup)** | « conseils de formateur » sur les points délicats de la ligne : rond-point étroit, arrêt difficile, gabarit | produit fermé |
| **Samsara / Fleetio** (contrôle avant départ) | photo prise sur place obligatoire, vérification de fraîcheur, défaut qui reste ouvert pour le chauffeur suivant jusqu'à sa clôture par l'atelier | fonctions IA en bêta |

Le TEC utilise déjà HASTUS SelfService (GIRO) en version web pour les demandes des chauffeurs. Aucune appli chauffeur publique n'a été trouvée chez Keolis ou Transdev.

Sources principales : pysae.com/platform/operations, swiftly.zendesk.com (Onboard App Basics), apps.apple.com/us/app/optibus-driver/id1661525117, collaborate2.trapezegroup.com (DriverMate), data.gouv.fr/organizations/regulbus, kb.samsara.com (DVIR 2.0), help.fleetio.com, police.be/5337.

## 4. Ce que l'iPhone et les données permettent

| Question | Verdict | Conséquence pour Copibus |
|---|---|---|
| Notification à heure fixe sur iPhone (app web installée) | **possible** (Web Push, iOS 16.4+, sans compte Apple Developer) | rappel « ta course part dans 15 min » envoyé par le serveur à partir du planning |
| Détecter l'arrivée à un arrêt, app fermée, sur iPhone | **impossible** en app web | à l'ouverture, EVE compare la position et le planning ; la détection automatique viendra avec l'app native |
| Raccourcis iOS « en arrivant à… » / CarPlay / Bluetooth | **à tester** : selon les sources, une confirmation reste parfois demandée ; `webapp://` ouvre l'app mais sur l'accueil | test sur l'iPhone 14 en phase 0 |
| Géorepérage Android (Capacitor) | **possible**, travail natif | une zone autour de chaque point de départ du jour déclenche une notification importante |
| Reconnaissance vocale dans l'app web iPhone | **peu fiable** | champ texte + **micro du clavier iOS** (dictée), qui marche partout ; écoute « Hé EVE » sur Android natif |
| Temps réel à un arrêt | **possible** | SIRI Estimated Timetable (vérifié le 24/11, 10 Mo par appel) filtré et mis en cache côté serveur, ou retard calculé à partir des positions SIRI. Le flux GTFS-RT TripUpdates répond 404 sans clé (testé le 25/11) : à revérifier avec la clé |

Sources : webkit.org/blog/13878 (Web Push iOS), firt.dev/notes/pwa-ios, developer.android.com (services de premier plan, géorepérage), source.android.com/docs/core/permissions/fsi-limits, matthewcassinelli.com (automatisations).

## 5. Ce qui a été ajouté au design le 25/11/2026

- **Prochains passages à un arrêt** : vraie liste TEC d'Aywaille Gare SNCB. Chaque bus porte un état en mots **et** en icône (à quai, à l'heure, retard, avance, prévu). Un point qui pulse signale le suivi en direct, un cercle pointillé l'horaire prévu. Ta course est mise en avant, et un filtre « Départs d'ici » est disponible.
- **EVE prend les devants** : notification à l'heure prévue, puis, à l'ouverture, « Tu es à Aywaille Gare, ta course 65 vers Liège part à 09:24, le bus est déjà à quai ». EVE dit **ce qu'elle a vu** (position, planning, TEC en direct) pour qu'on puisse lui faire confiance.
- **Parler à EVE** : « Je dois faire la 727 vers Verviers ». EVE trouve la seule ligne 727 du TEC et propose les départs : 17:48 d'ici, 57 arrêts, ou la ligne complète depuis Houssonloge, 72 arrêts. Elle signale aussi ce qu'il faut savoir : le tronçon jamais fait, le quai A à Verviers Gare Centrale dans ce sens, une déviation. Ensuite, un bouton « Charger et guider ».
- **Navigation** : un bouton EVE central dans la barre du bas, présent sur tous les écrans principaux. L'écran Guidage offre deux sorties : la ligne ouvre la liste des arrêts, le bouton « Éco » passe en mode économie. Le mode économie se quitte d'un toucher. Le bandeau de déviation ouvre la carte.

## 6. Idées retenues pour la suite, par valeur

1. **Notes de terrain par point délicat de la ligne** (Flexnav) : rond-point étroit, arrêt mal placé, gabarit. EVE les annonce avant le point, et les collègues les enrichissent (cela existe déjà en partie avec les notes du collègue).
2. **Passage automatique en carte à l'approche d'une déviation** (Swiftly), avec l'ancien tracé grisé et les arrêts fermés barrés.
3. **« Chrono indisponible » plutôt qu'un faux retard** : ne jamais inventer d'état temps réel.
4. **Rappel de prise de service** par notification, réglé sur le planning, avec une plage silencieuse (Transit).
5. **Défaut véhicule qui reste ouvert** pour le chauffeur suivant tant que l'atelier ne l'a pas clôturé (Fleetio).
6. **Bouton « cet horaire est faux »** (OneBusAway) : il améliore les données et rassure le chauffeur.
7. **Mode simple** (De Lijn) : un réglage « gros boutons » pour ceux qui le préfèrent.
8. **Bilan de fin de service** (DriverMate) : déjà prévu dans Fin de service.
9. **Plus tard** : changements de service poussés par le dépôt, et échanges de service (Optibus, INIT). Cela suppose un accord de l'employeur.

## 7. Pièges à éviter

- Un guidage « voiture » calculé sur un bus : mauvais tracé, arrêts ignorés, gabarit inconnu.
- Toute interaction en roulant : contraire à l'article 8.4 et au principe « zéro contact ». Un support fixe est à exiger dans le guide d'installation.
- Afficher un retard faux au lieu de « indisponible ».
- Un outil perçu comme de la surveillance (chronométrer le chauffeur) : à cadrer avec les représentants du personnel avant tout partage de données vers l'employeur.
- Matériel posé sur les véhicules (étiquettes NFC) : irréaliste avec des bus partagés ou de sous-traitants.
- Ne rien affirmer sur un retrait de permis lié au téléphone tant que la source officielle belge n'est pas confirmée.

## 8. Navettes de remplacement SNCB (recherche complémentaire du 25/11/2026)

| Source | Ce qu'elle donne | Limite |
|---|---|---|
| **GTFS SNCB** (sncb-opendata.hafas.de, accès anonyme) | 75 lignes `BUS` (`route_type` 700), 1 530 courses avec n° de train, horaires, gares desservies | publiées environ 5 semaines à l'avance ; les arrêts sont les gares elles-mêmes, sans position de l'arrêt de bus ni tracé |
| **GTFS-RT SNCB / iRail** | alertes en texte | clé nécessaire ; la SNCB dit n'avoir aucun temps réel sur ses bus (seul un pilote existe, Luttre–Manage) |
| **Infrabel** (`langetermijnplanning-tcr-spoornetwerk`) | travaux planifiés : ligne, dates, tracé GeoJSON, impact | aucune information sur les bus |
| **Feuilles de route** | aucune source publique | données du coordinateur SNCB ou de l'exploitant |
| **Valhalla**, en mode « bus » (MIT) | itinéraire adapté à la hauteur, la largeur, la longueur et le poids ; hors ligne possible | les limites de hauteur et de poids d'OpenStreetMap sont incomplètes en Wallonie |

Conclusion : horaires et gares en automatique ; arrêt exact devant la gare et trajet validé saisis par le chauffeur ou le dépôt, puis partagés. Sources : transportdata.be (jeu SNCB), github.com/iRail/iRail/issues/474, opendata.infrabel.be, valhalla.github.io (référence de l'API), belgiantrain.be (laboratoire d'innovation, bus de remplacement).
