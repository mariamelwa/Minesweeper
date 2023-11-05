# Date : 21 décembre 2022
# Auteures: Mariam Elwa et Gabrielle Rainville


## PARAMÈTRES

nombreMines = 4
largeur = 8
hauteur = 5

premierClic = None # contiendra le nombre de la case de la première entrée
minePerdante = None # contiendra le nombre de la case de la mine perdante

casesMines = [] # les cases contenant des mines seront les entrées
casesDevoilees = [] # les cases dévoilées seront les entrées
casesMarquees = [] # les cases marquées d'un drapeau seront les entrées
grilleReponse = [] # grille contenant les attributs de chaque case


## PARTIE HTML

main = document.querySelector('#main')
main.innerHTML = """
    <link rel="preload" href="http://codeboot.org/images/minesweeper/0.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/1.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/2.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/3.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/4.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/5.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/6.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/7.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/8.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/blank\
    .png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/flag.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/mine.png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/mine-red.\
    png">
    <link rel="preload" href="http://codeboot.org/images/minesweeper/mine-\
    red-x.png">

      <style>
      #main table {
        border: 1px solid black;
        margin: 10px;
      }
      #main table td {
        width: 30px;
        height: 30px;
        border: none;
      }
      </style>
      """

# La fonction idTuile prend un paramètre:
# - n: un entier qui représente l'index d'une case
# La fonction retourne l'identifiant HTML de l'élément représentant cette
# case dans le DOM. (source: tictactoe.py)
def idTuile(n):
    return "tuile" + str(n)

# testIdTuile est la fonction de tests pour la fonction idTuile
def testIdTuile():
    assert idTuile(2) == "tuile2"
    assert idTuile(0) == "tuile0"
    # deux chiffres
    assert idTuile(10) == "tuile10"


# La fonction choixImage prend un paramètre:
# - nomImage: un texte qui est le nom du fichier de l'image (ex:1, 2, blank,
# flag, etc).
# Elle retourne un texte qui est la balise de l'image qui a comme nom nomImage.
def choixImage(nomImage):
    return '<img src="http://codeboot.org/images/minesweeper/' + \
        str(nomImage) + '.png">'

# testChoixImage est la fonction de tests pour la fonction choixImage
def testChoixImage():
    assert choixImage('') == '<img src="http://codeboot.org/images/minesweeper/.png">'
    # chiffre
    assert choixImage('0') == '<img src="http://codeboot.org/images/minesweeper/0.png">'
    # lettres
    assert choixImage('mine') == '<img src="http://codeboot.org/images/minesweeper/mine.png">'


# La fonction element prend un paramètre:
# - index: un entier qui est l'index d'une case
# Elle retourne la fonction document.querySelector appliquée à la case index.
# (source: tictactoe.py)
def element(index):
    return document.querySelector('#' + idTuile(index))

# testElement est la fonction de tests pour la fonction element
def testElement():
    # un chiffre
    assert element(1) == document.querySelector('#tuile1')
    # deux chiffres
    assert element(10) == document.querySelector('#tuile10')
    # cas limite
    assert element(0) == document.querySelector('#tuile1')


# La fonction genererRangeeHTML prend deux paramètre:
# - n: un entier >= 0
# - debut: un entier >= 0
# Elle génère une rangée (un texte) d'une table HTML longueur 'n' et
# dont l'identificateur de la première case commence à 'debut'.
# (source: tictactoe.py)
def genererRangeeHTML(n, debut):
    rangees = []
    for i in range(n):
        numero = str(i + debut)
        onclick = 'onclick="clic(' + numero + ')"' # événement d'un clic
        id = 'id="' + idTuile(numero) + '"' # identification de la case
        img = 'img src=' + 'http://codeboot.org/images/minesweeper/blank.png'
        rangees.append("<td " + onclick + " " + id + "><" + img + "></td>")
    return "<tr>" + '\n'.join(rangees) + "<tr>"

# testGenererRangeeHTML est la fonction de tests pour la fonction
# genererRangeeHTML
def testGenererRangeeHTML():
    assert genererRangeeHTML(0,0) == '<tr><tr>'
    assert genererRangeeHTML(2,1) == '<tr><td onclick="clic(1)" id="tuile1"><img src=http://codeboot.org/images/minesweeper/blank.png></td>\n<td onclick="clic(2)" id="tuile2"><img src=http://codeboot.org/images/minesweeper/blank.png></td><tr>'


# La fonction genererGrilleHTML prend deux paramètre:
# - n: un entier
# - m: un entier
# Elle génère le HTML (un texte) d'une table de 'n' colonnes et 'm' lignes.
# (source: tictactoe.py)
def genererGrilleHTML(n, m):
    rangees = []
    for i in range(m):
        rangees.append(genererRangeeHTML(n, i * n))
    return "<table>" + '\n'.join(rangees) + '</table>'

# testGenererGrilleHTML est la fonction de tests pour la fonction
# genererGrilleHTML
def testGenererGrilleHTML():
    assert genererGrilleHTML(0,0) == '<table></table>'
    assert genererGrilleHTML(2,1) == '<table><tr><td onclick="clic(0)" id="tuile0"><img src=http://codeboot.org/images/minesweeper/blank.png></td>\n<td onclick="clic(1)" id="tuile1"><img src=http://codeboot.org/images/minesweeper/blank.png></td><tr></table>'


# La procédure mettreAJourHTML change les balises d'image des cases qui ont été
# dévoilées. Elle remplace donc les images 'blank' pour les images des nombres,
# mines ou drapeaux approprié selon la grille de réponse.
# (inspiré de: tictactoe.py)
def mettreAJourHTML():
    global minePerdante

    # on modifie seulement les images des cases dévoilées
    for case in casesDevoilees:
        # si la case est marquée, on change l'image pour un drapeau
        if case in casesMarquees:
            element(case).innerHTML = choixImage('flag')

        # si la case est la mine perdante, on change l'image pour la mine rouge
        elif case in casesMines and case == minePerdante:
            element(case).innerHTML = choixImage('mine-red')

        # si la case est une mine non dévoilée, on change l'image pour la mine
        elif case in casesMines:
                element(case).innerHTML = choixImage('mine')

        else: # c'est une case avec un numéro
            numero = grilleReponse[case]
            # on affiche l'image du nombre
            element(case).innerHTML = choixImage(str(numero))

    sleep(0) # hack pour redonner le control au navigateur pour dessiner
             # le DOM


## PARTIE ÉVÉNEMENTS

# La fonction randInt prend deux paramètre:
# - debut: un entier
# - fin: un entier
# Elle retourne un nombre entier dans l'intervalle [debut,fin] dont les
# bornes sont incluses
def randInt(debut, fin):
    return math.floor(fin * random()) + debut


# La fonction melangeFisherYates prend 1 paramètre:
# - tab: un tableau dont les entrées sont quelconques
# Elle retourne tab avec ses entrées dans un ordre aléatoire.
def melangeFisherYates(tab):
    n = len(tab)
    for i in range(n - 1, 1, -1):
        j = randInt(0, i) # on choisit un nombre au hasard dans l'intervalle
        temp = tab[j]
        tab[j] = tab[i]
        tab[i] = temp # on échange les entrées i et j du tableau
    return tab


# La fonction casesMines prend deux paramètres:
# -cases: un tableau dont les entrées sont des nombres entiers
# -premierClic: un entier qui est la case où à eu lieu le premier clic
# Elle retourne un tableau de longueur nombreMines dont les entrées sont les
# cases qui contiendront des mines (la case premierClic ne s’y trouve pas).
def casesMines(cases, premierClic):

    global nombreMines
    # tableau randomisé duquel on a pris les nombreMine+1 premières entrées
    resultat = melangeFisherYates(cases)[0:nombreMines + 1]

    # si l'index du premier clic en fait partie, on le retire du tableau (on ne
    # veut pas que ça soit une mine)
    if premierClic in resultat:
        pos = resultat.index(premierClic)
        resultat.pop(pos)

    # si l'index du premier clic n'en fait pas partie, on retire le dernier
    # élément ajouté au tableau pour avoir 'nombreMines' entrées
    else:
        resultat.pop()

    return resultat


# La fonction tuilesVoisines prend un paramètre:
# - case: un entier (index d'une case)
# La fonction retourne un tableau des indices de type int des tuiles
# directement voisines (droite, gauche, bas, haut, diagonale) à la tuile donnée
# en paramètre, tel que ce tableau est d'une longueur maximale de 8. Si la case
# donnée est sur un des bords de la grille, le tableau aura moins de 8 entrées.
def tuilesVoisines(case):

    global largeur, hauteur
    resultat = []

    # voisin gauche
    if case % largeur != 0: # si on n'est pas sur la bordure gauche
        resultat.append(case - 1)

    # voisin droit
    if case % largeur != largeur - 1: # si on n'est pas sur la bordure droite
        resultat.append(case + 1)

    # voisin de haut
    if case >= largeur: # si on n'est pas sur la bordure du haut
        resultat.append(case - largeur)

    # voisin du bas
    if case < largeur * (hauteur - 1): # si on n'est pas sur la bordure du bas
        resultat.append(case + largeur)

    # Les voisins en diagonale:
    if case % largeur != 0 and case >= largeur:
        resultat.append(case - largeur - 1)
    if case % largeur != largeur - 1 and case >= largeur:
        resultat.append(case - largeur + 1)
    if case % largeur != 0 and case < largeur * (hauteur - 1):
        resultat.append(case + largeur - 1)
    if case % largeur != largeur - 1 and case < largeur * (hauteur - 1):
        resultat.append(case + largeur + 1)

    return resultat

# testTuilesVoisines est la fonction de tests pour la fonction tuilesVoisines
def testTuilesVoisines():
    # sur une grille de taille hauteur x largeur
    # case en haut à gauche, seulement 3 cases voisines
    assert tuilesVoisines(0) == [1, largeur, largeur+1]
    # case centrale
    n = int(3/2*largeur)
    assert tuilesVoisines(n) == [n-1, n+1, n-largeur, n+largeur,
    n-largeur-1, n-largeur+1, n+largeur-1, n+largeur+1]
    # case en bas à droite, seulement 3 cases voisines
    assert tuilesVoisines(largeur*hauteur-1) == [largeur*hauteur-2,
    largeur*hauteur-1-largeur, largeur*hauteur-2-largeur]


# La fonction creerGrilleReponse prend 1 paramètre:
# - premierClic, indice de la première case cliquée, de type int
# La fonction retourne un tableau dans lequel chaque entrée est le texte 'mine'
# ou nombre de type int qui représente le nombre de mines dont la case de
# chaque index est voisine. Si ce n'est pas une mine ou qu'elle
# n'est voisine d'aucune mine. La case premierClic est automatiquement mise
# à 0. Les textes et nombres sont disposés de façon aléatoire dans le tableau.
def creerGrilleReponse(premierClic):
    global largeur, hauteur, casesMines
    # tuile est un tableau des indices des cases
    tuiles=[]
    tuiles.append(list(range(largeur*hauteur)))

    # on commence avec toutes les entrées 0
    grille= largeur*hauteur*[0]

    for mine in casesMines: # pour tous les indices de cases mine
        grille[mine] = 'mine' # on remplace 0 par mine

        # liste des tuiles voisines aux mines
        tuilesAdjacentes = tuilesVoisines(mine)

        for tuile in tuilesAdjacentes:
            if grille[tuile] != 'mine':
                # si la tuile n'est pas une mine, elle est voisine à une mine
                grille[tuile] = grille[tuile] + 1

    return grille


# La fonction nombreCasesRestantes prend 2 paramètres:
# - casesMines: un tableau des indices des cases contenant des mines
# - casesDevoilees: un tableau des indices des cases dévoilées
# La fonction retourne un entier qui est le nombre de cases restantes à
# dévoiler pour gagner.
def nombreCasesRestantes(casesMines, casesDevoilees):

    global largeur, hauteur

    return largeur * hauteur - (len(casesMines) + len(casesDevoilees))

# testNombreCasesRestantes est la fonction de tests pour la fonction
# nombreCasesRestantes
def testNombreCasesRestantes():
    assert nombreCasesRestantes([],[]) == largeur*hauteur
    assert nombreCasesRestantes([1,3,7], [0,2,4,6,8]) == \
    largeur*hauteur-8
    assert nombreCasesRestantes([],[1,3,7]) == largeur*hauteur - 3
    assert nombreCasesRestantes([1,3,7],[]) == largeur*hauteur - 3


# La procédure devoilerZone prend 1 paramètres:
# -index: l'index de la case qui vient d'être cliquée
# Elle ajoute au tableau casesDevoilées les cases sans mine qui seront
# dévoilées suite au clic sur la case index.
def devoilerZone(index):
    global casesDevoilees, grilleReponse, casesMines

    # si la case est une mine ou qu'elle touche à une mine,
    # il n'y a pas d'autres cases qui seront dévoilées que celle-ci
    if index in casesMines or grilleReponse[index]!= 0:
        casesDevoilees.append(index)
        return

    # si la case est déjà dévoilée, on ne fait rien
    elif index in casesDevoilees:
        return

    # si l'index fait partie de la grille, on fait un appel récursif de la
    # fonction sur tous ses voisins
    elif 0 <= index < len(range(largeur*hauteur)):
        casesDevoilees.append(index)
        for tuile in tuilesVoisines(index):
            devoilerZone(tuile)


# La procedure finDePartie prend 1 paramètre:
# - tuile: un entier représentant une case
# Elle vérifie s'il y a eu une victoire (toutes les cases sans mine on été
# marquées ou dévoilées) ou une défaite (on a cliqué sur une mine). Elle
# affiche le résultat dans une alerte s'il y a lieu. Sinon, elle ne fait rien.
def finDePartie(tuile):
    global casesMines, casesDevoilees, casesMarquees, minePerdante

    # si on a dévoilé toutes les cases sans mine, on a gagné
    if nombreCasesRestantes(casesMines, casesDevoilees) == 0:
        casesDevoilees=list(range(largeur*hauteur)) # on dévoile la grille
        mettreAJourHTML() # on affiche tout le tableau réponse
        alert("Victoire !")

    # Si on clique sur une mine, la partie est perdue
    elif tuile in casesMines:
        casesDevoilees=list(range(largeur*hauteur)) # on dévoile la grille
        # on voudra que cette tuile soit une mine rouge
        minePerdante=tuile
        mettreAJourHTML()
        alert("Défaite !")


# La procédure clic prend un paramètre:
# -tuile: un entier qui est l'indice d'une case qui a été cliquée
# Elle traite le clic de la case (si c'est le premier clic, elle crée la
# grille de réponse). Elle fait la mise à jour du HTML et voit s'il y
# a une victoire
def clic(tuile):
    global premierClic, largeur, hauteur, casesMines, grilleReponse

    # Si on clique sur une tuile avec un drapeau qui est protegée ou qui
    # a déjà été cliquée, on ne fait rien
    if tuile in casesDevoilees or tuile in casesMarquees:
        return

    # si c'est le premier clic, on génère la grille de réponses
    if premierClic == None:
        premierClic = tuile
        cases = list(range(largeur*hauteur))
        casesMines = casesMines(cases, premierClic)
        grilleReponse = creerGrilleReponse(premierClic)

    # on ajoute aux cases dévoilées toutes les voisines de tuile
    devoilerZone(tuile)

    # on affiche l'image adéquate dans la fenêtre de jeu
    mettreAJourHTML()

    # on vérifie si c'est la fin du jeu
    finDePartie(tuile)


# La procédure clicShift prend un paramètre:
# -tuile: un entier qui est l'indice d'une case
# La procédure traite le clic précédé de shift de la case. Elle fait la mise
# à jour du HTML pour changer la case cliquée par un drapeau et vérifie s'il
# y a eu une victoire.
def clicShift(tuile):
    global casesMarquees
    casesMarquees.append(tuile)
    mettreAJourHTML()
    finDePartie(tuile) # on vérifie si ça signifie la fin de la partie


# La procédure init prend deux paramètres:
# -largeur: un entier
# -hauteur: un entier
# La procédure crée le fichier HTML d'une grille largeur x hauteur et
# fait son affichage. Elle marque le début du jeu.
def init(largeur, hauteur):
    main.innerHTML += genererGrilleHTML(largeur, hauteur)


# testInit appelle les fonctions de tests des fonctions déclarées
def testInit():
    testIdTuile()
    testChoixImage()
    testElement()
    testGenererRangeeHTML()
    testGenererGrilleHTML()
    testTuilesVoisines()
    testNombreCasesRestantes()

testInit()
init(8,5)