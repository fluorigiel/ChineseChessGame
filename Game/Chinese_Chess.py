from math import sqrt   
from random import randint  
import pygame
import time

from class_Pieces import Pieces # import mon object piece

# !!! : coordinate ou pose : (x,y) et pos (x,y) avec pos la pose dans le plateau et coordinate la coordonée de l'image/rectange

pygame.init()   # initialise pygame
ecran_dimensions = (509,560)    # (509,560) = la taille de l'image fournit  # définit la taille de mon plateau de jeu sous forme d'un tuple (x,y)
ecran_dimensions_rect = pygame.Rect(0,0,ecran_dimensions[0],ecran_dimensions[1])    # crée un rectangle à la même pose et de même taille que notre fenêtre
ecran_dimensions_2 = (809,560)                                              # définit la taille de ma fenêtre lorsque les "paramètres" sont ouvertes 
screen = pygame.display.set_mode(ecran_dimensions)  # définit la taille de ma fenêtre pygame à la taille sans les paramètres 

file_places_board = ""          # Mon répertoire : "E:/_TG2_/NSI/Projet/Jeu_echec_chinois/V_2/"

plateau = pygame.image.load(f"{file_places_board}Chessboard.png") # définit l'image de fond de mon jeu d'echec chinois (à changer la provenance)

pygame.display.set_caption('Chinese Chess')


# Le terme pos reprèsente la place dans mon échéquier tandis que le terme pose reprèsente la coordonée d'une image/pièce/... dans ma fenêtre

# couleurs :    (avec le code RGB)

white = (255,255,255)
black = (0,0,0)
gray = (51,51,51)
green = (0,128,0)
red = (255,0,0)
light_green = (0,155,0)
crimson = (220,20,60)

# Boutons / Textes :

basic_font = 'freesansbold.ttf' # police de caractère utilisé par tous mes affichages

# Joueur actif :
font_player = pygame.font.Font(basic_font, 32)  # définit la taille et la police de caractère du texte qui va afficher le tour de quel joueur c'est 
players = ["Red","Black"]   # liste contenant les couleurs des deux joueurs 
current_player = "Red"   # à changer si l'on veut que cela soit le joueur noir qui commence ou appuyer sur "s" car cela "passe le tour" (permet de changer de tour)
player_turn_text = font_player.render(current_player+"'s Turn", True, white)    # définit le texte à afficher par le bouton qui annonce le tour de quel joueur c'est
player_turn_rect = player_turn_text.get_rect()  # récupére le rectangle de notre bouton
player_turn_rect.center = (ecran_dimensions[0] + (ecran_dimensions_2[0] - ecran_dimensions[0])/2,ecran_dimensions[1]/2) # définit la pose de notre rectangle en fonction de notre fenêtre, 
                                                                                                                        # pour qu'il soit adapter peu importe la taille de la fenêtre

# Timer :
font_timer = pygame.font.Font(basic_font, 24)   # définit la taille et la police de caractère du texte qui va afficher le chronomètre de chaque joueur
total_time_red = (0, 0)     # (secondes, minutes) du joueur rouge
seconds_red = 0     # définit les secondes du joueur rouge
minutes_red = 0     # définit les minutes du joueur rouge
total_time_black = (0, 0)  # (secondes, minutes) du joueur noir
seconds_black = 0   # définit les secondes du joueur noir
minutes_black = 0   # définit les minutes du joueur noir
timer_red_text = font_timer.render("00:00", True, crimson, white)   # texte initiale de l'affichage du chrono rouge ("texte", police à bord lisse ? , couleur du texte, couleur du fond)
timer_black_text = font_timer.render("00:00", True, black, white)   # texte initiale de l'affichage du chrono noir ("texte", police à bord lisse ? , couleur du texte, couleur du fond)
timer_red_rect = timer_red_text.get_rect()      # récupére le rectangle de notre texte
timer_black_rect = timer_black_text.get_rect()  # récupére le rectangle de notre texte
timer_red_rect.center = ((ecran_dimensions[0] + (ecran_dimensions_2[0] - ecran_dimensions[0])/2) - timer_red_rect.width/1.5 ,ecran_dimensions[1]/9)     # définit le centre du rectangle de notre texte
timer_black_rect.center = ((ecran_dimensions[0] + (ecran_dimensions_2[0] - ecran_dimensions[0])/2) + timer_black_rect.width/1.5 ,ecran_dimensions[1]/9) # définit le centre du rectangle de notre texte

# Bouton recommencer :

font_restart = pygame.font.Font(basic_font, 20)     # définit la police du bouton recommencer
restart_text = font_timer.render("Restart ?", True, black)  # affichage du bouton recommencer
restart_rect = restart_text.get_rect()  # récupére le rectangle du bouton recommencer
restart_rect.center = ((ecran_dimensions[0] + (ecran_dimensions_2[0] - ecran_dimensions[0])/2),ecran_dimensions[1]-ecran_dimensions[1]/4)   # définit le centre du rectangle de notre bouton


# Affichage victoire :

font_popup = pygame.font.Font(basic_font, 24)   # définit la police de caractère

popup_front_rect = pygame.Rect((0,0),(300,150)) # rectangle dessiné qui fera le fond blanc du pop up
popup_front_rect.center = (ecran_dimensions[0]/2, ecran_dimensions[1]/2)    # on le met au milieu du plateau d'échec

winner = None   # valeur par défaut de qui a gagné
popup_winner_text = font_timer.render(f"{winner} player won !", True, black)    # texte a affiché si un des deux joueurs met mat à l'autre
popup_winner_rect = popup_winner_text.get_rect()    # créer le rectangle du texte
popup_winner_rect.center = (ecran_dimensions[0]/2, ecran_dimensions[1]/2 - ecran_dimensions[1]/25)  # met le texte au milieu de notre fenêtre

popup_background_rect = pygame.Rect((0,0),(310,160))    # rectangle dessiné qui fera le fond gris du fond blanc du pop up (pour que ce soit plus beau)
popup_background_rect.center = (ecran_dimensions[0]/2, ecran_dimensions[1]/2) # on le met au milieu

popup_button_exit_text = font_timer.render("   Exit   ", True, black, red)  # texte du bouton exit
popup_button_exit_rect = popup_button_exit_text.get_rect()  # on récupère un rectangle a partir du texte
popup_button_exit_rect.center = (ecran_dimensions[0]/2 + ecran_dimensions[0]/8, ecran_dimensions[1]/2 + ecran_dimensions[1]/15) # on cale le bouton exit à droite car ça me semble plus logique que à gauche

popup_button_restart_text = font_timer.render("Restart", True, black, light_green) # texte du bouton recommencer
popup_button_restart_rect = popup_button_restart_text.get_rect()    # on récupère un rectangle a partir du texte
popup_button_restart_rect.center = (ecran_dimensions[0]/2 - ecran_dimensions[0]/8, ecran_dimensions[1]/2 + ecran_dimensions[1]/15)  # on cale le bouton recommencer à gauche car ça me semble plus logique que à droite


file_places_pieces = ""                  # Mon répertoire : "E:/_TG2_/NSI/Projet/Jeu_echec_chinois/pieces/"

# Pièces rouges :   # Permet d'importer toutes mes images à partir du fichier donnée 
Canon_R = pygame.image.load(f"{file_places_pieces}Canon_R.png").convert_alpha() 
Cavalier_R = pygame.image.load(f"{file_places_pieces}Cavalier_R.png").convert_alpha()
Chariot_R = pygame.image.load(f"{file_places_pieces}Chariot_R.png").convert_alpha() 
Elephant_R = pygame.image.load(f"{file_places_pieces}Elephant_R.png").convert_alpha()
Garde_R = pygame.image.load(f"{file_places_pieces}Garde_R.png").convert_alpha()
General_R = pygame.image.load(f"{file_places_pieces}General_R.png").convert_alpha()
Pion_R = pygame.image.load(f"{file_places_pieces}Pion_R.png").convert_alpha()

Pieces_R = [Canon_R,Cavalier_R,Chariot_R,Elephant_R,Garde_R,General_R,Pion_R] # liste contenant les images de toutes mes pièces rouges

# Pièces noires :   # Permet d'importer toutes mes images à partir du fichier donnée 
Canon_N = pygame.image.load(f"{file_places_pieces}Canon_N.png").convert_alpha()
Cavalier_N = pygame.image.load(f"{file_places_pieces}Cavalier_N.png").convert_alpha()
Chariot_N = pygame.image.load(f"{file_places_pieces}Chariot_N.png").convert_alpha()
Elephant_N = pygame.image.load(f"{file_places_pieces}Elephant_N.png").convert_alpha()
Garde_N = pygame.image.load(f"{file_places_pieces}Garde_N.png").convert_alpha()
General_N = pygame.image.load(f"{file_places_pieces}General_N.png").convert_alpha()
Pion_N = pygame.image.load(f"{file_places_pieces}Pion_N.png").convert_alpha()

Pieces_N = [Canon_N,Cavalier_N,Chariot_N,Elephant_N,Garde_N,General_N,Pion_N] # liste contenant les images de toutes mes pièces noires


# Pièces départ rouges: # définit la pos de départ des pièces du jeu d'échec chinois à l'aide d'un dictionnaire 
dict_red_start_pos = {Chariot_R:[(0,0),(8,0)],Cavalier_R:[(1,0),(7,0)],Canon_R:[(1,2),(7,2)], Elephant_R:[(2,0),(6,0)],Garde_R:[(3,0),(5,0)],General_R:[(4,0)],Pion_R:[(0,3),(2,3),(4,3),(6,3),(8,3)]}

# Pièces départ noires:
dict_black_start_pos = {Chariot_N:[(0,9),(8,9)],Cavalier_N:[(1,9),(7,9)],Canon_N:[(1,7),(7,7)], Elephant_N:[(2,9),(6,9)],Garde_N:[(3,9),(5,9)],General_N:[(4,9)],Pion_N:[(0,6),(2,6),(4,6),(6,6),(8,6)]}


def get_name(variable): # fonction renvoyant la clé du dictionnaire items de gloabals si la valeur lié à cette clé est la même que celle donnée en paramètre
    name = [key for key , value in globals().items() if value == variable]
    if len(name) > 1 :
        return name
    if len(name) == 1:
        return name[0]
    else:
        return None


def get_list_all_pose():    # Fonction créant un tableau à deux entrées définissant toutes les poses où des pièces du jeu d'échec peuvent se rendre (y,x) (l'ordonnée étant le premier paramètre et l'absice étant le deuxième)
    list_all_pose = []
    pose_y = 50
    for ligne in range(0,10):
        list_all_pose.append([])
        pose_x = 50
        for colonne in range(0,9):
            list_all_pose[ligne].append((pose_x,pose_y))    # ajoute à notre liste le tuple (pose_x,pose_y)  
            pose_x += 51
        pose_y += 51
    return list_all_pose

list_all_pose = get_list_all_pose() # stocke la pose de toute nos case dans list_all_pose


def get_list_all_pos():     # fonction créant une liste contenant toutes les pos où des pièces du jeu d'échec peuvent se rendre (elles font toutes partie d'une seule liste, ce n'est pas un tableau à deux entrées)
    list_all_pos = []
    pos_y = 0
    for ligne in range(0,10):
        pos_x = 0
        for colonne in range(0,9):
            list_all_pos.append((pos_x,pos_y))
            pos_x += 1  # attention : chacune de mes cases contient 50 x50 pixels mais il faut faire attention au bordures noires qui font 1 pixel
        pos_y += 1
    
    return list_all_pos

list_all_pos = get_list_all_pos()   # stocke la pos de toute nos case dans list_all_pos


kings = []  # 0 : le roi rouge et 1 : le roi noir   # crée une liste qui va contenir nos deux objets étant les rois, avec d'abord le roi rouge puis le roi noir

def get_list_object_pieces():
    list_object_pieces = [] # crée une liste contenant tous les objets (l'orde n'y a pas d'importance, ce n'est pas un tableau à deux entrées)

    for piece_rouge in Pieces_R:    # prend chaque image des pièces rouges, une à une et :
        for pos_piece in dict_red_start_pos[piece_rouge]:   # récupère sa pos de départ dans le dictionnaire dict_red_start_pos
            rectangle = piece_rouge.get_rect()  # lui crée un rectangle a partir de son image 
            rectangle.center = (list_all_pose[pos_piece[1]][pos_piece[0]])  # définit la position central du rectangle
            piece = Pieces("red",get_name(piece_rouge)[0:-2].lower(),list_all_pose[pos_piece[1]][pos_piece[0]],pos_piece,rectangle,piece_rouge)     # crée un objet pièce avec les paramètres : (couleur, le type de pièce que c'est (char), sa pose (coordinate), sa pos, son rectangle, son image)
            list_object_pieces.append(piece)    # puis ajoute cette pièce à notre
            if piece.char == "general": # si la pièce en question est un général alors :
                kings.append(piece)     # on l'ajoute à notre liste stockant les rois 

    for piece_noire in Pieces_N:    # prend chaque image des pièces noires, une à une et :
        for pos_piece in dict_black_start_pos[piece_noire]: # récupère sa pos de départ dans le dictionnaire dict_black_start_pos
            rectangle = piece_noire.get_rect()  # lui crée un rectangle a partir de son image 
            rectangle.center = (list_all_pose[pos_piece[1]][pos_piece[0]])  # définit la position central du rectangle
            piece = Pieces("black",get_name(piece_noire)[0:-2].lower(),list_all_pose[pos_piece[1]][pos_piece[0]],pos_piece,rectangle,piece_noire)   # crée un objet pièce avec les paramètres : (couleur, le type de pièce que c'est (char), sa pose (coordinate), sa pos, son rectangle, son image)
            list_object_pieces.append(piece)    # puis ajoute cette pièce à notre
            if piece.char == "general": # si la pièce en question est un général alors :
                kings.append(piece)     # on l'ajoute à notre liste stockant les rois 
    
    return list_object_pieces   # renvoit notre liste contenant tous les objets


list_object_pieces = get_list_object_pieces()   # stocke tous les object dans list_object_pieces


def calcul_dis(x1,y1,x2,y2):    # fonction renvoyant la distance entre deux points dans un plan en 2D, en prenant la pose x et y des deux points
    return sqrt((x2-x1)**2+(y2-y1)**2)  # formule calculant la distance entre deux points en 2 dimmensions


def get_case_nearest(pose):     # fonction renvoyant la pose de la case la plus proche de la pose donnée en paramètre

    pose_nearest = None
    dis_nearest = None

    num_colonne = 0
    for colonne in list_all_pose:   # Pour cela, on recherche parmis toute nos cases une à une en faisant calcul dis entre la pose en paramètre et la pose de la case téstée 
        num_ligne = 0
        for ligne in colonne:       # ligne représente le tuple (x,y) de la position d'un emplacement sur le plateau
            if pose_nearest == None:
                pose_nearest = ligne
                dis_nearest = calcul_dis(pose[0],pose[1],ligne[0],ligne[1])
            else:
                if dis_nearest > calcul_dis(pose[0],pose[1],ligne[0],ligne[1]):
                    pose_nearest = ligne
                    dis_nearest = calcul_dis(pose[0],pose[1],ligne[0],ligne[1])
            num_ligne += 1
        num_colonne += 1
    
    return pose_nearest


def get_pos_with_pose(pose):    # Obtient la pos à partir d'une pose (nécessite la pose exacte de la pos que l'on recherche)
    num_colonne = 0
    for colonne in list_all_pose:
        num_ligne = 0
        for ligne in colonne:
            if pose == ligne:
                return (num_ligne,num_colonne)
            num_ligne += 1
        num_colonne += 1

    return "mauvaise pose"

current_window = 0  # socke l'état actuel de notre fenêtre (0 : "sans paramètres"; 1 : "paramètres")
def switch_window():    # permet de changer entre la fenêtre "sans paramètres" et avec "paramètres"
    global current_window
    if current_window == 0:
        screen = pygame.display.set_mode(ecran_dimensions_2)    # change la taille de notre fenêtre pygame
        current_window += 1
    elif current_window == 1:
        screen = pygame.display.set_mode(ecran_dimensions)      # change la taille de notre fenêtre pygame
        current_window -= 1

def switch_player():    # fonction permettant de changer le joueur actuel
    global current_player
    global total_time_red
    global total_time_black
    global start_time_red
    global start_time_black

    # change le joueur actuel :
    if current_player == players[0]:
        current_player = players[1]
        start_time_black = time.time()
        total_time_black = (seconds_black, minutes_black)
    elif current_player == players[1]:
        current_player = players[0]
        start_time_red = time.time()
        total_time_red = (seconds_red, minutes_red) 

def get_other_player_color(color):  # obtient l'autre couleur que celle donnée en paramètre
    if color == 'red':
        return 'black'
    elif color == 'black':
        return 'red'

def switch_solo():  # permet de changer entre le mode solo (= le mode débug ou les joueur peuvent jouer même si ce n'est pas leur tour) et le mode non solo
    global solo
    if solo == True:
        solo = False
    else:
        solo = True

def restart():  # Fonction recommancant la partie à zéro
    global list_object_pieces

    global seconds_red
    global minutes_red
    global seconds_black
    global minutes_black
    global total_time_red
    global total_time_black
    global winner
    global mat
    global start_time_red
    global start_time_black
    global timer_red_text
    global timer_black_text
    global piece_to_move
    global piece_to_move_last_pose
    global down
    global current_player
    

    # en redonnant la valeur par défaut à mes variables
    list_object_pieces = get_list_object_pieces()
    seconds_red, minutes_red = 0, 0
    seconds_black, minutes_black = 0, 0
    total_time_red = (0, 0)
    total_time_black = (0, 0)

    winner = None
    mat = False
    pygame.mouse.set_cursor(pygame.cursors.arrow)

    start_time_red = time.time()
    start_time_black = time.time()
    timer_red_text = font_timer.render("00:00", True, crimson, white)
    timer_black_text = font_timer.render("00:00", True, black, white)

    piece_to_move = None
    piece_to_move_last_pose = None
    down = False

    current_player = 'Red'

def get_king(color):    # obtient l'objet roi à partir de sa couleur car ils sont stockés dans la liste king
    
    if color == 'red':
        return kings[0]
    elif color == 'black':
        return kings[1]


def test_echec(color_of_king):  # fonction renvoyant soit False soit True en fonction de si le roi de la couleur donné en paramètre est actuellement en échec
    echec = False
    
    # vérifie si chaque objet de la couleur différent du roi téster peuvent manger le roi la où il est et renvoit True si oui
    for object in list_object_pieces:
        if object.get_alive() ==  True:
            if object.get_color() == get_other_player_color(color_of_king):
                if object.test_case(get_king(color_of_king).pos,list_object_pieces) != False:
                    echec = True

    # une règle aux échecs chinois est que les deux rois ne peuvent pas se regarder sans pièces au milieu, donc c'est considérer comme un échec
    can_king_see_the_other_king = True
    if get_king(color_of_king).get_pos()[0] == get_king(get_other_player_color(color_of_king)).get_pos()[0]:    # vérifie déjà si les rois de couleurs opposé sont sur la même absice
        x_kings = get_king(color_of_king).get_pos()[0]  
        for y_pos in range(1+get_king('red').pos[1],get_king('black').pos[1]):  # puis vérifie pour chacune des cases les séparant si 
            for object in list_object_pieces:   
                if object.get_alive() == True:  # il y a une pièce qui ne sait pas déjà fait manger
                    if object.get_pos() == (x_kings,y_pos): # et si la pos de cette pièce est la même que une des cases séparant les deux rois 
                        can_king_see_the_other_king = False # si oui, cela signifie qu'ils ne peuvent pas se voir
    else:   # si ils ne sont pas sur le même absice alors ils ne peuvent pas se voir 
        can_king_see_the_other_king = False

    if (echec == True) or (can_king_see_the_other_king == True):    # si le roi est en échec ou est visible par l'autre roi alors, renvoit True
        return True
    else:
        return False


def test_mat(king_test):    # Permet de savoir si le roi donnée en paramètre est en échec

    move_possible_player = 0  # compte le nombre de case possible pour le joueur

    for object in list_object_pieces:   # Dans toutes les pièces encore vivantes et de même couleur que le roi : 
        if object.color == king_test.color: 
            if object.alive == True:

                for case in list_all_pos:   # Dans toutes les cases du plateau
                    
                    last_eaten = None   

                    test = object.test_case(case,list_object_pieces)    # vérifie si cette case est une case atteignable par l'objet que l'on teste

                    if test != False:   
                        if test != None:    # Si il y a un truc a y manger :
                            test.update_alive() # le manger + 
                            last_eaten = test   # stocker ce qu'on a mangé pour s'en rappeler

                        object_last_pose = object.get_coordinate()  # On sauvegarde l'ancienne pose de notre objet qui se déplace

                        object.get_rect().center = list_all_pose[case[1]][case[0]]  # et on met à jour son rectangle puis :
                        update_piece(object)    # sa pose et sa pos

                        echec = test_echec(object.color)    # vérifie si après ce déplacement le roi est en échec (on ne vérifie pas avant aussi car aux échec 
                                                            # chinois si un joueur ne peux plus du tout se déplacer(aucune de ses pièces), sa équivaut à un mat)

                        if echec != True:   # Si le roi n'est pas en échec après se déplacement alors :
                            move_possible_player += 1 # ça fait une case de plus où le joueur peut se déplacer 

                        object.get_rect().center = object_last_pose # redonne son rectangle à l'objet qui c'est déplacé 
                        update_piece(object)    # redonne sa pose et sa pos à l'objet qui c'est déplacé

                        if last_eaten != None:  # Si un objet a été mangé alors :
                            last_eaten.came_back_to_life()  # on le fait revenir à la vie


    if move_possible_player == 0:   # Si aucun déplacement n'est possible alors :
        return True     # c'est un mat
    else:
        return False    # sinon : c'est pas un mat          

                        



def update_piece(piece):    # fonction qui met à jour la pose et la pos de la pièce mise en paramètre à partir de la pose de sont rectangle 
    if piece.get_alive() == True:
        
        piece.update_coordinate((piece.get_rect().x+25, piece.get_rect().y+25)) # car la pose du rectangle est au milieu donc on ajoute en hauteur et en largeur la moitié d'une case
        
        if piece.char == 'general': # Si la pièce est un général alors :
            if piece.color == 'red':
                kings[0] = piece    # on va mettre à jour la liste qui contient les généraux, en fonction de sa couleur, kings[0] : rouge
            elif piece.color == 'black':
                kings[1] = piece    # on va mettre à jour la liste qui contient les généraux, en fonction de sa couleur, kings[1] : noir

        
        new_pos = get_pos_with_pose(piece.get_coordinate())
        if new_pos == "mauvaise pose":  # ce cas est lorsque l'on est en train de déplacer une pièce (lorsqu'elle est maintenu en "l'air")
            pass
        else:
            piece.update_pos(new_pos)


        

on = True   # on permet de garder la fenêtre du jeu ouverte

solo = False # solo (: a peu près le mode débug), permet si activer de jouer plusieurs fois d'affilé

mat = False # = True si un des deux joueurs à perdu

# Le chrono :
if current_player == 'Red':
    start_time_red = time.time()
elif current_player == 'Black':
    start_time_black = time.time()


while on == True:

    # stocke la position de notre souris sur l'écran sous forme d'un tuple (x,y) dans pose
    pose = pygame.mouse.get_pos()

    pose_x = pose[0]    # répartit pose en deux variable : pose_x et pose_y (apparemment jamais utilisé mais ça peu toujours servir)
    pose_y = pose[1]

    if "piece_to_move" not in globals():    # Permet "d'initialiser" le jeu, en vérifiant si la variable piece_to_move a déjà été créer 
        piece_to_move = None
        piece_to_move_last_pose = None
        down = False
        echec = None
        pygame.mouse.set_cursor(pygame.cursors.arrow)   # définit le curseur de base dans la fenêtre à la flèche verte (Pourquoi pas la flèche de base ? : car j'ai pas trouvé la commande)
        
    
    screen.fill(gray)   # remplis le fond de gris, puis

    screen.blit(plateau,(0,0))  # affiche le plateau (à ne pas faire dans l'autre sens ou on ne verrait pas le plateau)

    if current_window == 1 or mat == True: # vérifie que l'on ait ouvert le menu des "paramètres" et si c'est le cas : 
        if (restart_rect.collidepoint(pose) == False) and (popup_button_exit_rect.collidepoint(pose) == False) and (popup_button_restart_rect.collidepoint(pose) == False): # vérifie si la souris se trouve sur un bouton si non alors :
            pygame.mouse.set_cursor(pygame.cursors.arrow) # lui fait reprendre son apparence originale

    for event in pygame.event.get():    # vérifie les événements que l'on a réalisé (vérifie si y a des input clavier ou souris ou autre)
        if event.type == pygame.QUIT:  # si on a appuyer sur la petite croix en haut à droite alors:     
            pygame.quit()   # fermet la fenêtre pygame
            on = False  # et coupe la boucle

        if event.type == pygame.KEYDOWN:    # pareil que si on appuie sur la petite croix car j'ai l'habitude de définir quitter sur la flèche du bas
            if event.key == pygame.K_DOWN:
                pygame.quit()
                on = False
            
            if event.key == pygame.K_a: # si on appuie sur la touche 'a' alors :
                for piece in list_object_pieces:    
                    if piece.get_alive() == True:
                        if piece.get_rect().collidepoint(pose) == True: 
                            print(piece.get_info()) # affiche les informations concernant la pièces sur laquel on est (: pour débug)

            '''
            # Permet de tuer la pièce sur laquel est notre curseur lorsqu'on appuie sur 'e' mais pas très utile
            if event.key == pygame.K_e: 
                for piece in list_object_pieces:
                    if piece.get_alive() == True:
                        if piece.get_rect().collidepoint(pose) == True: 
                            piece.update_alive()
            '''
                            
            if event.key == pygame.K_s: # Si on appuie sur 's', change le tour du joueur (se fait automatiquement hors du mode solo mais permet de débug)
                switch_player()

            if event.key == pygame.K_o: # Permet d'intervertir entre le mode solo et non solo lorsqu'on appuie sur 'o'
                switch_solo()

            '''
            if event.key == pygame.K_p: # activer le menu comme si il y avait eu un mat
                mat = True
            '''
                
            if event.key == pygame.K_ESCAPE:    # Permet d'ouvrir le menu des paramètres lorsqu'on appuie sur 'echap'
                switch_window()


            if event.key == pygame.K_t: # Annonce au joueur quel roi est en échec (optionnel)
                if test_echec('red') == False :
                    print("Le roi rouge n'est pas en échec.")
                else:
                    print("Le roi rouge est en échec.")
                if test_echec('black') == False :
                    print("Le roi noir n'est pas en échec.")
                else:
                    print("Le roi noir est en échec.")
                

        if event.type == pygame.MOUSEBUTTONDOWN:    # si on appuie sur la souris (attention : différent de si on relache l'appuie sur la souris)
            down = True
            for piece in list_object_pieces:    
                if piece.get_alive() == True:   # Pour tous les objets étant en vie :
                    if piece.get_rect().collidepoint(pose) == True: # si l'image de la pièce est là où on a cliqué 
                        piece_to_move_last_pose = piece.get_coordinate()    # on stocke la pose de la pièce que l'on s'apprête à déplacer
                        piece_to_move = piece   # et on stocke la pièce que l'on est en train de déplacer
            
            if current_window == 1: # si le menu paramètre est ouvert alors :
                if restart_rect.collidepoint(pose): # si la souris se trouve sur le bouton recommencer lorsque l'on appuie sur la souris alors :
                    restart()   # on recommence la partie
            
            if mat == True:     # si un des deux joueurs est mat alors :
                if popup_button_exit_rect.collidepoint(pose):      # si on clique sur le bouton exit :
                    pygame.quit()
                    on = False  # ferme la fenêtre
                if popup_button_restart_rect.collidepoint(pose):   #  si on clique sur le bouton restart :
                    restart()   # relance le jeu
            
            
        if event.type == pygame.MOUSEBUTTONUP:      # si on relache l'appuie sur la souris
            if down == True:    # si on avait appuyer sur la souris avant alors
            
                if piece_to_move != None:   # si on est en train de déplacer une pièce

                    if solo :   # différentie le mode solo et le mode non solor pour savoir si un déplacement réussi change le joueur qui va jouer ou non et si le joueur à qui ce n'est pas le tour peut jouer

                        temporary_eaten = None
                        test = piece_to_move.test_case(get_pos_with_pose(get_case_nearest(pose)),list_object_pieces)    # .test_case() peut renvoyer 3 choses : False si l'on ne peut pas se déplacer, None 
                                                                                                                        # si l'on peut se déplacer mais qu'on ne mange pas et un objet si on peut manger ce dit objet
                        if test != False:   # si un déplacement est possible alors :                                                                                                                          
                            if test != None:    # si notre déplacement nous fait manger alors :
                                test.update_alive() # on tue l'objet manger
                                temporary_eaten = test  # et on le stocke

                            temporary_moved = piece_to_move # on stocke aussi la pose de l'objet qui va se déplacer, avant son déplacement

                            piece_to_move.get_rect().center = get_case_nearest(pose)    # on change la pose du rectangle de notre pièce avec la pose de la case la plus proche de la où la souris est
                            update_piece(piece_to_move) # puis on met à jour la pose et la pos de la pièce
                            
                            echec = test_echec(piece_to_move.get_color())   # on vérifie si suite à ce déplacement, le roi de la pièce en question est mis en échec
                            # on vérifie aussi si la souris est dans l'écran lorsqu'elle relache la pièce
                            if (echec == True) or (not ecran_dimensions_rect.collidepoint(pose)):   # si c'est le cas alors :
                                temporary_moved.get_rect().center = (piece_to_move_last_pose)   # on redonne l'ancienne pose à la pièce déplacée
                                if temporary_eaten != None:    # et si elle a mangé alors:
                                    temporary_eaten.came_back_to_life() # on fait revenir à la vie la pièce mangée

                            else:

                                if test_mat(get_king('red')) == True:
                                    winner = "Black"    # puis on définit le gagnant et
                                    mat = True  # on annonce qu'il y a mat

                                elif test_mat(get_king('black')) == True:
                                    winner = "Red"    # puis on définit le gagnant et
                                    mat = True  # on annonce qu'il y a mat


                        else:
                            piece_to_move.get_rect().center = (piece_to_move_last_pose) # si ce n'est pas un déplacement possible alors on fait revenir la pièce à son ancienne oise
                    
                    elif not solo : # Si on est pas seul alors comme solo sauf que :

                        if piece_to_move.get_color() == current_player.lower(): # on vérifie si le joueur actuel touche une de ses pièces
                            temporary_eaten = None
                            test = piece_to_move.test_case(get_pos_with_pose(get_case_nearest(pose)),list_object_pieces)
                            if test != False:
                                if test != None:
                                    test.update_alive() 
                                    temporary_eaten = test

                                temporary_moved = piece_to_move

                                piece_to_move.get_rect().center = (get_case_nearest(pose))
                                update_piece(piece_to_move) # puis on met à jour la pose et la pos de la pièce
                                
                                echec = test_echec(piece_to_move.get_color())

                                if (echec == True) or (not ecran_dimensions_rect.collidepoint(pose)):
                                    temporary_moved.get_rect().center = (piece_to_move_last_pose)
                                    if temporary_eaten != None:
                                        temporary_eaten.came_back_to_life()
                                else:

                                    if test_mat(get_king('red')) == True:
                                        winner = "Black"    # puis on définit le gagnant et
                                        mat = True  # on annonce qu'il y a mat

                                    elif test_mat(get_king('black')) == True:
                                        winner = "Red"    # puis on définit le gagnant et
                                        mat = True  # on annonce qu'il y a mat

                                    switch_player() # si le déplacement est validé alors on change le tour du joueur

                            else:
                                piece_to_move.get_rect().center = (piece_to_move_last_pose)

                        else:
                            piece_to_move.get_rect().center = (piece_to_move_last_pose) # Si le joueur essaye de déplacer une pièce qui ne lui intervient pas alors on annule le déplacement
    
            down = False
            piece_to_move = None
            piece_to_move_last_pose = None
            



        if event.type  == pygame.MOUSEMOTION:   # Si la souris se déplace alors : 
            if down == True:    # si le bouton de la souris est maintenu alors :
                if piece_to_move != None:   # si il y a une pièce que l'on est actuellement en train de déplacer
                    piece_to_move.get_rect().center = pose  # alors la pose du rectangle de cette pièce devient la pose actuelle de notre souris

            if current_window == 1: # si le menu "paramètres" est ouvert alors :
                if restart_rect.collidepoint(pose): # si la souris est sur le bouton recommencer
                    pygame.mouse.set_cursor(pygame.cursors.diamond) # alors on change le design du curseur de la souris

            if mat == True: # si la fenêtre qui s'ouvre lorsqu'un joueur à gagné est ouvert alors :
                if popup_button_restart_rect.collidepoint(pose):    # change sa souris si il est sur le bouton restart
                    pygame.mouse.set_cursor(pygame.cursors.diamond)

                if popup_button_exit_rect.collidepoint(pose):       # change sa souris si il est sur le bouton restart
                    pygame.mouse.set_cursor(pygame.cursors.diamond)

    if on : # Si la boucle n'est pas coupé (: presque inutile mais permet d'éviter le message d'erreur qui dit qu'on peut plus rien faire une fois qu'on a fermé la fenêtre pygame)

        for piece in list_object_pieces :   # pour chaque pièce dans la liste list_object_pieces
            if piece.get_alive() == True:   # si la pièce est en vie alors :

                piece.update_coordinate((piece.get_rect().x+25, piece.get_rect().y+25)) # on change la pose de la pièce en fonction de la pose de son rectangle # +25 car la pose du rectangle est au milieu donc on ajoute en hauteur et en largeur la moitié d'une case
                new_pose = get_pos_with_pose(piece.get_coordinate())    # change la pos de notre objet 
                if new_pose == "mauvaise pose": # si l'objet n'est pas actuellement en déplacement car si il est en train de se déplacer alors la pose donnée en paramètre ne sera surement pas exactement la pose de la case (et sinon, pas grave)
                    pass
                else:
                    piece.update_pos(get_pos_with_pose(piece.get_coordinate()))
        
                screen.blit(piece.get_picture(),piece.get_rect())   # affiche cette pièce sur notre écran "la surface".blit(l'image que l'on veut afficher, sur quel rectangle)

    if on : # Si la boucle est encore active alors : Permet de faire fonctionner le chrono même si ça marche pas encore : 
        """ Met à jour le temps des joueurs """
        current_time = time.time()
        if current_player == "Red":
            seconds_red = int(current_time - start_time_red + total_time_red[0] + total_time_red[1] * 60) % 60
            minutes_red = int(current_time - start_time_red + total_time_red[1] * 60 + total_time_red[0]) // 60
            str_seconds_red = "0"+str(round(seconds_red))
            str_minutes_red = "0"+str(minutes_red)
            timer_red_text = font_timer.render(f"{str_minutes_red[-2:]}:{str_seconds_red[-2:]}", True, crimson, white)
        elif current_player == "Black":
            seconds_black = int(current_time - start_time_black + total_time_black[0] + total_time_black[1] * 60) % 60 
            minutes_black = int(current_time - start_time_black + total_time_black[1] * 60 + total_time_black[0]) // 60
            str_seconds_black = "0"+str(round(seconds_black))
            str_minutes_black = "0"+str(minutes_black)
            timer_black_text = font_timer.render(f"{str_minutes_black[-2:]}:{str_seconds_black[-2:]}", True, black, white)
       
        # Permet de mettre à jour le texte qui indique le tour de quel joueur c'est dans les "paramètres" (en appuyant sur escape), 
        player_turn_text = font_player.render(current_player+"'s Turn", True, white) # car si je met pas à jour le rectangle du texte à 
        player_turn_rect = player_turn_text.get_rect() # chaque changement alors le texte ne sera pas centré
        player_turn_rect.center = (ecran_dimensions[0] + (ecran_dimensions_2[0] - ecran_dimensions[0])/2,ecran_dimensions[1]/2)

        if current_window == 1: # Si le menu "paramètre" est ouvert alors on affiche :
            screen.blit(player_turn_text,player_turn_rect)  # le texte qui indique le tour de quel joueur c'est 
            screen.blit(timer_red_text,timer_red_rect)      # le texte qui indique le temps du joueur rouge
            screen.blit(timer_black_text,timer_black_rect)  # le texte qui indique le temps du joueur noir
            screen.blit(restart_text,restart_rect)          # le bouton recommencer

        if mat == True: # si un des deux joueurs est mat alors :
            popup_winner_text = font_timer.render(f"{winner} player won !", True, black)
            pygame.draw.rect(screen, gray, popup_background_rect)             # affiche le fond gris
            pygame.draw.rect(screen, white, popup_front_rect)                 # affiche le devant blanc
            screen.blit(popup_winner_text, popup_winner_rect)                 # affiche le texte qui indique qui a gagné
            screen.blit(popup_button_exit_text, popup_button_exit_rect)       # affiche le bouton exit
            screen.blit(popup_button_restart_text, popup_button_restart_rect) # affiche le bouton restart
            

    if on :
        pygame.display.flip()   # met à jour notre fenêtre pygame