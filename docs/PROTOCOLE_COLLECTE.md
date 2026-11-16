# Protocole de collecte — phase 0

Résumé opérationnel du cahier des charges (section 7). À affiner sur le terrain.

## Objectif

Comparer le bpm estimé par caméra + flash à un appareil de référence (oxymètre / tensiomètre pharmacie), sur des teintes de peau et téléphones variés.

## Minimum visé

- ≥ 30 participants volontaires, consentement oral ou écrit.
- ≥ 3 modèles de téléphones Android.
- Teintes de peau variées (groupes cohérents, avec accord).

## Déroulement d’une mesure

1. Participant au repos (assis, ~5 minutes de calme) si condition `rest`.
2. Doigt posé doucement sur caméra arrière + flash ; téléphone immobile.
3. Enregistrement ~30 secondes.
4. Relever le bpm de référence au début et à la fin ; utiliser la moyenne.
5. Optionnel : mesure `after_effort` (ex. 1 min de marche rapide) si la personne est d’accord et en forme. Ne pas proposer d’effort si elle ne se sent pas bien.

## Anonymisation

- Code `P00x` uniquement.
- Pas de visage filmé, pas de nom dans les fichiers.
- Remplir une ligne dans `data/metadata.csv` par mesure.

## Hors code (phase 0 bis)

Entretiens avec 3–4 professionnels de santé en parallèle : seuils de l’indicateur, formulations, usage terrain. Notes à déposer dans `docs/` (sans données personnelles des patients).
