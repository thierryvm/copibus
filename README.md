# Copibus (nom provisoire)

Copilote pour les chauffeurs de bus du réseau TEC en Wallonie. L'assistante, EVE par défaut (renommable), guide le chauffeur sur le vrai tracé de la ligne, l'aide à préparer son service et le prévient de ce qu'il doit savoir.

Application indépendante, non affiliée au TEC, à la SNCB ni à Keolis.

**Tous droits réservés.** Le dépôt est public pour la consultation et la revue de code seulement : aucune réutilisation n'est autorisée sans accord écrit (voir [LICENSE](LICENSE)).

## État

- **Cadrage et design terminés** (novembre 2026) : voir [docs/PRD-v2.md](docs/PRD-v2.md) et le canevas de design (privé).
- **Phase 0 en cours** : vérifications techniques avant tout code applicatif, chacune conclue par une décision écrite dans [docs/adr/](docs/adr/). Plan : [docs/phase-0/PLAN.md](docs/phase-0/PLAN.md).

## Documents

| Document | Contenu |
|---|---|
| [docs/PRD-v2.md](docs/PRD-v2.md) | besoin, principes, modules, architecture, phase 0 |
| [docs/cadrage/verifications-2026-11-24.md](docs/cadrage/verifications-2026-11-24.md) | faits vérifiés sur les données TEC |
| [docs/recherche/benchmark-2026-11-25.md](docs/recherche/benchmark-2026-11-25.md) | ce que font les autres applis, faisabilité, navettes SNCB |

## Données

Données ouvertes TEC et SNCB (Belgian Mobility, transportdata.be), fonds de carte OpenStreetMap. Aucune donnée de santé n'est collectée.
