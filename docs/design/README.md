# Design de Copibus — référence pour coder l'interface

Ce fichier résume le canevas de design. La source de vérité produit reste `docs/PRD-v2.md` : en cas d'écart entre le canevas, ce fichier et le PRD, c'est le PRD qui fait foi, et tout changement passe par un ADR et une mise à jour du PRD.

## Canevas

- Adresse : https://claude.ai/artifact/UPhReypoKwSxE7WDHtFL64 (privé). Chaque écran se lit dans le fichier `project/<écran>.dc.html`.
- Direction retenue : **A « Halo »**. EVE est un robot copilote avec un micro-casque, en bleu nuit et cyan, avec des panneaux translucides posés sur la carte. Les directions B et C ont été supprimées.
- Version 34 : 24 écrans sur 4 rangées.

| Rangée | Écrans |
|---|---|
| 1. Conduite | Main, A-Guidage, A-Deviation, A-Economie, A-Pause, A-FinService, A-Checklist, A-Signaler |
| 2. Réseau | A-Carte, A-Lignes, A-LigneDetail, A-Arret, A-EVE, A-Proactif |
| 3. Compte | A-Connexion, A-Onboarding (5 étapes), A-Moi, A-Planning, A-Import, A-Reglages, A-Support, A-Mascotte (6 expressions) |
| 4. Administration | Admin-Dashboard (ordinateur), Admin-Mobile |

## Couleurs

### Fonds et surfaces

| Rôle | Valeur |
|---|---|
| Fond de l'app | `#070B14` |
| Fond du guidage | `#05080F` |
| Fond du mode économie | `#000000` |
| Surfaces | `#101827`, `#0C1320`, `#1A2538` |
| Pastille de ligne | `#24324A` |

### Texte

| Rôle | Valeur |
|---|---|
| Principal | `#EEF3FA` |
| Secondaire | `#C9D4E3`, `#B3C0D2` |
| Tertiaire | `#8FA0B8` |

### Accent

- Choisi par le chauffeur dans les réglages : `#3FD8FF` (par défaut), `#7CF29A`, `#FFB547`, `#B9A6FF`, `#FF8FB8`.
- Texte posé sur l'accent : `#04121A`.
- Contrastes vérifiés par script sur les 24 écrans et les 5 accents : tout texte est à **4,5:1 ou plus** (minimum relevé 5,06:1), et le texte sur un bouton d'accent à **8,9:1 ou plus**.
- **Règle :** on ne propose une nouvelle couleur que si elle tient ces deux seuils.

### États du temps réel

Affichés **en mots et avec une icône**, jamais par la couleur seule. Règle du PRD : l'avance et le retard ne s'affichent qu'**à l'arrêt** ; pendant la conduite, ces deux états sont masqués.

| État | Texte | Fond |
|---|---|---|
| À quai, à l'heure | `#7DF0B0` | `#0F2E22` |
| En retard | `#FFC46B` | `#33240C` |
| En avance | `#8BC8FF` | `#10243A` |
| Prévu (horaire théorique) | `#C9D4E3` | `#1A2538` |

- Suivi en direct : point vert qui pulse.
- Heure prévue : cercle en pointillés.
- **Une heure prévue n'est jamais présentée comme du direct.**

### Déviation et avertissements

- Déviation, hors parcours : ambre `#FFB547`.
- Avertissements : `#FFD9A0` sur `#1F1A10`.

## Typographie et formes

- Polices : **Inter** pour le texte ; **Space Grotesk** pour les heures, les distances et les titres, avec un interlettrage négatif aux grandes tailles.
- Rayons d'angle : de 10 à 28 px.
- Zones tactiles : 44 px minimum ; les grands boutons de conduite font **88 px**.

## Retour au toucher et mouvement

- Appui : `scale(.97)` en 120 ms. Avec « réduire les animations » : opacité .8 à la place.
- Avec « réduire les animations », le point du suivi en direct ne pulse plus (point plein fixe) et la bouche d'EVE reste immobile (l'état « parle » est montré par une icône).
- La bouche d'EVE suit la parole : événements `boundary` de la synthèse vocale, ou volume réel pour la voix premium.

## Navigation

- Écrans principaux : barre du bas de 84 px, translucide avec flou.
- 5 places : Aujourd'hui, Carte, bouton EVE central de 48 px qui dépasse vers le haut, Lignes, Moi. Libellés de 12 px sur une ligne de base commune.
- Écrans de conduite : **pas de barre du bas**, zéro toucher en roulant.
- Sorties utilisables à l'arrêt :
  - « Menu », 88 px, retour à l'accueil, en miroir de « Silence » ;
  - la pastille de ligne, qui ouvre la liste des arrêts ;
  - « Éco », pour le mode économie ;
  - le bandeau de déviation, qui ouvre la carte.
- **Chaque écran a une sortie visible.**

## Contenu des maquettes

- Planning **fictif** sur le modèle d'un vrai planning de chauffeur (un service coupé), avec des horaires TEC publics du 23/11 : lignes 64 (`gr:tec:L0064-24183`), 65 (`gr:tec:L0065-24185`) et 727 (`gr:tec:L0727-23616`, voir `docs/donnees/sources.md`) ; Aywaille Gare SNCB ; quais D et C à Guillemins.
- Retards, perturbations, notes et messages sont **inventés**.
- L'écran des arrêts, EVE proactive et la demande complète à EVE sont décrits dans `docs/PRD-v2.md` §4.2 et §4.6.

## Vérification du canevas (25/11/2026)

J'ai relu les 24 fichiers d'écran de la version 34 pour confronter cette référence au canevas.

**Conforme :**

- Barre du bas : 84 px, 5 places, bouton EVE central de 48 px, libellés de 12 px. Absente du guidage et du mode économie.
- Boutons « Menu » et « Silence » à 88 px sur les écrans de conduite.
- Couples de couleurs des 4 états du temps réel : identiques.
- Point direct qui pulse (vert `#5BE49B`) et cercle en pointillés pour l'heure prévue.
- Retour au toucher `scale(.97)` / opacité .8.
- Polices chargées : Inter 400 à 700, Space Grotesk 500 à 700.
- A-Reglages propose bien les 5 accents, rose `#FF8FB8` compris.
- Déviation en ambre `#FFB547` sur A-Deviation.
- A-Mascotte montre les 6 expressions : Prête, Parle, Contente, Attention, Réfléchit, En pause.

**Écarts et compléments à connaître en codant :**

- Le sélecteur d'accent des composants du canevas (`data-props`) ne liste que 4 couleurs : le rose y manque, alors que l'écran Réglages le propose. L'app doit offrir les 5.
- Le mode économie a sa propre palette : texte `#FFFFFF`, secondaire `#B4BCC8`, pastille « Éco » `#8EF0C0` sur `#0E2A22`, séparateur `#1F2633`.
- Surfaces supplémentaires : `#131D30` (tuiles de raccourcis) ; `#0E1E2C` avec une bordure d'accent à 53 % d'opacité pour la ligne de sa propre course. Panneaux du guidage : `rgba(12,20,34,.78)` à `.86` avec `blur(24px)`.
- Opacité de la barre du bas : .72 sur Main, .82 sur A-Arret. À unifier (proposition : .82, plus lisible sur la carte).
- Heures barrées en `#8391A6` (contraste estimé 5,4:1 sur `#101827`) ; même gris pour le cercle de l'heure prévue.
- Survol des liens : `#8BE8FF`.
- Bouton « C'est parti » à 72 px, pas 88 px (il se touche à l'arrêt, avant le départ).
- Le fond d'avertissement `#1F1A10` n'apparaît que sur A-Import et A-Lignes ; ailleurs, le texte `#FFD9A0` est posé sur d'autres surfaces. À harmoniser en codant.
- Notes du canevas : les codes Keolis sont encore à confirmer ; sur iPhone, EVE prévient à l'heure prévue, car détecter l'arrivée demande une app native.
