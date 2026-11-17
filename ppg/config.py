"""Constantes PPG — à calibrer en phase 0 (jamais en dur dans la logique métier)."""

# Zone centrale utilisée pour la moyenne R/G/B (fraction de la largeur/hauteur)
ROI_FRACTION = 0.5

# Durée cible d'une mesure (secondes)
MEASUREMENT_DURATION_S = 30

# Fréquence de rééchantillonnage (utilisée à partir de T0-3)
RESAMPLE_HZ = 30
