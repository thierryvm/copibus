# CLAUDE.md — Copibus

Projet personnel de Thierry (chauffeur de bus TEC, dépôt de Banneux). Le profil global `~/.claude/CLAUDE.md` s'applique ; ce fichier le complète.

## Identité et accès

- Contexte DevContext **`perso`** : toute commande sortante part de PowerShell, préfixée par `work perso -NoCd &&`.
- GitHub : dépôt `thierryvm/copibus`, **public** pour permettre la revue Sourcery, tous droits réservés (`LICENSE`). Tout ce qui est versionné est donc visible de tous : aucun identifiant d'infrastructure, aucune donnée personnelle, aucun secret. Les identifiants vont dans `.claude/infra.local.md` (non versionné).
- Supabase : développement **en local** (CLI + Docker). Le projet cloud `copibus` (identifiants dans `.claude/infra.local.md`, non versionné) ne sert qu'au pilote. Le jeton `SUPABASE_ACCESS_TOKEN` du contexte `perso` vise un **autre** compte : ne pas l'utiliser pour ce projet tant qu'un jeton dédié n'est pas dans le coffre.

## Interdits absolus

- Ne jamais toucher les autres projets de Thierry, en particulier **Terminal Learning** (sa vitrine en production) et **ankora-prod** (identifiants dans `.claude/infra.local.md`).
- Ne jamais versionner `docs/cadrage/exemples/` : captures de planning, données personnelles.
- Aucune donnée de santé. Logs sans données personnelles.
- Secrets uniquement en variables d'environnement (coffre DevContext), jamais dans un fichier, un log, une URL ou un outil navigateur.
- Aucun envoi externe (e-mail à la SNCB, à Keolis, au TEC) sans l'accord explicite de Thierry.

## Règles du projet

- Tout ce qui s'adresse à Thierry est en **français** (il lit mal l'anglais) : messages, rapports, PR, README, ADR. Le code et ses commentaires sont en anglais.
- **Phase 0 :** pas de code applicatif. Les sondes et prototypes vivent dans `spikes/<sujet>/` et chaque vérification se conclut par une décision dans `docs/adr/NNNN-titre.md` (modèle : `docs/adr/0000-modele.md`). Plan et suivi : `docs/phase-0/PLAN.md`.
- Source de vérité produit : `docs/PRD-v2.md`. Toute décision qui le contredit passe par un ADR et une mise à jour du PRD.
- Données : une ligne TEC s'identifie par son `route_id`, jamais par son seul numéro (quatre « 65 », six « 10 » en Wallonie). Les données horaires, arrêts et quais sont déterministes et sourcées ; l'IA ne les invente jamais.
- Scripts qui lisent des données téléchargées : Python lancé avec `-I`, données dans `data/raw/` (ignoré par git), scripts dans un dossier séparé.
- Branches `feature/`, `fix/` ; jamais de commit direct sur `main` après le commit initial. Une PR par vérification de phase 0.
- Design : canevas Claude Design https://claude.ai/artifact/UPhReypoKwSxE7WDHtFL64 (direction A « Halo »).
