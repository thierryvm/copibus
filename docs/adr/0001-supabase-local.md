# 0001 — Supabase en local pour tout le développement

- **Date :** 2026-11-25
- **Statut :** acceptée
- **Vérification de phase 0 :** 1 (voir `docs/PRD-v2.md` §9)

## Question

Est-ce que Supabase tourne en local (CLI + Docker) sur le poste de développement, à côté des autres projets qui utilisent déjà Supabase en local, sans les gêner ?

## Ce qui a été testé

- Supabase CLI v2.109.1 et Docker Desktop, sous Windows 11.
- `supabase init` dans le dépôt, puis `supabase start` et `supabase stop`, lancés **uniquement pour ce projet** (jamais `--all`).
- Trois autres projets avaient déjà leur Supabase local en marche, sur les ports 543xx et 544xx. Ils sont restés allumés pendant tout le test.

## Résultats

Vérifié le 25/11/2026 :

- **Démarrage :** 52 s (`time supabase start`). Les images Docker étaient déjà sur la machine, à cause des autres projets. Un tout premier démarrage, qui les télécharge, prend plus longtemps.
- **Services :** 12 conteneurs `*_copibus` démarrent. `imgproxy` et `pooler` restent arrêtés, ce qui est leur réglage par défaut.
- **Réponses des services :**
  - API REST : HTTP 200 sur `http://127.0.0.1:54721/rest/v1/`.
  - Studio : HTTP 307 (redirection vers sa page d'accueil) sur `:54723`.
- **Base de données :** PostgreSQL 17.6.
  - Extensions déjà installées : `pg_net`, `pg_stat_statements`, `pgcrypto`, `supabase_vault`, `uuid-ossp`.
  - Extensions disponibles à activer : `postgis`, `pg_cron` et `pgmq`.
- **Arrêt :** `supabase stop` arrête les 12 conteneurs de Copibus. Les trois autres bases locales tournent encore après l'arrêt. Les données locales sont gardées dans un volume Docker.

## Décision

- **Ports réservés à Copibus**, de 54720 à 54729 pour ne pas entrer en conflit avec les autres projets :

  | Service | Port |
  |---|---|
  | Base « shadow » | 54720 |
  | API | 54721 |
  | Base de données | 54722 |
  | Studio | 54723 |
  | E-mails de test | 54724 |
  | Analytique | 54727 |
  | Pooler | 54729 |
  | Inspecteur des Edge Functions | 8783 |

- **Inscription libre coupée** (`[auth] enable_signup = false`), dès le local. L'app fonctionne sur invitation (décision D9 du PRD).
  - Attention : `[auth.email] enable_signup = true` doit rester à `true`. Malgré son nom, ce réglage active la connexion par e-mail, pas l'inscription libre (la CLI le traduit en `GOTRUE_EXTERNAL_EMAIL_ENABLED`). Le passer à `false` empêcherait les personnes invitées de se connecter. Un commentaire le rappelle dans `config.toml`.
- On développe uniquement en local. Le projet cloud `copibus` (décision D11 du PRD) **n'est pas relié** au dépôt avant le pilote : aucun `supabase link`, aucun jeton cloud.
- Le dossier `supabase/` est versionné. `config.toml` ne contient aucun secret : les clés locales sont générées par la CLI. Les dossiers `.temp/` et `.branches/` sont exclus de git.

## Conséquences

- Pour démarrer : `supabase start` à la racine du dépôt. Pour arrêter : `supabase stop`, jamais `supabase stop --all`, qui couperait les autres projets.
- La CLI v3.4.0 est sortie. C'est une version majeure : on la prévoit au début de M0, sans la prendre au passage.
- Le jeton `SUPABASE_ACCESS_TOKEN` du contexte `perso` vise un autre compte. Il ne doit pas servir pour ce projet. Un jeton dédié ira dans le coffre DevContext au moment du pilote.
- **Réseau local : à surveiller.** La CLI publie les ports de la pile sur toutes les interfaces (`0.0.0.0`), pas seulement sur la machine. Essai du 25 novembre 2026 : un réseau Docker limité à `127.0.0.1` (`supabase start --network-id …`) ne change rien avec Docker Desktop sous Windows, les ports restent sur `0.0.0.0`. Or le pare-feu Windows contient une règle « Docker Desktop Backend » qui accepte les connexions entrantes sur les profils **privé et public**. La pile locale utilise des identifiants de démonstration connus de tous (base `postgres`, clé `service_role` de démo, Studio sans mot de passe). Sur un réseau non fiable (Wi-Fi public, dépôt), une autre machine pourrait donc y accéder. Ce réglage concerne toute la machine et les autres projets : la décision revient à Thierry (par exemple retirer le profil public de cette règle). En attendant : **ne lancer la pile que sur un réseau de confiance**, et ne jamais y mettre de données réelles.
- **Avant de relier le projet cloud (pilote)**, il faudra durcir ou séparer plusieurs réglages acceptables seulement en local, car la commande de publication de configuration de la CLI reprend `config.toml` tel quel : longueur minimale du mot de passe (6) sans autre exigence, confirmation des e-mails désactivée, `secure_password_change = false`, `site_url` en `127.0.0.1`.
- Le PRD ne change pas.
