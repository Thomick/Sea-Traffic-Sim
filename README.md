# Sea-Traffic-Sim
Code source du projet de TIPE de Thomas MICHEL : Stratégie et simulation d'évitement de collision en mer
Ce projet comprend la simulation d'un environnement de navigation (implémenté par une boucle de mise à jour d'instances de classes héritant de "boat"), ainsi que différentes stratégies d'évitement de collision.

###Le projet est actuellement arrêté suite à l’annulation de l’épreuve de TIPE en raison de crise sanitaire. Le code n’est en l’état pas fonctionnel (nécessite des modification de code source pour passer d’un algorithme à l’autre ou bien changer la configuration des bateaux) mais sera mis en ordre dès que possible.

Voici quelques indications sur les différents fichiers :
Caselauncher.py permet de visualiser certaines configurations préenregistrées
Boats.py implémente l’ensemble des bateaux possibles (chaque bateau correspond à une stratégie)
Simdisplay.py gère l’affichage
RLStrategie.py implémente l’algorithme de double DQN appliqué au problème considéré
Boatbuilder.py crée des instances de bateau à partir de fichiers de configuration
Les autres fichiers sont essentiellement des fonctions utilitaires ou des fichiers relatifs à la gestion de projet de TIPE

Les algorithmes actuellement implémentés sont :
- Algorithme simple de contournement (Dit de "réaction" lorsqu’une collision prochaine es détectée)
- Algorithme du "champ de vecteurs"
- Recherche locale de minimum (optimisation locale des trajectoires par communication entre les bateaux)
- Apprentissage par renforcement (Non entraîné ici)

Les stratégies sont largement inspirées des articles suivants
- R. SKJONG, K. M. MJELDE : Optimal evasive manoeuvre for a ship in an environment of a fixed
installations and other ships : 1982, Modeling, Identification and Control , vol.3, no. 4, 211-222
- D.-G. KIM, K. HIRAYAMA, T. OKIMOTO : Ship Collision Avoidance by Distributed Tabu Search :
2015, TransNav: International Journal on Marine Navigation and Safety of Sea,
doi:10.12716/1001.09.01.03
- Y. F. CHEN, M. LIU, M. EVERETT, J. P. HOW : Decentralized Non-communicating Multiagent
Collision Avoidance with Deep Reinforcement Learning : 2016, arXiv:1609.07845v2 [cs.MA]
- Y. Z. XUE, D. CLELLAND, B.S. LEE, D.F. HAN : Automatic simulation of ship navigation : 2011,
Ocean Engineering
- S.-M. LEE, K.-Y KWON, J. JOH : A fuzzy logic for autonomous navigation of marine vehicle
satisfying COLREG guidelines : 2004, International Journal of Control Automation and Systems