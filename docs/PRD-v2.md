# PRD v2 — Copilote du chauffeur de bus (nom de code « copibus »)

**Version :** 2.1 — 25 novembre 2026
**Statut :** cadrage validé par grilling (4 tours, 24-25 novembre 2026), puis relu par un agent Opus indépendant (25/11/2026). Aucun code écrit.
**Remplace :** `cadrage/EVE_PRD_Cadrage_v1.0.md` (PRD v1, ChatGPT). Le v1 reste la référence pour les règles de prudence détaillées (sections 3.10 déviations, 3.15 et 9 tachygraphe, 8 RGPD) tant qu'elles ne sont pas reprises ici.
**Sources :** `cadrage/inspirations/` (2 planches = vision cible complète), `cadrage/verifications-2026-11-24.md` (tests réels des données TEC).

---

## 0. En une page

Une application gratuite pour les chauffeurs de bus de la région liégeoise, avec une assistante vocale (« EVE » par défaut, renommable). Elle aide **avant** le service (mon service, heure de départ, véhicule), **pendant** (guidage sur l'itinéraire, prochain arrêt annoncé à voix haute, sans toucher le téléphone) et **à l'arrêt** (planning, signalements, collègues).

- **Pilote :** Thierry et une collègue, dépôts de la région liégeoise (Florzé/Sprimont, Banneux, Comblain-au-Pont, Flémalle).
- **Coût :** 0 € visé. Seule dépense possible : un nom de domaine (~10 €/an) pour l'envoi des e-mails de connexion (question ouverte, section 13). Options payantes uniquement via la clé API de l'utilisateur (IA, voix premium).
- **Indépendance :** aucune affiliation avec Keolis, le TEC ou l'OTW. Ni le nom ni l'interface n'utilisent leurs marques.
- **Technologie :** une seule base TypeScript, livrée d'abord en web app installable (PWA), conçue pour devenir une app native Android puis iOS avec Capacitor. Traitement des données TEC en Rust. Backend Supabase.
- **Développement modulaire :** MVP = socle + réseau + service du jour + guidage, puis un module à la fois.

## 1. Décisions prises pendant le cadrage

| # | Décision | Raison |
|---|---|---|
| D1 | « EVE » = nom par défaut de l'assistante ; chaque utilisateur choisit son nom, sa voix (homme/femme) et sa couleur | personnalisation ; le nom de l'app reste distinct |
| D2 | Nom de l'app non décidé ; dossier provisoire `copibus`. Aucune référence à Keolis ni au TEC dans le nom | marques déposées, risque de passer pour un outil officiel |
| D3 | En conduite : zéro contact avec le téléphone, fixé sur support. Voix et affichage passif, comme Waze. Le reste à l'arrêt. Usage confirmé comme admis par Thierry (24/11/2026) | sécurité et règlement de l'employeur |
| D4 | Le guidage GPS sur l'itinéraire fait partie du MVP, **y compris les trajets dépôt ↔ terminus (haut-le-pied)** | besoin n°1 : retrouver les trajets qu'on ne connaît plus ou pas encore |
| D5 | Pilote limité à la région liégeoise, 2 testeurs | valider l'usage réel avant d'élargir |
| D6 | Plannings visibles par tous les chauffeurs ; exemples réels utilisés pour développer, gardés hors de git | données personnelles des collègues |
| D7 | Gratuit. IA et voix premium uniquement via la clé API de l'utilisateur (Anthropic, OpenAI ou OpenRouter), liste de modèles choisie par nous pour chaque tâche | aucun coût récurrent pour le projet |
| D8 | Position des collègues = position de **leur bus** dans le flux TEC, déduite de leur service, avec leur accord révocable. Jamais de suivi de téléphone. Appel ou SMS seulement à l'arrêt | vie privée, batterie |
| D9 | Connexion sans mot de passe : code par e-mail ; double authentification (TOTP) pour l'admin. Passkeys reportés (en bêta chez Supabase depuis mai 2026). Inscription sur invitation. **Domaine d'envoi en attente** : la fonction est construite et Thierry l'utilise (le SMTP intégré de Supabase envoie aux membres du projet) ; les autres testeurs se connectent en attendant par une solution sans envoi d'e-mail (Google ou e-mail + mot de passe, à trancher en M0) | simplicité et sûreté ; pas de dépense avant le choix du nom |
| D10 | `/admin` dans l'app, réduit au pilote à : invitations, boîte de réception support, liste des bugs. Modération et santé des sources viennent avec les modules qui en ont besoin | Thierry gère les retours sans outil externe |
| D11 | Projet Supabase dédié, jamais dans la base de Terminal Learning. Développement en **Supabase local** (CLI + Docker). Projet cloud **créé le 25/11/2026** : org gratuite `copibus` sur un compte séparé des autres projets ; projet `copibus` (identifiants dans `.claude/infra.local.md`, non versionné), région Francfort (eu-central-1), RLS automatique sur les nouvelles tables, exposition automatique à l'API désactivée. Mot de passe de la base généré par Supabase et non conservé : à réinitialiser par Thierry et à ranger dans le coffre DevContext le jour où la CLI en aura besoin. Le projet se met en pause après 7 jours d'inactivité tant que le développement est local (réactivation en un clic) | isolation des données ; aucun risque pour Terminal Learning en production |
| D12 | Cadrage, design, socle et premiers modules dans Claude Code. M4 Véhicule confié à Timon comme test comparatif | quota Claude partagé ; fondations posées avec Thierry |
| D13 | Pas de Mac, pas de compte Apple Developer : iPhone = PWA. Android natif via APK installé directement. iOS natif quand le compte Apple sera financé | contrainte matérielle et budget |
| D14 | Tests sur l'iPhone 14 de Thierry et le téléphone Android de sa collègue | appareils réels du pilote |
| D15 | Le temps réel TEC (positions des bus, perturbations) sort du MVP : il arrive avec M5 et M6 | le guidage n'en a pas besoin ; moins de pièces mobiles au départ |

## 2. Principes non négociables

1. **Les données critiques sont déterministes, sourcées et datées.** L'IA explique et pilote l'interface ; elle n'invente jamais un horaire, un arrêt, une restriction, une obligation légale ni une consigne de sécurité.
2. **Zéro contact en conduite.** Aucun formulaire, clavier ni liste à faire défiler quand le véhicule roule.
3. **Honnêteté sur l'état des données.** Précision du GPS, version et date des horaires, fraîcheur des flux : toujours affichées.
4. **Aucune incitation dangereuse.** Pas d'avance/retard affiché en roulant (risque d'inciter à accélérer) ; aucune déviation présentée comme sûre sans validation humaine (PRD v1, section 3.10).
5. **Sécurité par défaut :** RLS sur toutes les tables, aucun secret côté client, moindre privilège, revue sécurité Opus avant chaque mise en ligne qui touche l'authentification, les données, les fonctions serveur, la CI ou du contenu utilisateur transmis à une IA.
6. **Gratuit pour les fonctions essentielles,** sans publicité ni revente de données.
7. **Pas d'affiliation simulée :** mention « application indépendante, non affiliée au TEC ni à Keolis » dans l'app et sur le site.
8. **Le guidage ne dépend jamais du réseau ni d'une session valide :** une fois le service préparé, tout fonctionne hors connexion.

## 3. Utilisateurs du pilote

- **Chauffeur en reprise ou débutant** (Thierry) : ne connaît plus tous les parcours, veut être guidé et rassuré, y compris pour rejoindre le terminus depuis le dépôt.
- **Chauffeuse expérimentée** (la collègue) : veut gagner du temps, être prévenue tôt, signaler vite.
- **Admin plateforme** (Thierry) : invitations, support, bugs, sécurité.

Rôles techniques : `driver`, `referent` (valide les notes terrain et les trajets haut-le-pied), `org_admin`, `platform_admin`. Un chauffeur peut être rattaché à **plusieurs dépôts**.

## 4. Expérience utilisateur

### 4.1 La règle du moindre clic (exigences mesurables)

| Exigence | Cible | Vérification |
|---|---|---|
| Contacts avec l'écran pendant la conduite | 0 | revue de chaque écran du mode conduite ; essai réel |
| Actions courantes depuis l'accueil (mon service, ma ligne, check-list, signaler, écrire au support) | ≤ 2 touchers | parcours chronométrés dans Playwright |
| Démarrer le guidage du service du jour | 1 toucher (« C'est parti »), qui débloque aussi le son | test e2e + iPhone 14 |
| Ouverture de l'app (PWA installée, 4G faible) | < 2 s jusqu'à l'écran utile | Lighthouse CI + mesure sur l'iPhone 14 |

### 4.2 Accueil contextuel

- **Avant le service :** service du jour, heure de départ conseillée de chez soi, météo utile, bouton « C'est parti ».
- **En service (guidage) :** carte, tracé, prochain arrêt (nom, distance), consigne au prochain carrefour, alerte hors parcours. EVE annonce à voix haute.
- **En pause / battement / à l'arrêt :** temps restant, avance/retard de la course écoulée, prochaine course, notes terrain de la prochaine ligne.
- **Après le service :** récapitulatif, envois en attente.
- **Arrivée à un point de départ (EVE prend les devants) :** quand le chauffeur ouvre l'app près d'un arrêt où commence une course de son planning, EVE la propose aussitôt (« Tu es à Aywaille Gare, ta course 65 vers Liège part à 09:24, le bus est déjà à quai ») avec ce qu'elle a vu : position, planning et TEC en direct. Un toucher charge la course. Avant chaque reprise, une notification arrive à l'heure prévue par le planning (Web Push, possible dans l'app web iPhone), avec une plage silencieuse réglable. La détection d'arrivée **app fermée** (géorepérage) n'existe pas dans une app web iPhone : elle viendra avec l'app Android, puis iOS native.

Navigation (révisée le 25/11/2026) : barre du bas à 5 places, soit 4 onglets (Aujourd'hui, Carte, Lignes, Moi) et un **bouton EVE central** toujours présent. Chaque écran a une sortie visible : retour, fermer ou lien. Les écrans de conduite n'ont que de grandes sorties, utilisables à l'arrêt :
- un bouton « Menu » de 88 px, symétrique de « Silence », ramène à l'accueil ;
- la ligne ouvre la liste des arrêts ;
- « Éco » passe en mode économie ;
- le bandeau de déviation ouvre la carte.

Les libellés de la barre sont alignés sur une même ligne de base, et le bouton EVE dépasse vers le haut sans décaler les autres libellés.

Contrastes vérifiés le 25/11/2026 par un script sur les 24 maquettes, avec les 5 couleurs d'accent (cyan, vert, ambre, lavande, rose) : 2 350 textes contrôlés, tous au-dessus de 4,5:1 (le plus faible à 5,06:1). Le texte sombre sur un bouton d'accent atteint au moins 8,9:1. Un défaut non textuel est corrigé : le rond d'un choix non coché passe de 1,3:1 à 4,1:1. La règle reste : une couleur d'accent n'est proposée que si elle atteint ces seuils sur les fonds de l'app.

### 4.3 Mode conduite

- Activé par « C'est parti » ; détecte le mouvement par la vitesse GPS.
- Écran maintenu allumé (Screen Wake Lock), repris automatiquement quand l'app revient au premier plan.
- Interface : très grands caractères, contraste maximal, aucune liste, aucune saisie, aucune donnée d'avance/retard.
- Voix : annonces courtes et non répétitives, débit réglable, compatibles avec une sortie Bluetooth. Si le téléphone est en silencieux, un avertissement visuel le signale avant le départ.
- **Mode déviation :** si le bus quitte le tracé (déviation, travaux), une seule annonce, puis silence ; recalage automatique au retour sur le tracé. Un gros bouton « silence » est utilisable à l'arrêt.
- **Mode économie :** carte remplacée par un affichage simplifié (prochain arrêt, flèche, distance) pour limiter la chauffe et la batterie au pare-brise.
- MVP : EVE **parle** mais n'écoute pas. L'écoute par mot d'activation (M7a) arrive avec l'app Android native ; sur iPhone, elle attend l'app iOS native (la reconnaissance vocale n'est pas fiable dans une PWA installée).

### 4.4 Personnalisation

Nom de l'assistante, voix (parmi les voix du téléphone, homme/femme), débit, couleur d'accent (refusée si le contraste calculé n'atteint pas WCAG 2.2 AA), taille du texte, thème sombre par défaut.

### 4.5 Accessibilité

WCAG 2.2 AA mesuré (contrastes, cibles tactiles ≥ 44 px, jamais la couleur seule, mouvement réduit, zoom sans perte). Pensé pour des utilisateurs âgés, avec lunettes, daltoniens ou peu à l'aise avec le numérique. Onboarding interactif et mode démo.

### 4.6 Direction visuelle

ADN des planches d'inspiration (bleu nuit, accent cyan électrique, assistante comme visage de l'app), traduit en interface sobre : fond presque noir, une seule couleur d'accent, typographie très lisible, halos réservés à l'assistante. Trois directions avec Claude Design sur les mêmes écrans (accueil/service du jour, guidage, personnalisation), chacune avec sa mascotte (robot repensé, visage dans un phare de bus, personnage-bus). Thierry choisit ou combine. Mascotte originale : aucune ressemblance avec l'EVE de Pixar ni avec le robot généré par ChatGPT.

**Choix du 25 novembre 2026 : direction A « Halo ».** Robot copilote à casque-micro, bleu nuit et cyan, panneaux translucides sur la carte. Canevas : https://claude.ai/artifact/UPhReypoKwSxE7WDHtFL64 (privé). Exigences ajoutées par Thierry :
- chaque fonction doit être visible et facile à toucher (libellés lisibles, raccourcis de 88 px, bouton « Silence » libellé et non une icône seule) ;
- la mascotte exprime des émotions : 6 expressions (prête, parle, contente, attention, réfléchit, en pause) ; l'état « attention » change de couleur **et** de forme ;
- quand EVE parle, sa bouche suit la parole. Voix système : synchronisation par mot via les événements `boundary` de la synthèse vocale, à vérifier sur l'iPhone 14 en phase 0 (repli : rythme estimé à partir du texte). Voix premium (clé API) : l'audio passe par l'app, la bouche suit le volume réel (Web Audio `AnalyserNode`). Respect de « réduire les animations ».
- **Photos d'avarie depuis la check-list :** un toucher pour photographier ; l'heure et le n° de parc sont ajoutés. Les photos restent **sur le téléphone** 30 jours puis s'effacent toutes seules ; elles ne partent vers le responsable du dépôt que sur un toucher « Envoyer » du chauffeur. Objectif : prouver qu'une avarie existait avant la prise de service. Stockage serveur seulement à l'envoi (bucket privé, RLS, accès chauffeur + responsable). Attention RGPD : une photo peut montrer des personnes ou des plaques ; durée et destinataires à valider avec l'employeur.
- **Retour au toucher :** chaque bouton réagit dès l'appui (léger enfoncement), remplacé par un changement d'opacité si « réduire les animations » est activé.
- **Détail d'une ligne :** le sens est détecté tout seul (position GPS + cap, comparés au tracé, et service du jour), avec reprise à la main possible et un bouton « Auto » pour revenir à la détection. Les arrêts déjà desservis passent en gris avec le rail plein ; le prochain arrêt est mis en avant avec sa distance.
- **Services coupés :** un service peut avoir plusieurs parties séparées par des coupures (ex. service 207 : 07:29-08:34 puis 15:19-19:52). L'app distingue la **pause entre deux courses** (écran Pause), la **fin de partie** (coupure : heure et lieu de reprise, rappel avant la reprise en tenant compte du trajet) et la **fin de service** (récapitulatif, envois en attente, service du lendemain).
- **Apprentissage (onboarding) :** au premier lancement, EVE guide en 5 étapes de moins d'une minute chacune (nommer l'assistante et écouter sa voix, vérifier le son et le mode silencieux, installer l'app sur l'écran d'accueil, autoriser la position au moment où elle sert, choisir son dépôt et ses lignes). Ensuite, un espace « Apprendre » dans « Moi » : courtes démos interactives par fonction et un **mode démo** qui rejoue une course simulée pour s'entraîner au guidage sans conduire. Chaque étape peut être passée et reprise.
- **Admin sur ordinateur (`/admin`) :** maquette du 25/11/2026 : support, bugs (avec « Copier pour Claude »), invitations, à valider (haut-le-pied, notes terrain, photos), état des données TEC, journal de sécurité, utilisateurs (déconnexion à distance). Badge permanent « double authentification vérifiée ».
- **Recherche de toutes les lignes TEC :** l'écran Lignes cherche dans les 852 lignes de Wallonie (numéro, ville ou arrêt, sans tenir compte des accents). Chaque résultat affiche sa région TEC ; quand plusieurs lignes portent le même numéro, un avertissement le signale, et les lignes de la zone du chauffeur passent en premier. Toute ligne trouvée peut être gardée hors ligne.
- **Déviations TEC sur la carte et le guidage :** les perturbations officielles (SIRI SX) s'affichent pendant le guidage et sur la carte, avec l'itinéraire de retour vers la ligne. Très utile hors de sa région habituelle (retour de Thierry, 25/11/2026).
- **Prochains passages à un arrêt :** depuis Lignes (« Près de toi ») ou EVE, l'arrêt le plus proche affiche les prochains bus. Chaque bus a une ligne, une destination et une heure, avec un état en mots **et** en icône : à quai, à l'heure, retard, avance, prévu, supprimé. Le suivi en direct est marqué par un point qui pulse, l'horaire prévu par un cercle pointillé : un horaire prévu ne se présente jamais comme du direct. La course du chauffeur est mise en avant, et un filtre « Départs d'ici » masque les arrivées en terminus. L'écran sert à l'arrêt ou à pied, jamais en roulant.
- **Parler à EVE (ligne inconnue) :** « Je dois faire la 727 vers Verviers ». La demande passe par le micro du clavier iOS ou par écrit, et la voix seule arrive avec l'app native. EVE trouve la ligne par son `route_id`, signale si plusieurs lignes portent ce numéro, et propose les départs vers cette destination. Elle liste ce qu'il faut savoir avant de partir : tronçon jamais fait (d'après les services passés), quai à un pôle (ex. Verviers Gare Centrale quai A dans ce sens), déviation TEC, parcours gardé hors ligne. Puis un bouton « Charger et guider ». L'interprétation de la phrase est déterministe (numéro + destination, comparés au GTFS), pour respecter le principe 1.
- **Demande complète à EVE :** le chauffeur peut tout dire d'un coup, par exemple « la 727 vers Verviers, je pars du dépôt de Banneux à 17:25 et je commence à Aywaille Gare ». EVE affiche ce qu'elle a compris (ligne, destination, dépôt et heure, lieu de début), puis construit le service :
  1. trajet à vide depuis le dépôt (guidé seulement si un collègue a validé le trajet, sinon l'arrêt est montré sur la carte) ;
  2. la course qui correspond à l'heure et au lieu ;
  3. le terminus.

  Les boutons « C'est mon service » et « Corriger » laissent le dernier mot au chauffeur.
- **Quais de chargement et de dépose :** l'app indique toujours le quai où l'on charge et celui où l'on dépose. Le GTFS TEC donne un arrêt par quai (`platform_code`). Vérifié le 25/11/2026 à Liège-Guillemins : les 64, 65, 58, 63, E20, E69 et 30 **partent du quai D** ; les 64, 65, E20, E69, 32, 58, 60, 61 et 62 **déposent au quai C** ; les quais B et F servent aux 6, 59, B2 et 57. EVE l'annonce avant d'arriver (« Terminus Guillemins, dépose au quai C ») et l'affiche à la pause et dans la course proposée.
- **Navettes de remplacement (bus SNCB quand les trains ne roulent pas) :** module à part (M11), après le MVP. Ce qui peut être automatique :
  - les horaires, les gares desservies et le numéro de train, lus dans le GTFS SNCB ;
  - l'alerte précoce de travaux, depuis Infrabel ;
  - un itinéraire adapté au gabarit du véhicule entre deux points, avec Valhalla en mode « bus ».

  Ce qui doit être saisi ou importé par le chauffeur ou le dépôt : l'arrêt exact devant chaque gare (photo + point sur la carte), la feuille de route et le trajet validé. Partagés entre collègues, ces arrêts servent ensuite à tous. Les limites de hauteur et de poids d'OpenStreetMap sont incomplètes en Wallonie : la route calculée est une proposition signalée comme telle, jamais une consigne sûre, et le chauffeur reste maître de l'itinéraire.
- **Maquettes complètes (25/11/2026), direction A :** accueil, guidage, hors parcours, mode économie, pause, fin de partie / de service, carte, lignes, détail de ligne, check-list, signaler, support, connexion par code e-mail, premiers pas (5 étapes), prochains passages à un arrêt, parler à EVE, EVE prend les devants, « Moi », planning de la semaine, import du planning (photo puis vérification des champs douteux), personnalisation, expressions de EVE ; admin sur ordinateur et sur téléphone (le téléphone sert à consulter et traiter vite, la gestion complète reste sur ordinateur).

## 5. Modules

Vision cible complète = les deux planches. Développement module par module, chacun avec ses critères d'acceptation et ses tests.

| Module | Contenu | Phase |
|---|---|---|
| **M0 Socle** | comptes, invitations, profil, personnalisation, PWA installable, hors ligne, design system, `/admin` réduit, support, bugs, audit, politique de confidentialité | **MVP** |
| **M1 Réseau** | lignes, arrêts, tracés et horaires TEC de la zone pilote, fiche de ligne, notes terrain | **MVP** |
| **M3a Service du jour** | composer son service (courses + trajets haut-le-pied), enchaînement | **MVP** |
| **M2 Guidage** | carte, position, suivi du tracé, prochain arrêt, consignes aux carrefours, annonces, déviation, haut-le-pied | **MVP** |
| M3b Planning OCR | photo du planning → services → correction → versions | juste après le MVP |
| Android natif | Capacitor + APK : GPS en arrière-plan, base pour M7a | après M3b |
| M7a Voix | « Hé EVE » (nom choisi), commandes simples sans IA | Android d'abord |
| M4 Véhicule | fiches du parc, check-list, avaries avec photos, brouillon d'e-mail | test Timon |
| M5 Alertes | perturbations TEC (SIRI SX) sur le parcours, travaux SPW si accès obtenu | |
| M5b Déviations | itinéraire de remplacement calculé avec un profil **poids lourd / bus** (hauteur, largeur, longueur, masse du véhicule) : Valhalla auto-hébergé (profil bus) ou GraphHopper (profil camion). Toujours présenté comme « à vérifier », jamais comme sûr (PRD v1, section 3.10) ; requiert les dimensions du véhicule (M4) | après M4 et M5 |
| M6 Équipe | bus en circulation, collègues par ligne (consentement), signalement façon Waze, appel/SMS à l'arrêt, échanges de services | |
| M7b IA | conversation libre, recherche documentaire, via la clé API de l'utilisateur | |
| M8 Apprendre | voyants, PFE, réflexes professionnels, astuces | |
| M9 Tachygraphe | suivi indicatif, après validation juridique | |
| M10 Site vitrine | présentation, référencement, dons, nom définitif | avant toute ouverture au-delà du pilote |

### 5.1 M0 Socle — critères d'acceptation

1. **Bloquant avant toute invitation :** politique de confidentialité et registre des traitements publiés (produits avec Publiable).
2. Thierry invite sa collègue depuis `/admin` (invitation à usage unique, liée à son e-mail, valable 48 h) ; elle crée son compte avec un code reçu par e-mail, sans aide.
3. Elle choisit ses dépôts, le nom et la voix de son assistante, sa couleur ; l'app refuse une couleur au contraste insuffisant.
4. L'app s'installe sur l'écran d'accueil (iPhone et Android) et s'ouvre hors connexion sur le dernier état connu.
5. « Écrire au support » et « Signaler un bug » en ≤ 2 touchers ; le message arrive dans la boîte de réception `/admin`. Un bug crée en plus un ticket GitHub privé contenant **uniquement** un identifiant et le contexte technique (version, écran, appareil), jamais le texte libre ni de donnée personnelle.
6. Aucune donnée d'un utilisateur n'est lisible par un autre, sauf partage explicite (prouvé par des tests RLS).
7. `/admin` exige le rôle `platform_admin` **et** une session à double authentification, vérifiées côté base de données (`aal2`), pas seulement dans l'interface. L'admin peut révoquer les sessions d'un utilisateur.
8. Export et suppression de son compte en libre-service.

### 5.2 M1 Réseau — critères d'acceptation

1. Les 26 lignes de la zone pilote (liste dans `cadrage/verifications-2026-11-24.md`) sont consultables : variantes, sens, arrêts dans l'ordre, tracé, horaires d'une date choisie.
2. Les horaires respectent le calendrier réel du TEC (`calendar` + `calendar_dates` : jours fériés, congés scolaires, services partiels), les heures après minuit (> 24:00) et les changements d'heure. Tests sur des dates précises (Noël, Nouvel An, changement d'heure de mars et d'octobre).
3. Mise à jour automatique à chaque nouvelle version du GTFS TEC ; version et date de validité affichées ; un paquet périmé est refusé avec un message clair.
4. Fiche de ligne : notes terrain typées (fait, règle officielle, observation, conseil, temporaire), avec auteur, date, statut (proposée, validée, expirée, contestée).
5. Une ligne téléchargée reste consultable hors connexion.

### 5.3 M3a Service du jour — critères d'acceptation

1. Le chauffeur compose son service en ≤ 4 touchers par course : ligne → sens → heure de départ (filtrée sur l'heure courante), ou choix d'un bloc TEC.
2. Un service peut commencer **en cours de course** (relève à un arrêt) et contenir des **trajets haut-le-pied** (dépôt → terminus, terminus → terminus, retour au dépôt).
3. Une course enregistrée est identifiée de façon stable (ligne, sens, arrêt de départ, heure de départ, date), pas par l'identifiant GTFS qui change à chaque version.
4. Heure de départ conseillée de chez soi : présence requise − trajet estimé − marges (préparation, hiver). Paramétrable, présentée comme indicative.

### 5.4 M2 Guidage — critères d'acceptation

1. Le tracé de la course et la position du téléphone s'affichent ; la progression le long du tracé est calculée sur l'appareil, avec une fenêtre de recherche limitée vers l'avant (tracés qui repassent sur la même route).
2. Prochain arrêt : nom et distance ; annonce vocale à une distance réglable avant l'arrêt.
3. **Consignes aux carrefours** uniquement sur de vrais carrefours (nœuds OSM où se croisent au moins 3 routes), avec le numéro de sortie aux ronds-points. Aucune consigne dans un simple virage.
4. **Haut-le-pied :** guidage sur un trajet enregistré par un chauffeur (trace GPS) et validé par un référent. Tant qu'aucun trajet validé n'existe, l'app l'indique et ne propose pas d'itinéraire calculé comme fiable.
5. Sortie de parcours : une seule annonce, puis mode déviation (section 4.3).
6. GPS imprécis (vallée de l'Ourthe, tunnels) : estimation de la position le long du tracé selon la dernière vitesse, incertitude affichée ; rien n'est inventé.
7. Avance/retard affiché seulement à l'arrêt ou en battement.
8. Validé par le rejeu de traces GPS **réelles** des lignes 65 et 63 (enregistrées par Thierry) et de traces simulées avec bruit, puis sur l'iPhone 14 en service réel.

## 6. Architecture

### 6.1 Vue d'ensemble (MVP)

```
  Belgian Mobility (GTFS TEC)        OpenStreetMap (extrait Belgique)
            │                                    │
            ▼                                    ▼
  ┌────────────────────────────────────────────────────────────┐
  │ Pipeline Rust (CI, seulement si le GTFS a changé)          │
  │  → paquets de ligne (arrêts, tracés, calendrier, carrefours)│
  │  → tuiles PMTiles du couloir des lignes (±2 km)            │
  └───────────────┬────────────────────────────────────────────┘
                  │ fichiers statiques versionnés (Vercel)
  ┌───────────────▼──────────────── Téléphone ───────────────────────────────┐
  │ PWA (React + TypeScript)                                                  │
  │  • thread principal : watchPosition → calcul de guidage (packages/core)   │
  │  • OPFS / IndexedDB : paquets de ligne, tuiles, service du jour, file     │
  │    d'envoi hors ligne                                                     │
  │  • Service worker : coquille de l'app hors ligne                          │
  └───────────────┬──────────────────────────────────────────────────────────┘
                  │ HTTPS (Supabase JS) — seulement pour compte, notes, support
  ┌───────────────▼──────────────────────────────────────────────────────────┐
  │ Supabase (projet dédié, UE) : Auth (OTP e-mail, TOTP admin),             │
  │ Postgres + RLS, Storage privé, Edge Functions (support → GitHub)         │
  └──────────────────────────────────────────────────────────────────────────┘
  Plus tard (M5/M6) : Edge Function déclenchée par pg_cron → SIRI → un message
  broadcast agrégé par interrogation, sur canaux privés.
```

### 6.2 Choix technologiques

| Couche | Choix | Pourquoi | Écarté |
|---|---|---|---|
| App | **React 19 + TypeScript strict + Vite**, PWA (vite-plugin-pwa / Workbox) | SPA statique : idéale hors ligne et pour Capacitor | Next.js (rendu serveur inutile ; export statique imposé par Capacitor) |
| Natif | **Capacitor** (Android d'abord, iOS quand le compte Apple est financé) | même code ; GPS en arrière-plan (plugin gratuit, `foregroundServiceType="location"`), reconnaissance vocale native | Swift + Kotlin (2 apps), Tauri mobile (Mac requis), React Native (réécriture de l'UI, iOS bloqué), Electron (bureau seulement) |
| Logique métier | **`packages/core`** en TypeScript pur | testable à 100 %, réutilisable partout | — |
| Carte | **MapLibre GL JS** (build compatible CSP) + **PMTiles** du couloir des lignes, stocké dans l'OPFS et lu localement | gratuit, ODbL respectée (attribution visible), hors ligne fiable | Google Maps (payant), tuiles OSM publiques (préchargement interdit), cache de requêtes partielles dans le service worker (fragile) |
| Données | **Pipeline Rust** (`tools/pipeline`) | 915 Mo de GTFS + extrait OSM à traiter vite ; résultats déterministes et testés | — |
| Backend | **Supabase** : Postgres 17 + RLS, Auth, Storage, Edge Functions | maîtrisé, gratuit au pilote, UE | — |
| E-mails | SMTP gratuit (Brevo ou équivalent) sur un domaine avec SPF, DKIM, DMARC | le SMTP intégré de Supabase n'envoie qu'aux membres de l'équipe du projet | — |
| Hébergement | **Vercel Hobby** (app, paquets, tuiles) | gratuit, usage non commercial | Supabase Storage pour les tuiles (50 Mo max par fichier en gratuit) |
| Site vitrine | **Astro** statique (M10) | meilleur référencement naturel | — |
| Erreurs | **Sentry** UE, plan gratuit, sans replay, nettoyage `beforeSend` (coordonnées, jetons d'URL) | remontée automatique des plantages | — |
| Monorepo | **pnpm workspaces** ; Cargo pour le pipeline | simple, suffisant pour 2 utilisateurs | Turborepo (inutile à cette taille) |

Arborescence cible :

```
copibus/
  apps/app/            PWA (React)
  apps/site/           site vitrine Astro (M10)
  packages/core/       logique métier pure (guidage, horaires, calendrier)
  packages/ui/         design system (jetons, composants)
  packages/data/       schémas Zod, types générés Supabase, accès aux données
  tools/pipeline/      Rust : GTFS + OSM → paquets de ligne et tuiles
  supabase/            migrations SQL, politiques RLS, Edge Functions, tests pgTAP
  docs/                PRD, ADR, cadrage (exemples/ exclu de git)
```

### 6.3 Données TEC (faits vérifiés le 24/11/2026)

- GTFS statique : zip de 97 Mo, valable ~2,5 mois, tracés denses (point tous les 10-16 m), `block_id` sur 99,96 % des courses.
- SIRI Vehicle Monitoring : positions âgées de ~10 s, 100 % reliables aux courses GTFS après normalisation des identifiants (`:`/`-` → `_`). Pour M6.
- SIRI Situation Exchange : 2 293 perturbations, beaucoup « permanentes » (fin en 2200) : filtrage obligatoire. Pour M5.
- URL GTFS-RT du PRD v1 : obsolètes.
- Licence de réutilisation et quotas de Belgian Mobility : **à lire avant M1** (phase 0). Compte développeur gratuit créé par Thierry ; clé dans le coffre DevContext et les secrets Supabase.

**Paquet de ligne** (un par variante) : arrêts ordonnés, tracé simplifié (~2 m), distances cumulées, courses avec leurs `service_id` et le calendrier réel embarqué, date d'expiration, consignes de carrefour, version du GTFS. Objectif : < 150 Ko compressé.

**Consignes aux carrefours :** le pipeline cale le tracé sur le réseau OSM et ne génère une consigne qu'aux nœuds où se croisent au moins 3 routes, avec les sorties de rond-point. Si le calage échoue sur une portion, aucune consigne n'y est générée (arrêts et sortie de parcours seulement).

**Trajets haut-le-pied :** absents du GTFS. Enregistrés par un chauffeur (trace GPS), relus et validés par un référent, versionnés comme les notes terrain.

### 6.4 Guidage

1. `watchPosition` haute précision **sur le thread principal** (l'API n'existe pas dans un Web Worker), seulement pendant le guidage ; demande d'autorisation expliquée avant la première fois.
2. Calcul dans `packages/core` : projection sur le tracé, progression vers l'avant uniquement (fenêtre limitée), filtrage du bruit (précision annoncée, vitesse, cap), estimation par la vitesse quand le signal se dégrade. Un Web Worker n'est ajouté que si une mesure montre qu'il en faut un.
3. Prochain arrêt, distance le long du tracé, consigne au prochain carrefour.
4. Sortie de parcours, mode déviation, recalage.
5. Déclencheurs vocaux par distance ou temps, avec anti-répétition.
6. Wake Lock repris à chaque retour au premier plan ; GPS coupé à la fin du guidage ou après inactivité.

Limite assumée de la PWA sur iPhone : l'app doit rester au premier plan, écran allumé ; le GPS s'arrête si l'écran se verrouille. Le GPS en arrière-plan arrive avec l'app Android native.

### 6.5 Modèle de données (MVP)

Toutes les tables liées à une organisation portent `org_id` ; RLS partout ; identifiants internes UUID.

- **Identité :** `profiles` (prénom, préférences, assistante : nom, voix, débit, couleur), `organizations`, `depots`, `memberships` (user × org × rôle), `user_depots`, `invitations` (usage unique, expiration, e-mail lié).
- **Réseau :** `gtfs_versions`, `lines`, `line_variants`, `stops` (catalogue ; les paquets vivent en fichiers).
- **Service :** `duties`, `duty_items` (course identifiée de façon stable, ou trajet haut-le-pied).
- **Terrain :** `route_notes`, `route_note_reviews`, `deadhead_routes` (trajets haut-le-pied : trace, auteur, statut, validateur).
- **Support et qualité :** `support_messages`, `bug_reports`, `audit_events`, `rate_limits`.

### 6.6 Sécurité

- **Authentification :** OTP par e-mail (durée courte, tentatives limitées), TOTP obligatoire pour `platform_admin`, exigé côté base (`aal2`). Inscription publique désactivée. Invitations à usage unique, liées à l'e-mail, 48 h. Récupération de compte par l'admin seulement après vérification par un autre canal (téléphone ou en personne), avec révocation des sessions existantes.
- **Autorisation :** RLS sur 100 % des tables, testée par pgTAP (accès permis et accès refusé pour chaque politique). Jamais de `user_metadata` dans une politique (modifiable par l'utilisateur) : les rôles vivent dans `memberships`. Fonctions `SECURITY DEFINER` avec `search_path` fixé ; vues en `security_invoker` ; politiques Storage testées.
- **Secrets :** clé Belgian Mobility, jeton GitHub fine-grained limité à `issues:write` sur le dépôt, secret dédié pour les appels pg_cron → Edge Function (jamais la clé `service_role`) : uniquement côté serveur.
- **Contenu utilisateur et IA :** le texte libre des utilisateurs ne quitte pas Supabase. Les tickets GitHub ne contiennent qu'un identifiant et le contexte technique, portent l'étiquette `non-fiable`, et aucun agent (Claude, Timon) n'est déclenché automatiquement par un ticket. Quand Claude lit un message support, il le traite comme une donnée, jamais comme une instruction.
- **Clés IA des utilisateurs (M7b) :** modèle de stockage à arbitrer à ce moment-là (sur l'appareil ou côté serveur avec chiffrement par enveloppe, jamais renvoyées, logs nettoyés) ; liste blanche de modèles par tâche, quotas, coupe-circuit, révocation.
- **Edge Functions :** validation Zod, limitation de débit par utilisateur et par IP (compteur Postgres), réponses sans trace ni version ; les fonctions appelées par pg_cron écrivent leur résultat dans `data_source_status`.
- **Realtime (M6) :** canaux privés uniquement (accès public désactivé), RLS sur `realtime.messages`.
- **Photos :** bucket privé, URL signées courtes, métadonnées EXIF (dont la position) supprimées sur l'appareil **et** revérifiées côté serveur (attention au HEIC).
- **Client :** CSP stricte (MapLibre en build CSP, `worker-src blob:`), aucun script tiers hors Sentry, dépendances auditées en CI.
- **Positions :** la position du téléphone ne quitte pas l'appareil, sauf trace haut-le-pied que le chauffeur choisit explicitement de partager.
- **Audit :** journal des actions sensibles (invitation, rôle, accès admin, export, suppression, révocation).
- **Revue :** agent Opus avant chaque mise en ligne qui touche auth, RLS, Edge Functions, secrets, CI ou contenu externe transmis à une IA.

### 6.7 RGPD

- Le partage entre collègues sort du cadre purement privé : le RGPD s'applique. Politique de confidentialité et registre (Publiable) avant la première invitation ; durées de conservation définies.
- Minimisation : pas de position de téléphone envoyée, pas de micro sans signal visible, pas de photos de personnes.
- **OCR du planning (M3b) :** le traitement ne conserve que les services de l'utilisateur ; les noms des autres chauffeurs ne sont pas stockés. Les exemples réels du développement restent hors de git et ne servent qu'aux tests locaux. Vérifier l'absence de clause de confidentialité de l'employeur sur les plannings.
- Lien collègue → bus (M6) : c'est une localisation de salarié. Consentement explicite, révocable, indicateur visible quand le partage est actif.
- Sous-traitants : Supabase (UE), Vercel, Sentry (UE, DPA signé), fournisseur SMTP, GitHub (contexte technique seulement), Belgian Mobility (données publiques).

## 7. Performance et batterie (budgets vérifiés en CI ou sur appareil)

| Indicateur | Budget |
|---|---|
| JavaScript initial (compressé) | < 200 Ko ; carte chargée à la demande |
| Ouverture PWA installée, 4G lente | < 2 s jusqu'à l'écran utile |
| Délai position GPS → écran | < 500 ms |
| Paquet de ligne | < 150 Ko compressé |
| Tuiles du couloir des 26 lignes | à mesurer en phase 0 ; découpées si > 25 Mo par fichier |
| Données mobiles pendant 1 h de guidage | < 1 Mo (tout est préchargé) |
| Batterie et chaleur, 2 h de guidage en charge, au soleil, iPhone 14 | mesurées en phase 0 ; mode économie si l'écran baisse ou coupe |

## 8. Qualité et tests

- **`packages/core` :** Vitest, couverture ≥ 90 %, tests par propriétés (fast-check) sur le calage GPS, le calendrier et les heures après minuit.
- **Guidage :** rejeu de traces GPS réelles (lignes 65 et 63) et simulées, avec résultats attendus (arrêts annoncés, consignes, sorties de parcours, déviation).
- **Pipeline Rust :** `cargo test`, `clippy`, `fmt` ; tests « golden » sur des paquets de référence ; tests de dates (jours fériés, changement d'heure).
- **Base de données :** pgTAP pour chaque politique RLS, y compris `aal2` sur l'admin.
- **Bout en bout :** Playwright (géolocalisation simulée, parcours « moindre clic » chronométrés, hors ligne).
- **Accessibilité :** axe-core en CI + VoiceOver/TalkBack sur les écrans clés.
- **Performance :** Lighthouse CI avec budgets bloquants.
- **Portes avant chaque commit :** type-check, lint, tests, build. CI GitHub Actions obligatoire avant fusion. Revue de code automatique + revue sécurité Opus (section 6.6).
- **Appareils réels :** chaque module validé sur l'iPhone 14 et sur l'Android de la collègue.

## 9. Phase 0 — vérifications avant le code applicatif

Chaque point se conclut par un ADR écrit.

1. **Supabase :** environnement local (CLI + Docker) pour tout le développement ; projet cloud `copibus` déjà créé (D11), branché au moment du pilote avec un jeton dédié dans le coffre DevContext.
2. **E-mails :** en attente du nom de domaine (SMTP gratuit avec SPF, DKIM, DMARC le moment venu).
3. **Belgian Mobility :** licence de réutilisation, quotas, conditions du compte développeur.
4. **PWA sur iPhone 14 :** GPS au premier plan 30 min, Wake Lock en mode installé (repris après retour au premier plan), voix françaises disponibles, déblocage du son par un toucher, comportement avec l'interrupteur silencieux, une sortie Bluetooth et l'écran verrouillé ; batterie et chaleur en charge sur support.
5. **Traces GPS :** les tracés des lignes viennent déjà du GTFS TEC, la même source que l'app Letec et Google Maps (dont les conditions interdisent d'extraire les itinéraires). Le rejeu commence avec des traces simulées et bruitées. Des traces réelles (application GPX lancée avant le départ, sans toucher pendant la conduite) sont un plus pour valider le comportement dans la vallée, et elles restent **indispensables pour les trajets haut-le-pied**, absents de toutes les sources publiques.
6. **Pipeline sur la ligne 65 :** paquet de ligne, calendrier réel, calage OSM et consignes de carrefour, rejeu des traces.
7. **Tuiles :** taille du PMTiles du couloir, stockage OPFS, lecture hors ligne sur l'iPhone.
8. **OCR (avec les exemples du lundi 30 novembre 2026) :** Tesseract.js sur l'appareil vs service gratuit vs IA vision via clé utilisateur ; précision mesurée.
9. **Lignes au même numéro :** le numéro n'est pas unique en Wallonie (quatre « 65 », six « 10 »), et certaines lignes de la zone desservent aussi d'autres parties de la région. Inventaire complet des lignes de la zone pilote par `route_id` (parcours, variantes, destinations affichées), validé par Thierry avec sa connaissance du terrain ; l'app ne désigne jamais une ligne par son seul numéro.
10. **Temps réel aux arrêts :** SIRI Estimated Timetable (10 Mo par appel) filtré et mis en cache côté serveur, comparé à un retard calculé à partir des positions SIRI. Le flux GTFS-RT TripUpdates répondait 404 sans clé le 25/11/2026 : à revérifier avec la clé du portail. Il faut mesurer la fraîcheur des données et la part de courses suivies.
11. **Proactivité sur iPhone 14 :** Web Push envoyé à l'heure prévue (pg_cron + Edge Function), délai réel de réception, mode Concentration ; Raccourcis iOS (« En arrivant à… », CarPlay, Bluetooth) qui ouvrent l'app via `webapp://` : avec ou sans confirmation ?

12. **Navettes de remplacement SNCB :** lire le GTFS SNCB (accès anonyme vérifié le 25/11/2026). Il contient 75 lignes `BUS` (`route_type` 700), publiées environ 5 semaines à l'avance, mais leurs arrêts sont les gares elles-mêmes, sans position d'arrêt de bus ni tracé. À faire aussi : croiser avec les travaux Infrabel (jeu `langetermijnplanning-tcr-spoornetwerk`, sans information bus) et prototyper le routage **Valhalla** en mode « bus » (hauteur, largeur, longueur, poids ; licence MIT ; hors ligne possible) sur un extrait de la Wallonie. Écrire à la SNCB (gtfs@sncb.be) et à Keolis pour le format des feuilles de route : un envoi externe, qui demande l'accord de Thierry.

Recherche comparative (applis voyageurs, applis chauffeurs, faisabilité, navettes) : `docs/recherche/benchmark-2026-11-25.md`.

Retirés de la phase 0 (plus tard) : temps réel (M5/M6), passkeys, mot d'activation (avec l'app Android).

## 10. Feuille de route

1. **Phase 0** — vérifications ci-dessus ; création du dépôt privé et du projet Supabase dédié (avec l'accord de Thierry).
2. **Design** — 3 directions avec Claude Design, choix de Thierry, design system.
3. **MVP** — M0 → M1 → M3a → M2. Version pilote v0.1 sur les deux téléphones.
4. **M3b** Planning OCR.
5. **Android natif** (Capacitor, APK) puis **M7a** voix « Hé EVE » sur Android.
6. **M4** Véhicule (développé dans Timon, comparaison).
7. **M5** Alertes → **M5b** Déviations poids lourd → **M6** Équipe → **M7b** IA → **M8** Apprendre → **M9** Tachygraphe (validation juridique) → **M10** Site vitrine et nom définitif.
8. **iOS natif** quand le compte Apple Developer est financé.

## 11. Hors périmètre (rappel)

Remplacer les outils officiels de Keolis ou du TEC ; valider officiellement un échange de service ; contrôler le bus, la PFE ou le tachygraphe ; garantir la sûreté d'une déviation ; caméra ou micro en continu sans signal visible ; reconnaissance faciale ; publicité ; gamification en conduite.

## 12. Risques principaux

| Risque | Mesure |
|---|---|
| PWA iOS : GPS et voix limités au premier plan | assumé pour le pilote ; Android natif ensuite ; mesuré en phase 0 |
| Consignes de carrefour fausses | carrefours OSM réels seulement ; rejeu de traces réelles ; aucune consigne si le calage échoue |
| Débutant perdu entre dépôt et terminus | trajets haut-le-pied enregistrés et validés |
| Flux TEC modifié ou coupé | adaptateur isolé, version affichée, dernier paquet valide conservé |
| OCR imprécis | correction humaine obligatoire, méthode choisie après mesure |
| Quota Claude partagé (Claude Code + Timon) | un module à la fois |
| Confusion avec un outil officiel | nom et visuels sans marques TEC/Keolis, mention d'indépendance |
| Plan gratuit Supabase (pause après 7 jours, pas de SLA, quotas partagés par l'org) | usage quotidien, ping hebdomadaire, sauvegarde exportée, org à décider en phase 0 |
| Vercel Hobby et dons | aucun bouton de don hébergé sur Vercel sans confirmation écrite de Vercel |
| APK installé directement (Android) | vérification d'identité des développeurs Android étendue en 2027 ; compte « loisir » limité à 20 appareils : suffisant pour le pilote |
| Chaleur et batterie au pare-brise | mode économie, test de 2 h en phase 0, conseil de brancher le téléphone |

## 13. Questions encore ouvertes

- Nom de l'app (session dédiée : candidats, domaines, marques BOIP/EUIPO).
- Domaine d'envoi des e-mails (en attente du nom de l'app) et connexion provisoire des testeurs (Google ou e-mail + mot de passe).
- Déviations poids lourd (M5b) : Valhalla ou GraphHopper, hébergement gratuit possible ou non.
- Méthode OCR (après les exemples du 30 novembre 2026).
- Correspondance entre un service conducteur et les blocs TEC (`block_id`), et entre numéros de parc et références véhicule SIRI (ex. `V5220_3197`).
- Exploitant réel de chaque dépôt pilote (référentiel à construire et vérifier).
- Accès machine aux données de trafic SPW/PEREX (pour M5).
