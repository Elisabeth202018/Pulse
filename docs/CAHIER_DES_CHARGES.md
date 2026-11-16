# Cahier des charges — Projet Pulse

> Document de référence du projet (extrait du PDF). À tenir à jour avec le dépôt.

---

Cahier des charges — Projet Pulse (nom de code
provisoire)

   Ce document est le contexte de référence du projet. Il est destiné à être lu par Cursor (assistant de
   code) et par la développeuse.
   À placer dans le dépôt : docs/CAHIER_DES_CHARGES.md .
   Le nom définitif du projet sera choisi plus tard ; le nom de code n'a aucune importance technique.




0. Instructions pour l'assistant de code (Cursor)

Avant d'écrire du code :

 1. Résume en quelques lignes ta compréhension du projet et de la tâche demandée.
 2. Liste les hypothèses que tu fais et pose les questions bloquantes.
 3. Propose un plan court, puis code une seule tâche à la fois (voir le backlog, section 14).

Règles permanentes :

    Ce projet n'est pas un dispositif médical. Aucun texte affiché à l'utilisateur ne doit poser un
    diagnostic, prédire une maladie ou rassurer de façon absolue (voir section 9, formulations
    interdites).
    Tous les seuils (bpm, qualité du signal, délais) sont des constantes dans un fichier de
    configuration, jamais écrits en dur dans la logique.

    Ne jamais afficher un bpm issu d'un signal de qualité insuffisante.
    Les données restent sur le téléphone par défaut. Pas de serveur, pas d'envoi réseau dans le MVP.
    N'ajoute pas de dépendance lourde sans la justifier et demander confirmation.
    Ne supprime pas de fichiers existants sans demander.
    La développeuse est étudiante et apprend en construisant : explique brièvement les choix
    importants, commente le code de façon simple, privilégie des solutions lisibles plutôt que
    sophistiquées.




1. Résumé du projet

Application Android gratuite et hors-ligne qui estime le rythme cardiaque à partir de la caméra arrière
et du flash du téléphone (l'utilisateur pose le doigt sur l'objectif), enregistre un historique local sur 30
jours, et affiche un indicateur de suivi (vert / orange / rouge) qui aide la personne à décider si elle doit

consulter un professionnel de santé. Dans une phase ultérieure, un agent conversationnel (français,
anglais, pidgin) pose quelques questions de contexte après chaque mesure.

Positionnement visé : outil de pré-dépistage et de sensibilisation pour agents de santé
communautaires, centres de santé et grand public, au Cameroun.


2. Contexte et problème

    Le suivi régulier du rythme cardiaque est peu accessible : les montres connectées sont chères, et
    beaucoup de gens n'ont qu'un téléphone Android d'entrée de gamme.
    Les capteurs optiques (PPG) sont connus pour être moins fiables sur les peaux foncées (la
    mélanine absorbe davantage la lumière). Des travaux de recherche existent sur le sujet, mais les
    données et tests réalisés localement sont rares.
    Le projet ne prétend pas résoudre ce problème : il construit un prototype de recherche appliquée,
    documente honnêtement sa précision, et collecte un petit jeu de données local.


3. Objectifs et hors-périmètre

Objectifs

    O1. Valider en Python qu'une mesure du rythme cardiaque par caméra est suffisamment fiable
    (phase 0).
    O2. Livrer un MVP Android utilisable hors ligne (phase 1).
    O3. Documenter clairement la méthode, les résultats et les limites sur GitHub (open source).

Hors-périmètre (ne pas implémenter)

    Diagnostic médical de toute sorte.
    Prédiction d'AVC ou de risque cardiovasculaire.
    Estimation de la température (non fiable avec une caméra).
    Mesure de la tension artérielle.
    Compte utilisateur, serveur, synchronisation cloud (MVP).
    Revente ou partage de données de santé.


4. Utilisateurs cibles

  Persona                     Besoin                                  Contraintes


  Agent de santé              Faire un pré-dépistage rapide sur le    Beaucoup de personnes à
  communautaire /             terrain, décider qui orienter vers un   mesurer, peu de temps, parfois
  infirmier                   centre de santé                         pas de réseau

  Persona                         Besoin                                     Contraintes


                                                                             Téléphone bas de gamme, peu
                                  Suivre son rythme au repos et savoir
  Personne du grand public                                                   d'aisance à l'écrit, plusieurs
                                  quand consulter
                                                                             langues



5. Contraintes techniques

Appareils visés : téléphones Android d'entrée de gamme (Tecno, Infinix, Itel, Samsung Galaxy A, Xiaomi
Redmi...), typiquement 1 à 3 Go de RAM, 16 à 32 Go de stockage, processeur peu puissant, caméra et
flash de qualité variable.


  Contrainte                    Valeur cible


  Version Android
                                Android 8.0 (API 26), à ajuster selon le framework
  minimale

  Taille de l'APK               inférieure à 30 Mo si possible

  Mémoire                       pas de modèle IA lourd embarqué dans le MVP

  Réseau                        100 % fonctionnel hors ligne

                                une mesure de 30 s avec flash ne doit pas être gourmande ; le flash est éteint
  Batterie
                                dès la fin

  Langues                       français (MVP), anglais, puis pidgin (phase 2)


Conséquence : toute fonction de mesure doit être testée sur au moins 3 modèles différents de
téléphones, car la caméra, le flash, la compression vidéo et la gestion de l'exposition varient beaucoup.


6. Plan par phases

                                                                                                   Durée
  Phase             Contenu
                                                                                                   indicative


                                                                                                   2à3
  0                 Validation de l'algorithme en Python
                                                                                                   semaines

  0 bis             Entretiens avec 3 à 4 professionnels de santé (en parallèle)                   en parallèle

                                                                                                   4à6
  1                 MVP de l'application (mesure, indicateur, historique)
                                                                                                   semaines

                                                                                              Durée
  Phase            Contenu
                                                                                              indicative


                                                                                              3à4
  2                Agent conversationnel (règles, puis langues, puis voix)
                                                                                              semaines

                   Ouverture (alerte à un proche avec consentement, orientation vers un
  3                                                                                           à décider
                   centre de santé, mode agent de santé)

                                                                                              1à2
  Finalisation     Tests, démo vidéo, documentation GitHub
                                                                                              semaines




7. Phase 0 — Validation de l'algorithme (Python)

7.1 Objectif

Savoir, avant de construire l'app, si la mesure par caméra est assez fiable sur le public visé.


7.2 Protocole de collecte

      Au moins 30 participants volontaires, avec consentement (oral ou écrit) de chacun, sur des teintes
      de peau variées, avec au moins 3 modèles de téléphones.

      Mesure de 30 secondes : doigt posé doucement sur la caméra arrière et le flash, téléphone
      immobile (posé sur une table, main appuyée).
      Pour chaque participant : une mesure au repos (assis, 5 minutes de calme), et si la personne est
      d'accord et en bonne forme, une mesure après un effort léger (par exemple 1 minute de marche
      rapide) afin de couvrir plusieurs niveaux de rythme. Ne pas proposer d'effort à une personne qui ne
      se sent pas bien.
      Appareil de référence : oxymètre de pouls au doigt (ou tensiomètre de pharmacie qui affiche le
      pouls). Relever la valeur de référence au début et à la fin de la mesure, et utiliser la moyenne.
      Aucune donnée nominative : chaque participant reçoit un code (P001, P002...). Pas de visage filmé,
      pas de nom dans les fichiers.


7.3 Format des données

Un fichier data/metadata.csv avec :


  Colonne                               Description


  participant_id                        code anonyme (P001...)

  date                                  date de la mesure

  Colonne                             Description


  device_model                        modèle du téléphone

  android_version                     version d'Android

  age_range                           tranche d'âge (optionnel)

                                      groupe de teinte de peau noté de façon cohérente (par exemple clair /
  skin_tone_group
                                      moyen / foncé), avec l'accord du participant

  condition                            rest ou after_effort


  reference_device                    modèle de l'appareil de référence

  reference_bpm_start,
                                      valeurs relevées
  reference_bpm_end

  video_filename                      nom du fichier vidéo ou CSV du signal

  notes                               problèmes éventuels (doigt qui a bougé, lumière...)


Limite connue : filmer avec l'application caméra du téléphone applique une compression vidéo qui peut
dégrader légèrement le signal. On commence ainsi pour aller vite, puis la première version de
l'application enregistrera directement, pour chaque image, un horodatage et les moyennes des canaux
R, G, B dans un fichier CSV ( timestamp_ms,mean_r,mean_g,mean_b ). Ce CSV devient le format de
référence.


7.4 Traitement et livrables

    Un notebook Jupyter notebooks/01_ppg_validation.ipynb reproductible (HeartPy ou NeuroKit2,
    NumPy, SciPy, pandas, Matplotlib).
    Un tableau comparatif mesure vs référence, avec : erreur moyenne absolue (MAE, en bpm), erreur
    relative moyenne (MAPE, en %), taux de mesures rejetées pour mauvaise qualité, résultats par
    groupe de teinte de peau et par modèle de téléphone.

    Un graphique mesure vs référence (nuage de points) et une courte analyse des cas d'échec.
    Le dataset public PPG-DaLiA peut servir à s'entraîner au traitement du signal, mais il vient d'un
    capteur au poignet : il ne remplace pas la validation avec une caméra de téléphone.


7.5 Critère de décision

Objectif indicatif : erreur moyenne inférieure à 5 bpm ou erreur relative moyenne inférieure à 10 %, avec
un taux de rejet raisonnable. Si ce n'est pas atteint, améliorer l'algorithme (ou limiter les conditions
d'usage) avant de passer à la phase 1. Les résultats, bons ou mauvais, sont publiés tels quels.

8. Algorithme de mesure (spécification)

Toutes les valeurs numériques ci-dessous sont des valeurs initiales à calibrer en phase 0, et vivent
dans un fichier de configuration ( config.py en Python, ppg_config.dart dans l'app).

Entrée : une série d'images (ou le CSV) avec, pour chaque image, un horodatage t en ms et les
moyennes R , G , B sur une zone centrale (environ 50 % de la surface de l'image).

Étapes

 1. Acquisition : 30 secondes, flash allumé. Verrouiller l'exposition et la balance des blancs après
    quelques instants si le framework le permet (sinon le signal est déformé par l'auto-exposition).
 2. Rejet du début : ignorer les 5 premières secondes (stabilisation du doigt et de l'exposition). Il reste
    environ 25 secondes analysées.
 3. Choix du canal : canal rouge par défaut (comparer avec le vert en phase 0).
 4. Rééchantillonnage : les téléphones ne délivrent pas les images à intervalle régulier. Utiliser les vrais
    horodatages et rééchantillonner à 30 Hz par interpolation linéaire.
 5. Prétraitement : retirer la tendance lente (detrend), puis filtre passe-bande de Butterworth (ordre 3)
    entre 0,7 Hz et 3,5 Hz (environ 42 à 210 bpm). Le traitement se fait après la capture, donc un filtre
    à phase nulle est possible.
 6. Détection des pics : distance minimale entre deux pics d'environ 0,3 s, seuil de proéminence relatif
    à l'écart-type du signal.
 7. Intervalles entre battements (IBI) : rejeter ceux hors de 0,3 à 1,5 s, et ceux qui s'écartent de plus de
    25 % de la médiane.
 8. Rythme : bpm = 60 / médiane(IBI) , arrondi à l'entier.
 9. Estimation de contrôle : estimer le rythme aussi par FFT (pic dominant dans la bande 0,7 à 3,5 Hz).
    Si les deux estimations diffèrent de plus de 5 bpm, la confiance baisse.
10. Indice de qualité du signal (SQI, entre 0 et 1) : combine (a) le nombre de battements valides
    (minimum 20), (b) la part d'IBI conservés (minimum 80 %), (c) l'accord entre estimation par pics et
    par FFT, (d) l'absence de saturation (valeur moyenne du canal ni proche du noir, ni proche de la
    saturation, par exemple en dehors de 50 à 250 sur 255).
11. Décision : si SQI < SQI_MIN (valeur initiale 0,6), la mesure est rejetée et l'app demande de
    recommencer. Aucun bpm n'est affiché.

Version de l'algorithme : stocker algorithm_version avec chaque mesure pour pouvoir comparer les
résultats après chaque amélioration.

Port vers l'application : l'algorithme est d'abord écrit et validé en Python, puis réimplémenté dans l'app.
Pour s'assurer que les deux donnent le même résultat, exporter quelques CSV d'exemple avec le bpm
attendu ( tests/fixtures/ ) et vérifier par tests unitaires que l'implémentation de l'app retrouve les
mêmes valeurs (tolérance à définir, par exemple 1 bpm).

9. Indicateur de suivi (vert / orange / rouge)

C'est une aide à la décision « dois-je consulter ? », pas un diagnostic.


9.1 Règles

    Seules les mesures au repos comptent pour l'indicateur. Avant chaque mesure, l'app demande : «
    Êtes-vous au repos depuis au moins 5 minutes ? » (oui = rest , non = after_effort ). Une mesure
    après effort est enregistrée mais n'influence pas la couleur.
    Plage de référence au repos (indicative, adulte) : 60 à 100 bpm. À faire valider par un
    professionnel de santé.

    Ligne de base personnelle : médiane des mesures au repos de la personne, disponible à partir de 7
    mesures valides réparties sur au moins 3 jours.


  Couleur    Conditions (valeurs initiales, configurables)


  Vert       Mesure au repos dans la plage de référence, et proche de la ligne de base si elle existe

             Au moins 2 mesures au repos hors plage sur 7 jours, ou (si ligne de base) écart de plus de 20
  Orange
             % par rapport à la ligne de base sur 2 mesures de la semaine

             2 mesures valides au repos consécutives (espacées d'au moins 5 minutes) en dessous de 40
  Rouge
             bpm ou au-dessus de 130 bpm, ou un symptôme grave signalé par l'utilisateur


    Symptômes graves (cases à cocher après la mesure, étape optionnelle mais proposée) : douleur à
    la poitrine, malaise ou évanouissement, essoufflement inhabituel, palpitations fortes. Si l'un est
    coché, le résultat passe à rouge quel que soit le bpm.
    Jamais de rouge sur une mesure isolée sans symptôme.
    Une mesure rejetée (qualité insuffisante) n'a pas de couleur et ne compte pas.


9.2 Textes de résultat (français)

    Vert : « Votre rythme est dans la plage de référence. Continuez à vous mesurer régulièrement. Cet
    outil ne remplace pas un avis médical. »
    Orange : « Votre rythme présente des variations inhabituelles cette semaine. Pensez à en parler à
    un infirmier ou à un médecin. »
    Rouge : « Votre rythme ou vos symptômes demandent une attention rapide. Consultez un
    professionnel de santé dès que possible. En cas de malaise, appelez les secours. »
    Mesure rejetée : « Mesure impossible. Posez le doigt doucement, sans appuyer fort, et ne bougez
    pas. Recommencez. »


9.3 Formulations interdites

Ne jamais écrire : « tout va bien », « aucun risque », « vous êtes en bonne santé », « diagnostic », «
risque d'AVC », « maladie cardiaque détectée ». La couleur ne doit jamais être le seul moyen de
transmettre l'information : toujours ajouter une icône et un texte.




10. Spécification de l'application (phase 1)

10.1 Écrans


  Écran              Contenu                                              Remarques


                     Présentation en 2 écrans simples, avertissement      Obligatoire avant d'utiliser l'app ;
  Premier
                     « outil de suivi, pas un diagnostic »,               version du consentement
  lancement
                     consentement                                         enregistrée

                     Gros bouton « Mesurer », dernière mesure avec
  Accueil                                                                 Une action principale par écran
                     sa couleur, accès à l'historique et aux paramètres

  Question de
                     « Au repos depuis 5 minutes ? » oui / non            Avant la mesure
  contexte

  Guide de           Illustration simple : où poser le doigt, appuyer
                                                                          Peu de texte
  mesure             doucement, ne pas bouger

  Mesure en          Compte à rebours de 30 s, barre de progression,      Flash allumé, éteint dès la fin ou
  cours              courbe du signal en direct (optionnel)               en cas d'annulation

                     bpm, couleur + icône + texte (section 9.2), étape
                                                                          Rappel permanent : ne remplace
  Résultat           optionnelle des symptômes, bouton «
                                                                          pas un avis médical
                     Recommencer » et « Terminer »

                     Liste des mesures des 30 derniers jours,
  Historique
                     graphique simple, filtre repos / effort

  Détail d'une
                     Date, bpm, contexte, couleur, qualité
  mesure

                     Langue, suppression de toutes les données,
  Paramètres                                                              Suppression avec confirmation
                     export CSV, page « À propos et limites »



10.2 Exigences d'interface

    Grande police, bons contrastes, boutons larges (utilisation en plein soleil, doigts de tous âges).
    Une action par écran, icônes et couleurs plutôt que longs textes.

    Textes dans des fichiers de traduction séparés (jamais en dur dans les widgets). Prévoir une
    couche d'internationalisation extensible : le pidgin camerounais n'a pas toujours de code de langue
    standard dans les frameworks.
    Fonctionne en mode portrait uniquement (simplicité).


10.2 bis Palette de couleurs

Principe : une interface bleue, sobre et calme, qui inspire confiance pour un outil de santé, et qui laisse
le vert, l'orange et le rouge réservés à l'indicateur de suivi. Ces trois couleurs ne doivent jamais servir
de décor.

Couleurs de l'interface


  Rôle                                                                     Nom dans le code      Valeur


  Primaire (boutons, en-têtes, anneau de progression, courbe du signal)     primary              #1F4E79


  Primaire foncé (bouton pressé)                                            primaryDark          #163A5A


  Primaire clair (cartes, sélection)                                        primaryLight         #DCE9F5


  Fond de l'écran                                                           background           #F7F9FB


  Surface (cartes, champs)                                                  surface              #FFFFFF


  Texte principal                                                           textPrimary          #172B3C


  Texte secondaire                                                          textSecondary        #5B6B7A


  Bordures                                                                  border               #D5DEE6



Couleurs des statuts


                                        Fond de
  Statut      Couleur                                    Icône     Couleur du texte dessus
                                        carte


               statusGreen
  Vert                                   #E8F5E9         ✓         blanc
               #2E7D32


               statusOrange                                        foncé #172B3C (le blanc n'est pas
  Orange                                 #FFF3E0         ⚠
               #E08600                                             assez lisible sur l'orange)

               statusRed
  Rouge                                  #FDECEA         !         blanc
               #C62828



Règles d'utilisation

      La couleur ne porte jamais le sens seule : chaque statut s'affiche toujours avec icône + texte +
      couleur.

      Pas d'icône de cœur rouge dans l'application (risque de confusion avec une alerte) : utiliser un
      cœur ou une pulsation en bleu primaire.
      La courbe du signal, la barre de progression et les graphiques de l'historique restent en bleu
      primaire, jamais en vert, orange ou rouge.
      Pas de mode sombre dans le MVP.
      Contraste visé : niveau AA au minimum (texte normal à 4,5:1 ou plus). Les combinaisons ci-dessus
      sont prévues pour l'atteindre ; vérifier avec un outil de contraste, puis sur de vrais téléphones en
      plein soleil.
      Toutes les couleurs sont définies à un seul endroit, dans lib/core/theme/app_colors.dart , et
      utilisées par tout le reste de l'app via le thème. Ne jamais écrire une valeur de couleur directement
      dans un écran.
      Les couleurs et motifs à identité locale (inspirés des tissus et formes traditionnelles) seront définis
      plus tard, en tons neutres, sur l'écran d'accueil et les écrans vides, sans toucher aux couleurs de
      statut.


10.3 Gestion des erreurs

      Flash indisponible ou permission caméra refusée : message clair qui explique pourquoi la caméra
      est nécessaire.
      Doigt retiré pendant la mesure (la moyenne de la zone change brutalement) : arrêt de la mesure et
      message de relance.
      Application mise en arrière-plan : arrêt immédiat de la mesure et extinction du flash.
      Qualité du signal insuffisante : voir section 8, étape 11.


10.4 Modèle de données (SQLite local)

measurements


 Champ                         Type                           Description


 id                            INTEGER, clé primaire

 created_at                    TEXT (ISO 8601)                date et heure

 bpm                           INTEGER                        rythme estimé

 sqi                           REAL                           indice de qualité

 duration_s                    INTEGER                        durée de la mesure

 context                       TEXT                            rest , after_effort ou unknown

  Champ                      Type                           Description


  status                     TEXT                            green , orange , red


  symptoms                   TEXT                           liste JSON des symptômes cochés

  algorithm_version          TEXT

  device_model               TEXT


consents : id , version , accepted_at .
settings : key , value (langue, etc.).

Les mesures rejetées ne sont pas enregistrées dans l'historique (seulement comptées pour les
statistiques de la phase 0 si le mode de collecte est activé). Le signal brut n'est pas conservé par
défaut ; un mode « collecte » désactivé par défaut permet d'enregistrer le CSV du signal pour la
validation.




11. Agent conversationnel (phase 2)

    Déclenchement : après un résultat valide.

    Principe : arbre de règles simple en premier. Pas de modèle de langage dans la première version.

    Questions (3 maximum par mesure, choisies dans une banque) : sommeil de la nuit passée, maux
    de tête, fatigue, stress, consommation d'eau, activité du jour.
    Sortie : un conseil court et prudent (repos, hydratation, en parler à un professionnel si la situation
    se répète). Aucun conseil médical précis, aucun médicament, aucun diagnostic.
    Historique : les réponses sont stockées localement avec la mesure, sur 30 jours, pour repérer des
    tendances (par exemple « rythme plus élevé les jours de mauvais sommeil »), présentées comme
    de simples observations.
    Fichiers de dialogue : questions, réponses et conseils dans des fichiers JSON par langue, séparés
    du code.
    Langues : français, anglais, puis pidgin. La synthèse vocale hors ligne existe en général pour le
    français et l'anglais, probablement pas pour le pidgin : le pidgin sera en texte au départ. Les textes
    en pidgin doivent être relus par un locuteur natif.
    Sécurité : si l'utilisateur signale un symptôme grave, l'agent renvoie vers le message rouge (section
    9.2) et n'essaie pas de gérer la situation seul.


12. Phase 3 — pistes (optionnelles, à décider plus tard)

    Alerte SMS à un proche : uniquement avec consentement explicite préalable, contact choisi par
    l'utilisateur, message neutre.

    Orientation vers un centre de santé proche (liste locale hors ligne).
    Mode agent de santé : suivi de plusieurs personnes avec leur accord.




13. Architecture et conventions de code

13.1 Choix technique (à confirmer après la phase 0)

    Option A, recommandée par défaut : Flutter avec le plugin camera (flux d'images + contrôle du
    flash).
    Option B : Android natif (Kotlin + CameraX), contrôle de la caméra plus fin, apprentissage plus
    long.
    Kivy est déconseillé : accès difficile au flash et au flux d'images.
    Stockage : SQLite local. Pas de serveur dans le MVP.


13.1 bis Outils, langages et bibliothèques

Logiciels à installer


  Outil                                                          Rôle


  Cursor                                                         éditeur de code avec assistant IA

                                                                 historique du code, dépôt public open
  Git et compte GitHub
                                                                 source

  Python 3 + Jupyter (JupyterLab ou extension Jupyter dans
                                                                 phase 0 : analyse du signal
  Cursor)

  Flutter SDK (inclut Dart)                                      développement de l'application

                                                                 SDK Android, outils de compilation,
  Android Studio
                                                                 émulateur

  Figma (optionnel)                                              maquettes des écrans avant de les coder


Matériel

    Un ou plusieurs téléphones Android physiques, avec le mode développeur et le débogage USB
    activés. L'émulateur ne reproduit pas correctement la caméra et le flash : les tests de mesure se
    font sur de vrais téléphones.
    Un oxymètre de pouls ou un tensiomètre de pharmacie comme appareil de référence.

Bibliothèques Python (phase 0) : numpy , scipy , pandas , matplotlib , heartpy ou neurokit2 ,
jupyter .

Packages Flutter (phase 1) : camera (flux d'images et flash), sqflite (base SQLite locale),
path_provider (accès aux fichiers), permission_handler (permission caméra), fl_chart
(graphiques), intl et flutter_localizations (traductions), share_plus (export CSV). Utiliser les
versions stables actuelles et vérifier la compatibilité avant d'ajouter un package.


13.2 Organisation du code (Flutter)

Architecture en trois couches : présentation (écrans), domaine (règles, algorithme), données (SQLite).

Le traitement du signal est un module en Dart pur, sans dépendance à Flutter, pour pouvoir être testé
facilement et comparé à l'implémentation Python. Les bibliothèques de traitement du signal sont
limitées en Dart : le filtre passe-bande et la détection de pics devront probablement être implémentés à
la main, d'où l'importance des tests de comparaison avec Python. Si cela devient trop coûteux, c'est un
argument pour l'option B.


13.3 Structure du dépôt


  /docs                      cahier des charges, protocole de collecte, notes de validation
  /notebooks                 phase 0 : analyse Python
  /data                      données anonymisées (jamais de données nominatives)
  /app                       application mobile
    /lib
         /core               configuration, thème, traductions, base de données
         /features
           /onboarding       consentement, présentation
           /measurement      capture caméra, algorithme PPG, écran de mesure et de résultat
           /history          historique et détail
           /settings         langue, suppression, export, à propos
           /assistant        agent conversationnel (phase 2)
    /test                    tests unitaires et de widgets
  /tests/fixtures            CSV d'exemple avec bpm attendu
  README.md                  présentation, limites, avertissements



13.4 Conventions

    Noms de variables, fonctions et fichiers en anglais ; commentaires et textes affichés en français
    (via fichiers de traduction).
    Un commit Git par tâche terminée, message court et clair.
    Pas de clé secrète ni de donnée personnelle dans le dépôt.
    Chaque fonction du domaine (algorithme, règles de couleur) a des tests unitaires.




14. Backlog de tâches pour Cursor (ordre recommandé)

Phase 0 (Python)


 #      Tâche                                                             Critère d'acceptation


 T0-    Créer le dépôt, le README, la structure de dossiers,              Dépôt propre avec les dossiers de la
 1      .cursorrules                                                      section 13.3

 T0-    Notebook : charger une vidéo (ou CSV) et extraire la
                                                                          Courbe du canal rouge affichée
 2      moyenne R, G, B par image avec horodatage

 T0-                                                                      Signal filtré affiché, battements
        Rééchantillonnage à 30 Hz, detrend, filtre passe-bande
 3                                                                        visibles

 T0-    Détection des pics, calcul des IBI et du bpm, estimation          bpm affiché pour un enregistrement
 4      FFT de contrôle                                                   d'essai

 T0-                                                                      Mesures volontairement mauvaises
        Calcul du SQI et rejet des mesures de mauvaise qualité
 5                                                                        (doigt qui bouge) rejetées

 T0-    Script de comparaison avec la référence : MAE, MAPE,              Tableau et graphique générés à partir
 6      résultats par teinte de peau et par téléphone                     de metadata.csv



Phase 1 (application)


 #      Tâche                                                  Critère d'acceptation


 T1-    Squelette de l'app, navigation, thème, système
                                                               L'app démarre et navigue entre écrans vides
 1      de traduction (fr)

 T1-                                                           Impossible d'accéder à l'accueil sans
        Écran de consentement et d'avertissement
 2                                                             consentement ; version enregistrée

        Accès à la caméra arrière et au flash,
 T1-                                                           Flash allumé pendant la mesure, éteint à la
        permission, extinction du flash en toute
 3                                                             fin, à l'annulation et en arrière-plan
        situation

 T1-    Capture des moyennes R, G, B par image avec            CSV généré, utilisable par le notebook
 4      horodatage, export CSV (mode collecte)                 Python

                                                               Tests de comparaison avec
 T1-    Implémentation de l'algorithme (section 8) en
                                                               tests/fixtures réussis (tolérance
 5      Dart pur
                                                               définie)

 T1-    Écrans de guide, de mesure (compte à rebours)          Une mesure complète de 30 s fonctionne
 6      et de résultat                                         hors ligne

  #           Tâche                                           Critère d'acceptation


  T1-                                                         Tests unitaires couvrant vert, orange, rouge,
              Règles de l'indicateur et textes (section 9)
  7                                                           symptômes et mesure rejetée

  T1-         Base SQLite et historique sur 30 jours avec     Mesures conservées après fermeture de
  8           graphique                                       l'app, purge au-delà de 30 jours

  T1-         Paramètres : langue, suppression des données,   La suppression efface bien toutes les
  9           export CSV, page « À propos et limites »        données

  T1-         Tests manuels sur 3 modèles de téléphones,      Rapport de test avec modèle, version
  10          correction des problèmes                        Android, résultat



Phase 2

Banque de questions et arbre de règles, fichiers de dialogue fr/en, puis pidgin en texte, puis voix (fr/en).




15. Tests et critères d'acceptation du MVP

      Une mesure complète en 30 secondes, sans connexion internet.
      Une mesure de mauvaise qualité est détectée et refusée, sans afficher de bpm.
      L'historique des 30 derniers jours est consultable et persiste après redémarrage.
      Les limites du projet sont visibles dans l'app (consentement, écran de résultat, « À propos »).
      Les tests unitaires de l'algorithme et des règles de couleur passent.
      L'app a été essayée sur au moins 3 modèles de téléphones différents.
      Le README documente la méthode, les résultats de validation et les limites, sans promesse
      médicale.


16. Données personnelles et éthique

      Consentement explicite, en langage simple, au premier lancement.
      Données stockées localement ; suppression possible à tout moment depuis l'app.
      Aucune revente de données de santé ; aucun partage sans consentement explicite.
      Pour la collecte de la phase 0 : consentement de chaque participant, données anonymisées, pas de
      visage ni de nom dans les fichiers.
      Respecter la législation camerounaise sur la protection des données personnelles.
      Les seuils médicaux (section 9) doivent être validés par un professionnel de santé avant tout usage
      réel.

17. Risques

 Risque                                               Réponse


 Précision insuffisante sur certaines teintes de      Phase 0, comparaison avec un appareil de référence,
 peau ou certains téléphones                          résultats publiés tels quels

                                                      Formulations non rassurantes, rappels de consultation,
 Fausse impression de sécurité
                                                      validation des seuils par un professionnel

 Différences entre téléphones (caméra, flash,         Tests sur plusieurs modèles, verrouillage de l'exposition
 exposition)                                          si possible, contrôle de qualité strict

 Réimplémentation de l'algorithme en Dart             Tests de comparaison avec Python ; option B (Kotlin) si
 difficile                                            nécessaire

                                                      Phases courtes, MVP minimal, agent conversationnel
 Charge de travail avec les études
                                                      reporté en phase 2

                                                      Présenter le projet comme un prototype de recherche
 Échantillon trop petit
                                                      appliquée



18. Glossaire

   bpm : battements par minute.

   PPG (photopléthysmographie) : mesure des variations de lumière réfléchie par la peau, liées au
   passage du sang à chaque battement.
   IBI : intervalle entre deux battements consécutifs.

   SQI : indice de qualité du signal.

   MAE / MAPE : erreur absolue moyenne / erreur relative moyenne par rapport à la référence.

   Ligne de base : valeur habituelle de la personne, calculée sur ses propres mesures au repos.



19. Questions ouvertes (à trancher en cours de route)

1. Nom définitif du projet (inspiré d'une langue locale, à vérifier avec un locuteur).
2. Choix final Flutter ou Kotlin, après la phase 0.
3. Validation des seuils de la section 9 par un professionnel de santé.
4. Modalités exactes de la collecte (lieu, matériel de référence, consentement écrit ou oral).
5. Orientation après le prototype : bourses et concours, partenariat avec un centre de santé, usage par
   agents de santé communautaires.
