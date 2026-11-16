# Données (anonymisées uniquement)

## Règles

- Aucun nom, visage, numéro de téléphone ou donnée nominative.
- Identifiants : `P001`, `P002`, …
- Les vidéos brutes restent en local dans `raw/` (ignorées par Git si lourdes).
- Le format de référence pour l’algo : CSV `timestamp_ms,mean_r,mean_g,mean_b`.

## Fichiers

| Fichier | Rôle |
|---------|------|
| `metadata.csv` | Une ligne par mesure (protocole section 7.3) |
| `raw/` | Vidéos ou CSV de signal bruts |
| `processed/` | Signaux traités / exports d’analyse |

## Collecte

Voir `docs/PROTOCOLE_COLLECTE.md`. Tant que la collecte n’a pas commencé, le notebook peut tourner sur `tests/fixtures/`.
