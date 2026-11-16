# Pulse (nom de code provisoire)

Application Android **gratuite et hors ligne** qui estime le rythme cardiaque à partir de la caméra arrière et du flash (doigt sur l’objectif), enregistre un historique local sur 30 jours, et affiche un indicateur de suivi (vert / orange / rouge) pour aider à décider si consulter un professionnel de santé.

**Ce n’est pas un dispositif médical.** Aucun diagnostic, aucune prédiction de maladie, aucune garantie de « tout va bien ».

Public visé : agents de santé communautaires, centres de santé et grand public au Cameroun, sur téléphones Android d’entrée de gamme.

## État du projet

| Phase | Contenu | Statut |
|-------|---------|--------|
| 0 | Validation de l’algorithme PPG en Python | En cours |
| 0 bis | Entretiens avec des professionnels de santé | En parallèle (hors code) |
| 1 | MVP Flutter (mesure, indicateur, historique) | À venir |
| 2 | Agent conversationnel (règles, langues) | Plus tard |
| 3 | Alertes / orientation / mode agent | Optionnel |

## Limites (à lire)

- La mesure par caméra (PPG) est sensible au mouvement, à la pression du doigt, à la qualité du flash/caméra et à la teinte de peau.
- Les seuils de l’indicateur sont **indicatifs** et doivent être validés par un professionnel de santé avant un usage réel.
- Sans connexion réseau volontairement : les données restent sur le téléphone.

## Structure du dépôt

```
docs/           Cahier des charges, protocole, notes
notebooks/      Phase 0 — analyse Python
data/           Données anonymisées (jamais de noms / visages)
app/            Application Flutter (phase 1)
tests/fixtures/ CSV d’exemple avec bpm attendu
```

Détail : voir [`docs/CAHIER_DES_CHARGES.md`](docs/CAHIER_DES_CHARGES.md).

## Démarrage rapide (phase 0)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab   # ou l’extension Jupyter dans Cursor
```

Les notebooks attendront des fichiers dans `data/raw/` (CSV `timestamp_ms,mean_r,mean_g,mean_b` ou vidéos). En attendant la collecte réelle, on utilisera des fixtures dans `tests/fixtures/`.

## Confidentialité

- Consentement explicite avant usage.
- Pas de serveur dans le MVP ; suppression des données possible depuis l’app (phase 1).
- Collecte phase 0 : codes anonymes (P001…), pas de donnée nominative dans le dépôt.

## Licence

À définir (objectif open source).
