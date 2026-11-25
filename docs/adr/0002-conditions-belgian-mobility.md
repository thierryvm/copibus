# 0002 — Conditions de Belgian Mobility : licence, quotas, clé

- **Date :** 2026-11-25
- **Statut :** acceptée
- **Vérification de phase 0 :** 3 (voir `docs/PRD-v2.md` §9)

## Question

A-t-on le droit de réutiliser les données TEC publiées par Belgian Mobility (BMC) dans Copibus ? Si oui, à quelles conditions, et avec combien d'appels permis ?

## Ce qui a été testé

Lecture le 25/11/2026 des pages publiques :

- https://data.belgianmobility.io/en/terms.html (conditions, « Last updated: December 2025 »)
- https://data.belgianmobility.io/en/data.html
- https://data.belgianmobility.io/en/faq.html
- https://data.belgianmobility.io/en/knowledge-base.html
- le portail développeur `api-management-opendata-production.developer.azure-api.net`. Sans compte, on n'y voit pas la liste des offres.

Pas de clé développeur au moment du test (rien sous `devctx/perso/bmc-key` dans le coffre). Tout a donc été fait en **accès anonyme**.

## Résultats

### Licence (vérifié dans les conditions, §3 et §4)

- **CC BY 4.0.** Le TEC reste le seul concédant de la licence. BMC n'est que l'opérateur technique.
- **Usage commercial permis**, à condition de citer la source.
- **Mention minimale** : « Source : [nom de l'opérateur] – Open Data – [date de mise à jour du jeu] ». Si les données ont été modifiées, BMC recommande en plus : « Contient des données publiées à l'origine par [opérateur], modifiées par [utilisateur] ».
- La FAQ demande aussi de citer « Belgian Mobility Company » avec un lien vers le portail. Copibus suivra les deux.
- **Aucune garantie** : les données sont fournies « en l'état ».
- Aucune règle trouvée sur la redistribution des données dérivées ni sur la mise en cache, au-delà de la licence CC BY 4.0. La base de connaissances conseille même de mettre les données en cache pour réduire les appels.

### Accès et quotas (conditions §5, présentés comme « indicatifs »)

| Niveau | Pour quoi | Quota | Garantie de service |
|---|---|---|---|
| Anonyme | exploration, tests | 100 appels/jour, 10/minute | aucune |
| Standard (compte gratuit) | production | 12 000 appels/jour, 500/minute | aucune |
| Gold | sur demande, peut devenir payant | à négocier | oui |

- Si on dépasse le quota, le service peut répondre **HTTP 429** (trop de requêtes) et restreindre l'accès pendant un temps.
- La clé s'envoie dans l'en-tête `bmc-partner-key`. Elle est **personnelle et non transférable** : ni partagée, ni divulguée.
- En cas d'abus ou de mise en danger du service, l'accès peut être suspendu (§9).

### Fréquence de mise à jour (page données et FAQ)

- GTFS statique TEC : une fois par jour. L'heure n'est pas indiquée. Le fichier du 25/11/2026 date de 02 h 43 (heure du fichier dans le zip).
- GTFS-RT et SIRI : environ toutes les 30 secondes.

### Points non trouvés

- Le quota s'applique-t-il par clé ou par adresse IP ?
- Le service envoie-t-il un délai d'attente (`Retry-After`) avec le 429 ?
- Le quota est-il le même pour chaque flux ?
- Y a-t-il un quota de bande passante ?
- Quelle est la liste des offres du portail développeur ? Elle n'est visible qu'avec un compte.
- La base de connaissances donne **deux familles d'adresses** pour le GTFS-RT TEC :
  - `opendata-discovery-gtfs-realtime...`, déjà constatée hors service (DNS) ;
  - `api.belgianmobility.io/api/gtfs/feed/tec/rt/...`.

  À trancher dans la vérification 10 (ADR 0005).

## Décision

1. **La réutilisation est permise** : licence CC BY 4.0, usage commercial compris. Copibus peut traiter le GTFS TEC dans son pipeline et republier les paquets de ligne dérivés sur Vercel, en fichiers statiques.
2. **Mention de la source obligatoire**, à deux endroits :
   - dans l'app (écran « À propos » et pied de la carte) :
     « Source : TEC – Open Data, via Belgian Mobility Company – données du JJ/MM/AAAA. Contient des données modifiées par Copibus. » ;
   - dans chaque paquet de ligne, avec la date du jeu (`feed_version`).
3. **La clé BMC reste côté serveur.** Elle sert dans le pipeline et dans les Edge Functions, jamais dans le code envoyé au téléphone ni dans un fichier statique. Raison : elle est personnelle, et la publier violerait les conditions §5. Les téléphones ne doivent donc **jamais** appeler BMC directement. Le temps réel passe par une fonction serveur qui fait un seul appel et le partage entre tous les utilisateurs, avec un cache.
4. **Budget d'appels** prévu pour la production, en compte Standard :
   - le temps réel est interrogé toutes les 30 s par le serveur, soit 2 880 appels/jour par flux ;
   - avec 2 flux, on reste sous 6 000 appels/jour, c'est-à-dire moins de la moitié du quota ;
   - un 429 fait passer l'app en mode « horaire théorique », sans relance agressive.
5. **En phase 0**, l'accès anonyme suffit pour explorer, à condition de rester sous 100 appels par jour : on compte les appels faits dans les sondes.

## Conséquences

- **À faire par Thierry avant M1** : créer le compte développeur gratuit sur le portail BMC, puis la clé « Standard ». La clé va dans le coffre DevContext `perso` sous le nom `devctx/perso/bmc-key`. `docs/phase-0/PLAN.md` disait `BMC_API_KEY` : le nom est aligné dans la PR de fin de phase 0.
- **PRD §9, point 3** : la vérification passe à « faite ». La section des risques note qu'il n'y a **aucune garantie de service** sur le niveau gratuit, d'où l'importance du mode dégradé « horaire théorique ».
- **À revérifier** quand la clé existera :
  - quota par clé ou par IP ;
  - en-têtes du 429 ;
  - offres réellement proposées sur le portail.
- Les conditions peuvent changer (§8 : BMC prévient « via la plateforme »). Il faudra les relire avant le pilote.
