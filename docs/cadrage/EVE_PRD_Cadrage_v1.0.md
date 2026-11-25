# EVE --- Product Requirements Document (PRD)

## Version 1.0 --- Cadrage fonctionnel, technique et étude des sources

**Date : 23 novembre 2026**\
**Périmètre initial : Belgique --- réseaux TEC, avec pilote autour de
Liège / Aywaille et extension Wallonie, Belgique et pays limitrophes.**\
**Statut : document de cadrage pour Claude Code / équipe de
développement.**

------------------------------------------------------------------------

## 0. Résumé exécutif

EVE est une copilote numérique destinée aux conducteurs professionnels
d'autobus et d'autocars. Elle regroupe dans une interface mobile simple
les services du chauffeur, les lignes et arrêts, la navigation GPS, les
perturbations, les connaissances de terrain partagées, les informations
véhicules, les contrôles de prise de service, les signalements
d'avaries, la documentation métier et une assistance vocale en français
de Belgique.

EVE doit fonctionner sans intégration privée Keolis ou TEC. Le produit
initial repose sur : - des jeux de données publics et leurs licences ; -
des plannings et documents importés par les chauffeurs (photos, PDF,
fichiers) ; - des données de lignes, arrêts, véhicules, dépôts et fiches
de parcours ajoutées par la communauté ; - des signalements géolocalisés
volontaires ; - des intégrations facultatives de calendrier et de
fournisseurs d'IA.

EVE ne doit jamais être présentée comme un dispositif officiel de
sécurité, un outil de conformité tachygraphique certifié, un système de
dispatching du transporteur ou un GPS poids-lourds/autobus garantissant
à lui seul la sécurité d'un itinéraire.

**Principe directeur :** les données critiques sont déterministes,
sourcées, datées et vérifiables. L'IA explique et orchestre les
fonctions, mais ne fabrique jamais des horaires, des restrictions
routières, des obligations légales, des affectations ou des consignes de
sécurité.

## 1. Vision et objectifs

### 1.1 Vision

Faire d'EVE un assistant métier qui accompagne le conducteur avant,
pendant et après son service, sans le distraire : - avant le service :
préparer l'horaire, le départ domicile-dépôt, le véhicule, la météo et
les particularités du parcours ; - à la prise du véhicule : effectuer
une check-list, documenter les dommages et signaler les avaries ; -
pendant le service : suivre la bonne ligne en temps réel, annoncer les
arrêts et avertir assez tôt des difficultés ; - entre collègues :
partager les incidents et visualiser, si les données et consentements le
permettent, les véhicules utiles aux correspondances ; - après le
service : clôturer les contrôles, transmettre les signalements et
conserver un historique utile ; - en apprentissage : retrouver les
procédures PFE, les particularités des bus et les connaissances du
réseau.

### 1.2 Objectifs mesurables du pilote

1.  Un conducteur peut créer son profil et renseigner entreprise, dépôt,
    préférences et véhicules.
2.  Un conducteur peut importer une photo de son planning mensuel,
    corriger les résultats OCR et retrouver ses services.
3.  Un conducteur peut préparer un service et visualiser ligne, sens,
    arrêts, horaires et tracé.
4.  La carte suit la position GPS du téléphone et indique clairement la
    progression sur le bon parcours.
5.  Les alertes sont filtrées par correspondance géographique avec le
    trajet et affichées suffisamment tôt.
6.  Le conducteur peut compléter une check-list véhicule et joindre des
    photos horodatées.
7.  Un signalement peut être préparé comme rapport et envoyé par e-mail
    après confirmation explicite.
8.  L'application fonctionne avec une connexion mobile limitée et gère
    une perte temporaire de réseau.
9.  Le mode conduite est lisible, vocal, sobre et limite fortement les
    manipulations.
10. L'application est accessible via une URL/PWA, sans frais de
    publication iOS ou Google Play au lancement.

### 1.3 Non-objectifs de la première version

-   Remplacer les logiciels officiels de planning Keolis/TEC.
-   Modifier directement les plannings ou valider des échanges de
    services auprès de l'employeur.
-   Contrôler ou commander le bus, la PFE, les portes, les freins, le
    chauffage ou le tachygraphe.
-   Garantir qu'une déviation proposée est sûre sans validation humaine
    et données routières vérifiées.
-   Fournir une détection d'accident par caméra en continu.
-   Enregistrer le microphone en permanence en arrière-plan.
-   Remplacer le tachygraphe ou certifier la conformité légale des temps
    de conduite et de repos.

## 2. Utilisateurs, organisations et périmètre géographique

### 2.1 Profils utilisateurs

-   Conducteur débutant / en reprise : guidage pédagogique, gros
    caractères, fiches de rappel.
-   Conducteur expérimenté : raccourcis, alertes configurables,
    contribution aux fiches de ligne.
-   Conducteur d'autobus régulier : services, arrêts, lignes,
    correspondances.
-   Conducteur de service express / longue distance : informations de
    service et module tachygraphe lorsque le règlement s'applique.
-   Conducteur de navette ferroviaire / service spécial : service
    spécifique, arrêts ou points de prise en charge, classification
    réglementaire à confirmer.
-   Référent communautaire : vérifie les fiches de parcours et
    signalements.
-   Administrateur d'organisation : gère les dépôts, véhicules,
    utilisateurs et documents de son organisation.
-   Administrateur plateforme : modération, sécurité, opérateurs,
    connecteurs, coûts et abus.

### 2.2 Multi-entreprises et modèle de données organisationnel

EVE doit distinguer clairement : - l'opérateur public / autorité de
transport (ex. OTW/TEC) ; - l'entreprise privée qui exploite une ou
plusieurs prestations (ex. Keolis ou autre sous-traitant) ; - la filiale
/ entité juridique ; - le dépôt / garage / site opérationnel ; - le
contrat ou lot d'exploitation et sa période de validité ; - le réseau,
la ligne publique, la course et le service conducteur ; - le véhicule
physique et son numéro de parc.

Ne pas déduire qu'une société répertoriée comme autocariste exploite
nécessairement une ligne TEC. Les contrats, lots, dépôts et dates de
validité doivent être vérifiés avant publication.

### 2.3 Première couverture

-   Priorité pilote : province de Liège, région Aywaille/Sprimont,
    Liège-Verviers.
-   Extension : Namur-Luxembourg et reste de la Wallonie.
-   Ensuite : Belgique (TEC, De Lijn, STIB-MIVB, SNCB pour
    correspondances) et pays limitrophes.
-   Les lignes transfrontalières vers l'Allemagne et les autres pays
    doivent appliquer les règles locales pertinentes, en particulier
    pour les services internationaux et le tachygraphe.

### 2.4 Répertoire des entreprises et dépôts

Utiliser le localisateur FBAA comme source de départ pour les
entreprises de bus et autocars. Il n'est ni un registre exhaustif de
tous les sous-traitants TEC, ni une preuve d'attribution d'un marché
public. Exemples visibles dans le répertoire FBAA pour la province de
Liège : Compagnie des Autobus Liégeois à Sprimont, Autocars Jacky à
Aywaille/Sougné-Remouchamps, Autobus F. Gohy à Theux, Eurobussing
Wallonie à Flémalle, Garage du Perron à Verviers/Petit-Rechain, SADAR à
Kelmis, Satracom à Waimes, Transcar à Seraing, Voyages Léonard à
Blegny/Barchon, Z-Cars à Eupen. Pour Namur : Bus et Cars Roquet, Deblire
Autocars, Latour Autobus et d'autres sociétés référencées. Ces données
sont des pistes de départ : l'administrateur doit confirmer la
dénomination, le statut, le dépôt réel, le lien contractuel TEC et la
période de validité. Ne pas publier de liste de « dépôts TEC »
construite par supposition.

## 3. Fonctionnalités et exigences détaillées

### 3.1 Profil conducteur et préférences

Champs : - identité d'affichage et coordonnées vérifiées ; - entreprise,
filiale, dépôt, rôle ; - langue (français Belgique par défaut ;
néerlandais, allemand et autres langues ensuite) ; - préférences vocales
: voix, débit, volume, prononciation, niveau de bavardage ; -
préférences d'affichage : taille texte, accent color, contraste, thème
sombre par défaut ; - paramètres de données : mode économe,
téléchargement Wi-Fi seulement, qualité carte ; - autorisations de
position, partage entre collègues et durée de conservation ; -
calendrier(s) connectés ; - préférences de notification ; - véhicules et
types de service habituels.

Le profil ne doit jamais demander un mot de passe tiers ou une clé API
personnelle en clair. Les secrets d'intégration sont stockés dans un
coffre chiffré ou dans les mécanismes OAuth sécurisés.

### 3.2 Planning mensuel et OCR

Sources possibles : photo du tableau horaire/classeur, PDF, image,
XLSX/CSV, calendrier et éventuellement export de l'application employeur
si autorisé. Parcours : 1. importer document ; 2. améliorer l'image
(recadrage, rotation, perspective, contraste) ; 3. OCR ; 4. reconnaître
tableaux, codes de services, dates, heures, lieux, lignes, courses et
annotations ; 5. afficher une prévisualisation avec confiance par champ
; 6. demander confirmation des champs incertains ; 7. enregistrer le
planning versionné ; 8. comparer le nouveau planning aux versions
antérieures et signaler les changements. Chaque modification manuelle
doit être historisée. Les documents sources restent associés au planning
selon une politique de conservation choisie. L'OCR n'est jamais
considéré comme exact sans validation humaine. L'application doit
détecter les ambiguïtés (6/8, 0/O, heures, codes de service).

### 3.3 Gestion des échanges de services

-   Recherche de collègues dont les horaires pourraient être
    compatibles, uniquement dans le groupe/organisation autorisé.
-   Affichage des conflits horaires, temps de repos et contraintes
    configurées.
-   Proposition de demande d'échange, acceptation explicite des deux
    parties.
-   Statut « à soumettre à l'employeur » et « autorisé par l'employeur
    ».
-   Aucun échange ne devient officiel sans validation du système ou du
    responsable compétent.
-   Ne pas exposer le planning complet d'un collègue sans base légale et
    autorisation appropriée.

### 3.4 Préparation du départ domicile-dépôt et météo

Calculer une heure de départ recommandée en séparant : - temps de trajet
routier estimé vers le dépôt ; - marge de circulation ; - heure à
laquelle le conducteur doit être présent ; - temps de prise de service /
remise de clés / formalités ; - inspection avant départ ; - préparation
du véhicule ; - marge liée à la météo. La préparation hivernale doit
être paramétrable par véhicule et dépôt. Valeur initiale indicative : 15
à 20 minutes pour dégivrage, déneigement et montée en température, à
confirmer selon véhicule, conditions et consignes employeur. Ne pas
considérer cette valeur comme une obligation réglementaire ni déclencher
automatiquement le chauffage ou le moteur. Facteurs météo : température,
précipitations, neige, gel, verglas probable, vent, brouillard, humidité
et heure de lever du soleil. Une prévision météo est une indication, pas
un diagnostic de l'état réel du véhicule. Exemple de calcul : heure de
départ = heure de présence requise - trajet estimé - marge trajet.
L'heure de présence requise inclut les étapes de préparation définies
par l'organisation et le conducteur. Alertes : la veille, au moment
choisi, puis seulement si le trafic ou la météo modifie réellement la
recommandation.

### 3.5 Check-list de prise du véhicule

Créer une check-list configurable par organisation et type de véhicule.
Liste initiale indicative : - pneus et état visible, dommages apparents
; - éclairage, clignotants, feux stop, feux de détresse ; - rétroviseurs
et caméras ; - pare-brise, vitres, essuie-glaces et lave-glace ; -
portes, rampes et dispositifs d'accès PMR ; - avertisseur sonore ; -
tableau de bord, voyants et messages ; - fuites visibles, dommages
carrosserie ; - équipements de sécurité et issues de secours selon
procédure employeur ; - propreté et visibilité ; - documents et
équipements requis ; - anomalies ressenties ou signalées par le service
précédent. Les items doivent pouvoir être marqués « conforme », «
anomalie », « non applicable », « à vérifier ». La liste officielle de
l'employeur prévaut. Les photos peuvent être jointes à un item ou à une
avarie, avec date, heure, véhicule et description. Éviter de
photographier passagers, visages, plaques privées ou documents
personnels. Prévoir un rapport d'avarie avec priorité, catégorie,
description, photos, kilométrage si saisi, lieu, horodatage, statut et
historique. Envoi par e-mail : préparer un message et pièces jointes au
service désigné ; le conducteur vérifie et confirme l'envoi. Conserver
une copie du rapport et du résultat d'envoi. Ne pas envoyer
automatiquement à un destinataire non vérifié. Mode hors ligne :
enregistrer localement de façon chiffrée, synchroniser quand le réseau
revient, éviter les doublons.

### 3.6 Base de données des véhicules

Fiche véhicule : - numéro de parc (ex. 404, 405, 524) ; - opérateur,
dépôt, statut ; - marque, modèle, année et motorisation ; - hauteur,
largeur, longueur, masse, PTAC/masse autorisée et autres limites connues
; - nombre d'essieux, empattement, porte-à-faux, rayon de braquage si
disponible ; - type de boîte, transmission, carburant/énergie ; -
particularités de conduite et commandes ; - documentation et photos
annotées ; - historique d'avaries et contrôles accessibles aux personnes
autorisées. Le numéro de parc n'est pas toujours unique entre
entreprises : identifiant interne + organisation obligatoires. Un
véhicule peut changer de dépôt ou d'affectation ; conserver un
historique daté.

### 3.7 Fiches de ligne, services et classeurs papier

Importer manuellement les classeurs ou photos des documents : - ligne,
variante, sens, destination ; - séquence d'arrêts et coordonnées ; -
points de correspondance entre lignes ; - horaires théoriques et temps
de battement ; - tracé réel validé ; - points de prise en charge et
terminus ; - notes d'exploitation ; - points difficiles et restrictions
vérifiées ; - photos et commentaires ; - date de vérification et auteur.
La connaissance terrain doit distinguer : - fait cartographique ; -
règle officielle ; - observation d'un chauffeur ; - conseil personnel
; - signalement temporaire. Chaque élément a un niveau de confiance, une
date de dernière validation, une source et un statut (proposé, vérifié,
expiré, contesté). Une note critique doit être affichée avant l'approche
de la zone, pas au dernier moment. Le déclenchement se fait par
distance/temps d'approche et position sur le parcours, avec seuil
configurable (par défaut viser 60 à 120 secondes avant la zone lorsque
la vitesse le permet). Ne pas annoncer des alertes qui saturent le
conducteur.

### 3.8 Navigation GPS et carte temps réel

Exigences : - carte fluide avec position du téléphone ; - suivi du
parcours sélectionné et comparaison avec le tracé attendu ; - sens de
circulation, nom de ligne et destination ; - arrêts positionnés à leurs
coordonnées réelles et distingués par côté/plateforme lorsque les
données le permettent ; - prochain arrêt, distance et estimation
d'arrivée ; - recalage GPS (map matching) et détection de sortie de
parcours ; - position des véhicules TEC disponibles publiquement ; -
position de collègues uniquement si leur partage volontaire est activé
et si leur identité/mission est correctement associée ; - affichage de
fraîcheur des données et indicateur « position indisponible / retardée »
; - mode paysage et support de fixation ; - mode hors ligne pour les
données de service, arrêts, géométrie et fiches téléchargées à l'avance.
Ne jamais afficher un bus comme étant un collègue identifié si le flux
ne permet que d'identifier un véhicule/cours public. Les positions TEC
peuvent être retardées ou absentes si la PFE est défaillante ou le bus
non détecté. Le GPS du téléphone peut être précis, mais la précision
varie selon appareil, tunnel, canyon urbain et météo. Afficher un état
de confiance plutôt que prétendre à une précision parfaite.

### 3.9 Alertes de circulation et pertinence sur l'itinéraire

Sources : - alertes TEC / SIRI ; - trafic et travaux
SPW/PEREX/Trafiroutes ; - signalements EVE ; - données cartographiques
et restrictions ; - sources complémentaires après vérification des
licences. Pipeline : 1. normaliser chaque événement ; 2. géocoder sa
géométrie ou sa position ; 3. comparer avec la géométrie de la ligne et
le sens de circulation ; 4. calculer distance latérale, distance le long
du parcours, heure de validité et impact probable ; 5. vérifier si
l'événement est sur la route ou à proximité pertinente ; 6. classer par
gravité, confiance et urgence ; 7. prévenir suffisamment tôt. L'alerte
doit être visualisée par une portion colorée du trajet et un panneau
synthétique. Ne jamais utiliser la couleur seule : icône, libellé et
annonce vocale doivent compléter. Exemple : « Travaux dans 900 mètres,
sur le parcours, voie rétrécie. Information SPW publiée à 14:10. »
Distinguer événement officiel, événement signalé par un collègue, et
estimation calculée. Afficher source et âge de l'information.

### 3.10 Déviation et contraintes de véhicule --- fonctionnalité à haut risque

EVE peut calculer des itinéraires candidats adaptés aux dimensions
renseignées du véhicule, mais un moteur open source ne garantit pas la
sûreté de la route. La qualité OSM est inégale ; les restrictions de
tonnage, largeur, hauteur, accès riverains, sens, travaux temporaires,
virages, rayon de braquage, pente et giration peuvent manquer ou être
obsolètes. Règles impératives : - Ne jamais présenter un itinéraire
alternatif comme « validé/sûr » uniquement parce qu'un routeur le
calcule. - Un itinéraire candidat est « à vérifier » jusqu'à
confirmation par une source officielle, un référent exploitation ou une
procédure validée. - Les dimensions et limites doivent provenir de la
fiche exacte du véhicule. - Vérifier hauteur, largeur, longueur,
masse/charge par essieu si disponible, restrictions, sens uniques,
interdictions bus/poids lourds, ponts, tunnels, travaux et accès. - Si
une donnée critique manque : bloquer la recommandation automatique et
conseiller de suivre la procédure d'exploitation / contacter le
dispatch. - Ne jamais inciter à faire demi-tour, reculer ou emprunter
une voie dangereuse. - En conduite, ne pas afficher de longues
instructions techniques ; proposer un arrêt sécurisé pour examiner
l'alternative. - Historiser la validation, l'auteur, la date et la
période de validité. Le moteur Valhalla propose un profil bus avec
paramètres hauteur, largeur, longueur et poids. Cela constitue une aide
de calcul, pas une certification de passage.

### 3.11 Réseau collaboratif chauffeurs

-   signalement vocal ou formulaire à l'arrêt ;
-   catégorie, description, position, ligne, sens, véhicule facultatif,
    photo facultative ;
-   diffusion uniquement aux chauffeurs concernés par le segment et la
    période ;
-   confirmations indépendantes ;
-   expiration automatique ;
-   contestation et modération ;
-   score de fiabilité basé sur historique, confirmations et source,
    sans classement humiliant des conducteurs ;
-   mode « ne pas déranger » et limites de fréquence. Partage de
    position : activé explicitement pour une période de service, visible
    aux groupes autorisés, avec bouton d'arrêt et durée de rétention
    courte. Pas de suivi domicile-travail par défaut. Pas de
    surveillance cachée.

### 3.12 Assistant vocal et navigation de l'application

L'utilisateur doit pouvoir parler naturellement en français de Belgique,
avec expressions familières et vocabulaire transport. Exemples : - «
EVE, ouvre la carte. » - « Montre-moi la circulation sur mon trajet. » -
« Quel est le prochain arrêt ? » - « Est-ce qu'on passe près de la gare
de X ? » - « Signale un accident ici. » - « Explique-moi ce bouton sur
le bus 524. » - « Combien de temps avant mon prochain service ? » - «
Prépare un rapport pour la mécanique. » - « Ouvre ma check-list. » EVE
doit pouvoir ouvrir les vues, onglets et fiches, mais les actions
sensibles (envoyer, partager, échanger un service, publier une alerte
critique) demandent confirmation. Ton : professionnel, chaleureux, un
peu d'humour optionnel, jamais sarcastique dans une situation d'urgence.
Mode vocal : - bouton d'activation prioritaire ; - mot d'activation
uniquement si compatible avec les règles des OS et l'app au premier plan
/ session autorisée ; - réponses courtes en conduite ; - possibilité de
répéter ou ralentir ; - dictionnaire de prononciation (TEC, PFE, noms de
communes, noms d'arrêts, lignes E20/E69, acronymes) ; - test de
compréhension et de voix pendant l'onboarding. Pas de promesse d'écoute
permanente garantie : iOS et Android limitent les services microphone en
arrière-plan. Le microphone ne doit pas être activé sans signal visible
et consentement.

### 3.13 Passagers et lieux à proximité

L'assistant peut répondre à une question de passager sur un lieu ou une
destination : - vérifier si le parcours passe près du lieu demandé ; -
calculer une proximité à pied/à vol d'oiseau distincte ; - préciser si
le bus s'arrête réellement à un arrêt proche ; - ne pas affirmer qu'un
arrêt est desservi si la course/variante ne le prévoit pas. Exemple de
réponse : « Nous passons à environ 300 mètres de la gare, mais le bus ne
dessert pas directement l'entrée. Le prochain arrêt desservi est X. » La
réponse doit distinguer « près de », « arrêt desservi » et «
correspondance possible ».

### 3.14 Documentation métier et aide PFE

-   bibliothèque de documents par entreprise, dépôt, véhicule, ligne et
    catégorie ;
-   import PDF/image, OCR, recherche plein texte et recherche sémantique
    ;
-   guides pas à pas, captures d'écran annotées, vidéos autorisées ;
-   fiches PFE, billettique, afficheurs, radio, équipements et
    procédures ;
-   réponse IA citant le document, la page et la version ;
-   signaler « information introuvable » plutôt que créer une procédure.
    Les documents employeur peuvent être confidentiels : accès par
    organisation, droits et journal d'accès.

### 3.15 Tachygraphe et temps de conduite

Module pédagogique et de suivi indicatif, jamais substitut au
tachygraphe homologué ni à l'interprétation officielle. - profil de
service (régulier, spécial régulier, occasionnel, international,
navette, autre) ; - distance et classification de la ligne, notamment
seuil de 50 km ; - saisie/import des périodes de conduite, autre
travail, disponibilité, pauses et repos ; - rappels indicatifs et
affichage des règles pertinentes ; - explication des pictogrammes et
séquences du tachygraphe ; - historique et export personnel ; -
avertissement lorsque des données sont manquantes. Les règles
européennes diffèrent selon le type de service et des exemptions. Pour
les services couverts par le règlement 561/2006, les règles générales
comprennent notamment une pause de 45 minutes au plus tard après 4 h 30
de conduite (avec fractionnement permis selon conditions), mais
l'application doit calculer uniquement après qualification du service et
du droit applicable. Le conducteur reste tenu de respecter le
tachygraphe et les consignes officielles. Ne pas interpréter
automatiquement une navette SNCB comme exemptée ou soumise sans examiner
son contrat, sa nature, son itinéraire et les textes applicables.
Prévoir validation par un expert social transport / responsable
conformité avant activation en production.

### 3.16 E-mails et calendriers

-   Google Calendar / Gmail via OAuth et API officielle, consentement
    utilisateur.
-   Outlook / Hotmail / Microsoft 365 via Microsoft Graph et OAuth.
-   Proton : prévoir import ICS lorsque possible ; ne pas promettre une
    API Calendar publique équivalente sans vérification de la
    documentation et des limites.
-   autres calendriers via ICS/WebCal lorsque disponible.
-   e-mails d'avarie : création d'un brouillon ou envoi après
    confirmation ; ne jamais demander mot de passe mail. Les connecteurs
    doivent être facultatifs, révocables et limités aux autorisations
    nécessaires.

### 3.17 IA personnelle / BYOK

L'IA ne doit pas être obligatoire pour les fonctions de base. - Mode
sans IA : navigation, données, alertes, check-lists, planning validé,
fiches et règles déterministes. - Mode IA personnelle : l'utilisateur
ajoute une clé API personnelle ou connecte un compte par OAuth lorsque
le fournisseur le permet. - Les clés API sont chiffrées côté serveur,
jamais exposées au navigateur ni stockées en clair. - Les abonnements
ChatGPT/Claude/Gemini grand public ne donnent pas automatiquement droit
à l'utilisation API. Une API est généralement facturée séparément, sauf
mécanisme OAuth/partenaire officiellement supporté. - EVE ne doit pas
demander le mot de passe ChatGPT, Claude ou Google. - Limiter les
modèles aux actions permises et appliquer des garde-fous côté serveur. -
Afficher les coûts estimés et consommation par fournisseur ; quotas et
coupe-circuit. - Chaque organisation peut désactiver l'IA ou imposer des
modèles approuvés. - Les appels IA ne doivent pas être utilisés pour les
décisions de sécurité routière, le calcul légal du tachygraphe ou les
faits opérationnels déterministes.

## 4. Interface et accessibilité

### 4.1 Principes UX

-   Mode sombre par défaut, conçu pour rester lisible en plein soleil.
-   Accent personnalisable (vert, bleu, etc.) uniquement si le contraste
    calculé reste conforme.
-   Typographie très lisible, grands éléments tactiles et hiérarchie
    visuelle claire.
-   Trois contextes : Préparation, Conduite, Pause.
-   Le mode conduite ne comporte ni clavier, ni formulaires longs, ni
    navigation complexe.
-   Le conducteur ne doit jamais devoir parcourir un menu profond pour
    une fonction essentielle.
-   L'assistant vocal peut ouvrir les écrans, mais le conducteur peut
    toujours revenir à un écran d'accueil simple.
-   Onboarding interactif, tutoriel réutilisable et mode démo.
-   Prévoir utilisateurs âgés, lunettes, vision réduite, daltonisme et
    faible aisance numérique.

### 4.2 WCAG 2.2 AA

Cibles minimales : - contraste texte normal : 4,5:1 ; - grand texte :
3:1 ; - composants et éléments graphiques nécessaires : contraste non
textuel conforme ; - ne jamais utiliser la couleur comme seul indicateur
; - navigation clavier et lecteur d'écran pour la partie web ; - tailles
de cibles tactiles confortables ; - zoom sans perte de contenu ; -
mouvement réduit. Le thème accent ne peut être validé que par tests
automatiques et tests utilisateurs. WCAG est une norme web
d'accessibilité ; l'application mobile doit aussi suivre les
recommandations natives iOS/Android.

### 4.3 Maquettes indispensables

Avant développement fonctionnel : 1. Accueil / service du jour. 2. Mode
conduite avec prochain arrêt et carte. 3. Alerte travaux avec portion
surlignée. 4. Fiche véhicule et check-list. 5. Rapport d'avarie et
photos. 6. Planning mensuel OCR avec correction. 7. Fiche ligne avec
notes de difficulté. 8. Réseau collègues / alerte. 9. Assistant vocal et
commandes. 10. Onboarding simple.

## 5. Sources de données et API --- inventaire initial

  -------------------------------------------------------------------------
  Source            Données / usage   Gratuité et        Décision
                                      limites            
  ----------------- ----------------- ------------------ ------------------
  Belgian Mobility  GTFS statique,    Données de base    Intégration
  Open Data         GTFS-RT, SIRI 2.1 gratuites sous     prioritaire
                    TEC : horaires    licence ouverte ;  
                    estimés, alertes, accès anonyme pour 
                    positions         exploration ;      
                    véhicules         compte développeur 
                                      gratuit + clé pour 
                                      interrogations de  
                                      production ;       
                                      premium pour       
                                      historique,        
                                      capacités          
                                      supérieures        

  TEC / LETEC       Lignes, arrêts,   Flux publics       Source principale
                    courses, temps    agrégés via BMO ;  
                    réel              API interne et     
                                      identité du        
                                      chauffeur non      
                                      garanties          

  De Lijn / STIB /  Données pour      Couverture et flux Phase ultérieure
  SNCB              extension et      variables par      
                    correspondances   opérateur          

  SPW / PEREX /     Trafic,           Site public et     Étude technique et
  Trafiroutes       incidents,        informations temps demande d'accès
                    travaux, météo    réel ; API         
                    routière et       publique stable et 
                    caméras sur le    conditions d'usage 
                    réseau géré       à confirmer ;      
                                      contact SPW/PEREX  
                                      nécessaire pour    
                                      flux machine       

  OpenStreetMap     Réseau routier,   Données ODbL       Intégration
                    géométrie,        gratuites avec     prioritaire
                    restrictions et   attribution ;      
                    points d'intérêt  complétude         
                                      variable           

  MapLibre          Affichage         Bibliothèque open  Intégration
                    cartographique    source ; ne        prioritaire
                                      fournit pas les    
                                      tuiles ni le       
                                      trafic             

  Valhalla          Routage, profil   Open source,       Prototype de
                    bus et paramètres auto-hébergement   routage
                    dimensions        possible ;         
                                      restrictions       
                                      cartographiques    
                                      incomplètes ; pas  
                                      de trafic temps    
                                      réel natif garanti 

  GraphHopper       Routage et        Moteur open source Alternative
                    profils           et offre hébergée  
                    personnalisés     avec quotas/prix à 
                                      vérifier           

  Open-Meteo        Prévisions météo  Gratuit pour usage Prototype puis
                    et données        non commercial     budget/licence ou
                    horaires          sous conditions ;  auto-hébergement
                                      usage commercial   
                                      nécessite          
                                      licence/API        
                                      payante ; pas de   
                                      SLA sur offre      
                                      gratuite           

  Google Maps       Trafic et calcul  Facturation à la   Option premium,
  Routes            de route          requête, billing   pas base gratuite
                                      obligatoire ;      
                                      trafic temps réel  
                                      dans offres        
                                      supérieures        

  FBAA              Répertoire des    Consultation       Référentiel
                    entreprises de    publique ; pas     initial à valider
                    bus et autocars   preuve             
                                      d'attribution d'un 
                                      marché TEC         

  Documents         Planning,         Apport             Source centrale
  chauffeurs        classeurs, fiches communautaire ;    EVE
                    ligne, véhicules, droits de          
                    procédures        diffusion à        
                                      contrôler          

  EVE Community     Incidents,        Données            Source
                    travaux           volontaires ;      complémentaire
                    temporaires,      qualité à modérer  
                    difficultés                          
  -------------------------------------------------------------------------

### 5.1 Belgian Mobility Open Data : endpoints à prototyper

Documentation : - https://data.belgianmobility.io/en/data.html -
https://data.belgianmobility.io/en/faq.html -
https://data.belgianmobility.io/en/knowledge-base.html

Endpoints documentés : - GTFS TEC statique :
`https://opendata-discovery-gtfs-static.api.production.belgianmobility.io/api/gtfs/feed/tec/static` -
GTFS-RT trip updates :
`https://opendata-discovery-gtfs-realtime.api.production.belgianmobility.io/api/gtfs-rt/tec/TripUpdates.pbf` -
GTFS-RT service alerts :
`https://opendata-discovery-gtfs-realtime.api.production.belgianmobility.io/api/gtfs-rt/tec/ServiceAlerts.pbf` -
SIRI estimated timetable :
`https://api-management-discovery-production.azure-api.net/api/siri/feed/tec/estimated-timetable?format=json` -
SIRI situation exchange :
`https://api-management-discovery-production.azure-api.net/api/siri/feed/tec/situation-exchange?format=json` -
SIRI vehicle monitoring :
`https://api-management-discovery-production.azure-api.net/api/siri/feed/tec/vehicle-monitoring?format=json`

Les flux SIRI sont annoncés comme actualisés environ toutes les 30
secondes. Le portail indique que les données de base sont gratuites et
que l'accès anonyme est destiné à l'exploration ; un compte gratuit et
une clé API sont requis pour le polling en production. Les limites
exactes doivent être vérifiées auprès du portail avant dimensionnement.
Clé dans l'en-tête `bmc-partner-key` selon sa FAQ. Ne jamais intégrer la
clé dans l'application mobile.

### 5.2 Trafic SPW

Trafiroutes expose publiquement une carte et des listes de travaux,
incidents et impacts. Le centre PEREX agrège des capteurs, caméras,
stations météo, détecteurs de brouillard et informations de partenaires.
Contact public indiqué par la Wallonie : Centre PEREX,
permanence.perex@spw.wallonie.be, 0800/48.400. À faire : demander un
accès documenté aux données machine (API, WFS/WMS, GeoJSON, flux,
fréquence, licence, limites de redistribution). Tant qu'il n'est pas
confirmé, ne pas promettre un flux API ouvert. Le portail wallon indique
une modernisation de Trafiroutes attendue à l'automne 2026 ; vérifier
l'état réel au moment de l'intégration.

### 5.3 Positions de bus TEC et collègues

Le portail BMO annonce un flux SIRI Vehicle Monitoring TEC. Cela peut
fournir des positions de véhicules, mais ne prouve pas qu'EVE peut
retrouver le chauffeur, son planning ou le numéro de parc de façon
fiable. Le site tiers Letec Finder indique utiliser une position issue
de la PFE et une API TEC, avec actualisation très fréquente. C'est un
indice technique intéressant, pas une autorisation de réutilisation.
Contacter l'éditeur et le TEC avant toute dépendance ou redistribution.
Pour le pilote, afficher les véhicules publics seulement si le flux, son
identifiant et sa fraîcheur sont fiables. L'association avec le collègue
doit reposer sur une correspondance vérifiée entre course/vehicle ID et
service, ou sur un partage volontaire EVE distinct.

## 6. Architecture technique proposée

### 6.1 Architecture de lancement

Ne pas imposer Flutter + Next.js en double dès le jour 1. Pour un
développeur non professionnel et un lancement à coût minimal : - PWA
responsive en Next.js/TypeScript comme première interface ; - backend
Supabase (PostgreSQL, Auth, Storage, Realtime, Edge Functions si adapté)
; - MapLibre GL JS pour la carte ; - service worker pour cache de
l'application et données préchargées ; - API backend pour proxy des flux
TEC et autres fournisseurs ; - schéma de données multi-tenant avec Row
Level Security. L'architecture doit isoler les adaptateurs de données et
permettre plus tard une application native (Capacitor ou Flutter/React
Native après étude), sans réécrire les règles métier. Attention : PWA ne
garantit pas le suivi GPS en arrière-plan fiable et continu,
particulièrement sur iOS. Pour une navigation professionnelle réellement
continue, une app native sera probablement nécessaire à terme.

### 6.2 Hébergement et scalabilité

-   Vercel Hobby : gratuit mais destiné aux projets personnels/non
    commerciaux ; ne pas le considérer comme une garantie de production
    pour un service multi-utilisateurs public. Vercel Pro annoncé à 20
    USD/mois, hors dépassements et taxes.
-   Supabase Free : 0 USD, 2 projets actifs, 500 MB base, 5 GB egress, 1
    GB stockage, 50 000 MAU selon la page tarifaire consultée ; projets
    gratuits en pause après une semaine d'inactivité. Suffisant pour
    prototype, pas une garantie SLA.
-   Supabase Pro : à partir de 25 USD/mois par projet selon page
    tarifaire consultée ; inclut davantage de stockage, egress et
    sauvegardes.
-   Pour une production fiable : budgets alertes, sauvegardes,
    monitoring, tests de restauration, limitation de débit, plan de
    reprise, export régulier et éventuellement hébergement UE.
-   Ne jamais considérer le free tier comme un SLA de sécurité ou de
    disponibilité.

### 6.3 Sécurité

-   RLS sur toutes les tables multi-tenant.
-   RBAC : conducteur, référent, responsable dépôt, admin organisation,
    admin plateforme.
-   Isolation stricte entre entreprises.
-   Secrets API côté serveur, chiffrés.
-   OAuth avec scopes minimaux.
-   MFA pour administrateurs.
-   journal d'audit pour changements de service, signalements, accès
    documents et partage position.
-   rate limiting, protection anti-spam, validation fichiers, antivirus
    si possible.
-   chiffrement en transit et au repos.
-   sauvegardes et tests de restauration.
-   politique de conservation et suppression.
-   aucune clé API dans le code frontend ou dépôt Git.
-   revue de sécurité et test d'intrusion avant ouverture élargie.
-   prévoir procédure de violation de données et contact DPO.

### 6.4 Modèle de données initial

Tables/entités principales : - organizations, legal_entities, depots,
organization_members, roles; - operators, networks, service_contracts,
contract_lots; - routes, route_variants, trips, stops, stop_sequences,
route_shapes, transfers; - drivers, driver_preferences, calendars,
duty_rosters, duty_roster_versions, duties, duty_segments; - vehicles,
vehicle_dimensions, vehicle_documents, vehicle_assignments,
vehicle_defects; - pre_trip_templates, pre_trip_checks,
inspection_items, inspection_photos; - route_knowledge, route_hazards,
route_notes, route_note_reviews; - incidents, incident_geometries,
incident_confirmations, incident_status_history; - vehicle_positions,
colleague_location_shares (rétention très courte); - documents,
document_versions, OCR_jobs, OCR_fields, knowledge_chunks; -
integrations, oauth_connections, encrypted_provider_credentials; -
notification_preferences, audit_events, data_source_status; -
tachograph_profiles, activity_entries (si module activé après validation
juridique). Toute table liée à un utilisateur ou une organisation doit
porter organization_id lorsque pertinent. Identifiants internes stables
; ne jamais utiliser seulement le numéro de parc comme clé primaire.

## 7. Consommation batterie et données mobiles

### 7.1 GPS

-   localisation précise uniquement en mode conduite ;
-   arrêter le GPS à la fin du service ou après inactivité définie ;
-   fréquence adaptative : plus élevée quand le véhicule roule et
    approche d'un arrêt/alerte, réduite à l'arrêt ;
-   faire le map matching sur l'appareil quand possible ;
-   n'envoyer au serveur que les positions nécessaires au partage
    volontaire ;
-   ne pas diffuser une position GPS brute à tous les utilisateurs ;
-   avertir le conducteur de l'impact batterie et proposer un
    branchement alimentation véhicule. Les OS limitent les tâches
    d'arrière-plan. Les fonctions de navigation natives nécessiteront
    des modes autorisés et des permissions explicites.

### 7.2 Données mobiles

-   télécharger GTFS et géométries en Wi-Fi ;
-   synchroniser uniquement les changements ;
-   compresser les événements et images ;
-   chargement progressif des tuiles ;
-   option « données mobiles minimales » ;
-   désactiver les vidéos et préchargements lourds ;
-   qualité carte ajustable ;
-   cache local de la journée de service ;
-   photos téléversées en Wi-Fi seulement, sauf choix explicite ;
-   afficher la consommation estimée et le dernier rafraîchissement. Ne
    pas utiliser les serveurs de tuiles publics standards
    d'OpenStreetMap pour du préchargement massif ou des cartes hors
    ligne : leur politique interdit le bulk download et le
    préchargement. Prévoir fournisseur de tuiles autorisant
    explicitement l'usage hors ligne ou auto-hébergement.

## 8. RGPD, droit du travail et sécurité

### 8.1 Données personnelles

Données potentiellement personnelles : - position des chauffeurs ; -
plannings et échanges de services ; - photos et dommages ; - documents
employeur ; - voix et transcriptions ; - identifiants véhicule reliés à
un conducteur ; - journaux d'utilisation. Principes : - minimisation ; -
finalités claires ; - base juridique documentée ; - information
transparente ; - durée de conservation ; - droits d'accès,
rectification, effacement et opposition selon base juridique ; -
sécurité et sous-traitants ; - transferts internationaux maîtrisés ; -
analyse d'impact si le traitement est susceptible d'engendrer un risque
élevé. Pour la géolocalisation au travail, l'Autorité belge de
protection des données explique que la géolocalisation constitue un
traitement de données personnelles et que l'employeur doit notamment
informer les travailleurs sur la base juridique, la finalité, l'étendue,
la durée, les données et les droits. L'APD indique également des usages
de surveillance à exclure, notamment le suivi permanent et le suivi hors
temps de travail dans les conditions décrites. Pour un outil personnel
entre collègues, appliquer une protection équivalente : position
partagée uniquement sur activation explicite, pendant une durée limitée,
pas de partage par défaut et pas d'usage disciplinaire caché. \### 8.2
Publiable.dev Utiliser https://publiable.dev/ comme outil de travail
pour l'analyse RGPD, sans le considérer comme une validation juridique
exhaustive. Compléter par : - registre de traitements ; - politique de
confidentialité ; - conditions d'utilisation ; - contrats de
sous-traitance (DPA) ; - politique de cookies/traceurs si applicable ; -
politique de conservation ; - procédure de violation ; - gestion des
demandes des personnes ; - analyse d'impact si nécessaire ; -
documentation des bases légales et transferts. Faire valider les
traitements de données de salariés par un juriste/DPO avant un
déploiement avec l'employeur.

### 8.3 Images et caméra

-   photos de dommages uniquement à l'arrêt ;
-   demander de cadrer le dommage et d'éviter les personnes ;
-   flouter visages et plaques privées si présentes ;
-   pas de flux caméra continu dans le MVP ;
-   pas d'enregistrement audio continu ;
-   pas de reconnaissance faciale. \### 8.4 Sécurité routière
-   aucune action interactive complexe en mouvement ;
-   commandes vocales courtes ;
-   alertes audio non répétitives ;
-   pas de publicité ;
-   pas de gamification en conduite ;
-   pas de vidéo ;
-   avertissements et consignes à l'arrêt pour les informations
    complexes ;
-   EVE ne remplace jamais les consignes du dispatch, de l'employeur, de
    la police ou des autorités routières.

## 9. Tachygraphe : périmètre et règles de prudence

Le règlement (CE) 561/2006 exclut notamment les véhicules utilisés pour
des services réguliers de transport de voyageurs lorsque le parcours du
service ne dépasse pas 50 km. Les règles applicables aux autres services
doivent être qualifiées selon leur nature, distance, caractère
national/international, régularité et éventuelles exemptions. Pour les
services soumis au règlement, les règles générales comprennent notamment
: - pause de 45 minutes au plus tard après 4 h 30 de conduite
(fractionnement 15 + 30 selon conditions) ; - repos journalier et
hebdomadaire selon les règles applicables ; - durée de conduite
journalière/hebdomadaire et règles spécifiques. Les cartes
tachygraphiques intelligentes enregistrent des activités et conservent
des données ; la Commission indique que le conducteur doit insérer sa
carte avant de conduire et que les enregistrements doivent pouvoir être
présentés pour la journée en cours et les 56 jours précédents selon le
régime applicable. EVE ne doit pas lire une carte tachygraphique sans
autorisation et conformité technique. Dans le MVP, l'utilisateur saisit
ou importe les activités pertinentes ; EVE explique les règles et
signale les incohérences, mais affiche « estimation indicative ---
vérifier le tachygraphe et les consignes officielles ». Avant lancement
de ce module : validation par un spécialiste du droit social du
transport en Belgique, et par l'employeur si l'outil est utilisé dans un
contexte professionnel.

## 10. Modèle économique proposé

### 10.1 Principe

-   Les fonctionnalités de base restent gratuites pour rendre l'outil
    utile aux chauffeurs.
-   Les coûts récurrents sont couverts par un modèle transparent, sans
    publicité et sans vendre les données.
-   Les fonctionnalités IA payantes utilisent le BYOK (clé personnelle)
    ou une option premium facultative.
-   Ne pas faire payer pour les alertes de sécurité fondamentales.

### 10.2 Gratuit

-   compte et profil ;
-   import planning OCR local/limité ;
-   services et lignes ;
-   carte et arrêts ;
-   données TEC publiques dans les limites de l'API ;
-   alertes publiques et communautaires ;
-   check-list de prise de véhicule ;
-   rapports d'avarie et photos avec quota raisonnable ;
-   fiches véhicule et de ligne ;
-   signalements entre collègues ;
-   navigation PWA en ligne, mode dégradé ;
-   guide interactif ;
-   calendrier ICS manuel ;
-   voix système (TTS/STT local ou OS lorsque disponible) ;
-   IA désactivée par défaut. Les quotas gratuits doivent être définis
    après mesure des coûts réels, sans mettre en danger les alertes
    essentielles.

### 10.3 Premium facultatif

-   IA hébergée EVE avec crédits mensuels ;
-   OCR cloud avancé et extraction complexe ;
-   recherche documentaire IA ;
-   synthèses vocales premium ;
-   stockage documentaire/photographique étendu ;
-   historique étendu et exports ;
-   synchronisation avancée de calendriers ;
-   fonctions organisation avancées ;
-   rapports statistiques non intrusifs. Le premium ne doit pas être
    nécessaire pour utiliser les fonctions essentielles en conduite.

### 10.4 BYOK

-   intégration optionnelle de clés API OpenAI, Anthropic, Google ou
    autres ;
-   le client paie directement son fournisseur ;
-   EVE facture éventuellement uniquement la couche d'intégration, si
    une valeur réelle est fournie ;
-   avertissement : un abonnement ChatGPT/Claude/Gemini grand public
    n'est pas automatiquement une clé API incluse.
-   ne jamais contourner les conditions des fournisseurs.

### 10.5 Organisations / dépôts

À terme, proposer une offre B2B : - espace organisation ; - gestion des
véhicules et dépôts ; - documents et check-lists personnalisés ; -
rapports d'avaries et workflow de maintenance ; - import des plannings
; - demandes d'échange et validation ; - statistiques agrégées ; -
intégration officielle si autorisée. Les prix seront fixés après pilote
et calcul des coûts par utilisateur actif.

### 10.6 Financement des coûts

-   contributions volontaires / soutien communautaire ;
-   premium individuel ;
-   abonnement par organisation ;
-   sponsoring non intrusif et clairement identifié, sans publicité
    pendant la conduite ;
-   partenariats avec associations professionnelles. Ne pas utiliser les
    données de localisation ou de travail pour la publicité.

### 10.7 Coûts de référence à surveiller

-   Vercel Hobby : gratuit mais réservé aux projets personnels/non
    commerciaux ; Vercel Pro affiché à 20 USD/mois, plus usage éventuel
    et taxes.
-   Supabase Free : gratuit, quotas et pause après une semaine
    d'inactivité ; Supabase Pro annoncé à partir de 25 USD/mois.
-   Apple Developer Program : 99 USD/an pour distribution officielle et
    TestFlight. Un compte gratuit permet des tests directs sur appareils
    avec Xcode mais pas la distribution App Store/ TestFlight.
-   Google Play Console : 25 USD une fois pour distribution complète. La
    documentation Google présente également une voie de distribution
    limitée sans frais pour un petit groupe de 20 appareils sous les
    conditions du programme correspondant.
-   Open-Meteo : offre gratuite non commerciale ; usage commercial avec
    licence payante.
-   Google Routes : paiement à la requête ; le trafic temps réel relève
    des fonctions plus coûteuses que le calcul basique.
-   Map tiles : ne pas présumer que les tuiles gratuites OSM sont un
    service de production ou un SLA. Tous les montants sont à revalider
    avant achat ; prix en USD hors TVA et changements de grille
    possibles.

## 11. Distribution sans frais de stores au départ

### 11.1 PWA

-   partager une URL sécurisée ;
-   « Ajouter à l'écran d'accueil » sur iPhone et Android ;
-   mises à jour automatiques ;
-   pas de frais Apple Developer ;
-   installation facile pour un petit groupe. Limites : PWA ne garantit
    pas les mises à jour GPS continues en arrière-plan, l'écoute
    permanente ou les fonctions natives nécessaires à une navigation
    professionnelle fiable.

### 11.2 Android

Pour un groupe restreint, une distribution privée / installation directe
peut être envisagée après vérification des règles Google, de la
signature et des avertissements de sécurité. Le programme Android
Developer Console mentionne une distribution limitée jusqu'à 20
appareils sans frais sous conditions. Publication Play Store complète :
25 USD une fois.

### 11.3 iOS

PWA en premier. Une application native iOS distribuée publiquement ou
via TestFlight nécessite normalement le programme Apple Developer à 99
USD/an. Un compte gratuit permet le développement et des tests directs
sur appareil avec Xcode, mais ne constitue pas un canal pratique de
diffusion à un groupe. Décision : PWA pour le pilote ; évaluer le natif
après validation du produit et financement.

## 12. Langues et voix

-   Français Belgique : priorité absolue.
-   prononciation des communes, arrêts et termes TEC ;
-   vocabulaire belge : septante, nonante, terminus, dépôt, service,
    battement, PFE, etc. ;
-   débit lent/normal/rapide ;
-   voix claire, naturelle, pas trop bavarde ;
-   commandes vocales testées dans un bus à l'arrêt, avec bruit de fond
    réel ;
-   prévoir allemand pour certaines zones de l'Est et services
    transfrontaliers, néerlandais pour extension nationale ;
-   utiliser TTS du système en première version, puis comparer les
    offres premium. Ne pas promettre une reconnaissance parfaite en
    environnement bruyant. Toujours offrir une alternative tactile à
    l'arrêt.

## 13. Roadmap recommandée

### Phase 0 --- Validation technique et UX

-   dépôt Git et documentation ;
-   maquettes de 10 écrans ;
-   test des flux GTFS TEC / SIRI ;
-   extraction d'un planning réel anonymisé ;
-   test PWA iPhone et Android ;
-   étude licences trafic, météo et tuiles ;
-   prototype GPS et map matching ;
-   revue sécurité / RGPD initiale.

### Phase 1 --- MVP pilote

-   authentification et profils ;
-   organisation pilote et dépôt ;
-   planning manuel + OCR avec correction ;
-   services et lignes ;
-   import GTFS TEC ;
-   carte et position GPS au premier plan ;
-   prochain arrêt ;
-   check-list véhicule ;
-   fiches véhicule ;
-   photos d'avaries et brouillon e-mail ;
-   alertes officielles disponibles ;
-   mode sombre accessible ;
-   tutoriel et guide.

### Phase 2 --- Navigation et communauté

-   suivi GPS optimisé ;
-   alertes sur la portion réelle du parcours ;
-   signalements communautaires ;
-   confirmations et expiration ;
-   partage volontaire de position ;
-   fiches de difficulté avec validation ;
-   notifications vocales ;
-   cache hors ligne.

### Phase 3 --- Intelligence métier

-   assistant vocal conversationnel ;
-   commandes de navigation dans l'application ;
-   recherche documentaire PFE et véhicules ;
-   calendrier Google/Microsoft/ICS ;
-   suggestions d'échange de services ;
-   module tachygraphe après validation juridique.

### Phase 4 --- Produit multi-opérateurs

-   répertoire opérateurs et dépôts ;
-   import de données de plusieurs réseaux ;
-   allemand/néerlandais ;
-   intégration organisation ;
-   workflow responsable / mécanicien ;
-   application native si budget validé ;
-   offres B2B et premium.

## 14. Critères d'acceptation du MVP

1.  Un nouveau chauffeur termine l'inscription et le tutoriel sans aide
    externe.
2.  Il peut importer un planning et corriger chaque donnée OCR
    incertaine.
3.  Le service du jour est visible et peut être modifié sans perdre
    l'historique.
4.  La carte montre le bon parcours, le sens, les arrêts et la position
    actuelle.
5.  Si le GPS ou le flux temps réel est indisponible, l'interface le dit
    clairement.
6.  Une alerte hors parcours n'interrompt pas le conducteur.
7.  Une alerte située sur le parcours est présentée avec portion,
    distance/temps avant l'événement, source et fraîcheur.
8.  La check-list est configurable et utilisable hors ligne.
9.  Les photos sont reliées au véhicule, à l'item et au rapport.
10. Aucun e-mail n'est envoyé sans confirmation.
11. Les données d'une organisation ne sont jamais visibles par une autre
    organisation.
12. L'utilisateur peut désactiver le partage de position et supprimer
    ses données selon les règles applicables.
13. Le mode conduite ne permet pas d'éditer du texte ni de consulter des
    documents longs.
14. Les contrastes sont mesurés et respectent WCAG 2.2 AA pour les
    éléments concernés.
15. Aucun itinéraire alternatif n'est qualifié de sûr sans validation
    vérifiable.
16. Aucune indication tachygraphique n'est présentée comme une
    certification ou un remplacement du dispositif officiel.

## 15. Risques et décisions à prendre

  -----------------------------------------------------------------------
  Risque                              Mesure
  ----------------------------------- -----------------------------------
  Flux TEC modifié / indisponible     adaptateur isolé, cache,
                                      monitoring, fallback

  Données temps réel retardées        afficher fraîcheur et qualité

  Déviation dangereuse                statut candidat, validation
                                      obligatoire

  OCR incorrect                       confirmation humaine

  PWA limitée en arrière-plan         natif ultérieur, mode foreground
                                      explicite

  Batterie / data                     GPS adaptatif, synchronisation
                                      minimale

  Fausse alerte collègue              confirmations, expiration,
                                      modération

  Fuite de planning ou position       RLS, minimisation, audit, rétention

  Dépassement coûts                   quotas, budgets, alertes, BYOK

  Tachygraphe mal interprété          classification et validation
                                      juridique

  Usage commercial des API gratuites  licence commerciale avant
  interdit                            monétisation

  Dépôt ou contrat mal identifié      vérification admin, dates de
                                      validité
  -----------------------------------------------------------------------

## 16. Liste des tâches de recherche restantes

Avant d'implémenter les connecteurs : 1. Créer un compte développeur
Belgian Mobility Open Data et tester les quotas réels,
l'authentification, les licences et les limites de débit. 2. Tester la
présence, la stabilité et la granularité des positions TEC SIRI. 3.
Demander au SPW/PEREX une documentation d'accès aux flux machine
trafic/travaux. 4. Vérifier les licences et les conditions de
cache/redistribution des tuiles cartographiques. 5. Vérifier les données
OSM utiles aux autobus : hauteur, largeur, tonnage, restrictions,
giration et sens. 6. Collecter un échantillon anonymisé de planning
mensuel et de classeur de ligne. 7. Identifier les procédures de prise
de véhicule et avarie validées par l'employeur. 8. Faire vérifier les
obligations tachygraphiques par type de service. 9. Faire valider le
schéma RGPD et les durées de conservation. 10. Tester la PWA sur iPhone
réel et Android réel, écran verrouillé et réseau dégradé.

## 17. Consignes de travail à Claude Code

Claude Code doit commencer par auditer le dépôt existant et
l'environnement avant toute modification. Ne pas supposer que la stack
proposée est déjà installée. Ne pas réécrire une application existante
sans inventaire. Ordre de travail : 1. Inspecter repository, package
manager, framework, Supabase, Vercel, conventions et tests. 2. Écrire un
rapport d'audit et proposer l'architecture finale avec justification. 3.
Lister les décisions bloquantes et les hypothèses. 4. Créer ADR
(Architecture Decision Records). 5. Définir schéma de données et
politiques RLS avant les écrans. 6. Construire un prototype isolé des
données GTFS TEC. 7. Développer les écrans MVP et tests. 8. Ajouter
tests d'accessibilité, sécurité, hors ligne et consommation. 9. Ne
jamais inventer de données/API ou de résultats de test. 10. Demander
validation humaine pour les décisions critiques de sécurité, juridiques,
itinéraires et échanges de service. 11. Maintenir une documentation
utilisateur accessible aux conducteurs peu à l'aise avec la technologie.
12. Livrer par petites étapes, avec tests et notes de version.

### Instruction fondamentale

Claude Code est autorisé à remettre en question ce PRD. S'il découvre
une incompatibilité technique, une API inexistante, une contrainte
iOS/Android, un risque de sécurité, une licence incompatible ou une
meilleure architecture, il doit le signaler et proposer une alternative
avant d'implémenter. La sécurité, la confidentialité, la fiabilité et la
simplicité priment sur la vitesse de développement.

------------------------------------------------------------------------

## 18. Sources de recherche consultées

### Données transport

-   Belgian Mobility Open Data --- données :
    https://data.belgianmobility.io/en/data.html
-   Belgian Mobility Open Data --- FAQ / licences / gratuité :
    https://data.belgianmobility.io/en/faq.html
-   Belgian Mobility Open Data --- documentation API :
    https://data.belgianmobility.io/en/knowledge-base.html
-   Wallonie --- TEC et réseau :
    https://mobilite-waf.wallonie.be/home/acteurs/tec.html
-   Wallonie --- organisation OTW et business units :
    https://www.wallonie.be/nl/actoren-en-instellingen/wallonie/autres-acteurs-publics-de-la-wallonie/operateur-de-transport-de-wallonie-otw
-   FBAA --- localisateur des entreprises :
    https://www.fbaa.be/fr/entrepreneurs/localisateur-dentreprises
-   Letec Finder --- FAQ technique non officielle sur PFE et positions :
    https://letecfinder.be/faq

### Trafic, cartes et météo

-   Wallonie --- informations trafic, travaux et PEREX :
    https://economie.wallonie.be/en/demandes/2718_requesting-information-about-traffic-conditions-traffic-roadworks-accidents-congestion-etc.html
-   Trafiroutes : https://trafiroutes.wallonie.be/
-   OpenStreetMap licence : https://www.openstreetmap.org/copyright
-   OpenStreetMap tile usage policy :
    https://operations.osmfoundation.org/policies/tiles/
-   Valhalla route API :
    https://valhalla.github.io/valhalla/api/route/api-reference/
-   Open-Meteo tarifs : https://open-meteo.com/en/pricing
-   Open-Meteo conditions : https://open-meteo.com/en/terms
-   Google Routes billing :
    https://developers.google.com/maps/documentation/routes/usage-and-billing

### Tachygraphe / transport

-   Règlement (CE) 561/2006 :
    https://eur-lex.europa.eu/eli/reg/2006/561/2024-12-31/eng/
-   Commission européenne --- temps de conduite et repos :
    https://transport.ec.europa.eu/transport-modes/road/social-provisions/driving-time-and-rest-periods_en
-   Commission européenne --- tachygraphe :
    https://transport.ec.europa.eu/transport-modes/road/tachograph_en
-   Commission européenne --- Q&A 56 jours :
    https://transport.ec.europa.eu/transport-modes/road/mobility-package-i/tachographs/questions-and-answers-tachograph-provisions-mobility-package-1_en
-   Your Europe --- règles transport routier :
    https://europa.eu/youreurope/citizens/work/work-abroad/rules-working-road-transport/indexamp_en.htm

### Confidentialité et accessibilité

-   APD Belgique --- géolocalisation au travail :
    https://www.autoriteprotectiondonnees.be/professionnel/themes/vie-privee-sur-le-lieu-de-travail/surveillance-de-l-employeur/geolocalisation
-   WCAG 2.2 : https://www.w3.org/TR/WCAG22/
-   W3C contraste AA :
    https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

### Hébergement et distribution

-   Vercel pricing : https://vercel.com/pricing
-   Supabase pricing : https://supabase.com/pricing
-   Apple Developer Program : https://developer.apple.com/programs/
-   Google Play Console :
    https://support.google.com/googleplay/android-developer/answer/6112435/
-   Android limited distribution :
    https://support.google.com/android-developer-console/answer/16604405

### Nom et domaine

-   DNS Belgium --- vérification .be : https://www.dnsbelgium.be/en/
-   DNS Belgium --- statut d'un domaine :
    https://www.dnsbelgium.be/en/domain-name-status

------------------------------------------------------------------------

## 19. Nom du projet --- pistes préliminaires

Le nom de travail reste **EVE**, mais il est trop court et très utilisé
pour constituer une marque distinctive sans vérification approfondie. Il
ne faut pas enregistrer un domaine ni déposer une marque sur la seule
base de cette liste.

Première recherche exploratoire : - **Navelys** : à exclure, le nom est
déjà utilisé dans le secteur du transport et du logiciel. - **Lignova**
: à exclure, une société technologique utilise déjà ce nom. -
**Routiva** : à exclure de la shortlist, une société porte déjà ce
nom. - **Conduvia** : à exclure, utilisé dans le domaine logiciel/IA. -
**Buselium** : piste de travail à investiguer ; aucune disponibilité
juridique ou .be n'est garantie. - **Buselya** : piste de travail à
investiguer ; aucune disponibilité juridique ou .be n'est garantie. -
**BusVeya** : piste de travail à investiguer ; aucune disponibilité
juridique ou .be n'est garantie.

Avant décision : 1. vérifier le .be via DNS Belgium et les extensions
.com/.eu ; 2. vérifier les marques Benelux via BOIP et les marques
européennes via EUIPO ; 3. rechercher les sociétés et applications
existantes ; 4. vérifier les réseaux sociaux et prononciation en
français, néerlandais et allemand ; 5. réserver domaine et marque
seulement après vérification juridique.

**Recommandation provisoire :** conserver « EVE » comme nom de
l'assistante vocale et choisir une marque produit distincte, par exemple
« Buselium --- avec EVE à bord », uniquement si les vérifications de
disponibilité aboutissent.

Fin du document.
