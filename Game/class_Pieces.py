
class Pieces :

    def __init__(self,color,char,coordinate,pos,rect,picture): # !!! : coordinate ou pose : (x,y) et pos (x,y) avec pos la pose dans le plateau et coordinate la coordonée de l'image
        self.color = color  # color = "red" or "black"
        self.char = char    # donne le type de pièce
        self.coordinate = coordinate    # donne la coordonée dans la fenêtre
        self.pos = pos  # donne la pos de la pièce
        self.rect = rect    # donne le rectangle de la pièce
        self.picture = picture  # donne l'image de la pièce

        self.alive = True   # dit si la pièce est actuellement vivante
        if self.char == "pion": # si c'est un pion alors :
            self.awaken = False # lui donne une stat d'éveil (pour savoir si il a passé la rivière)

    def get_color(self):    # renvoit la couleur de la pièce
        return self.color
    
    def get_char(self):     # renvoit le type de la pièce
        return self.char

    def get_coordinate(self):   # renvoit les coordonées de la pièce
        return self.coordinate
    
    def get_pos(self):  # renvoit la pos de la pièce
        return self.pos
    
    def get_rect(self): # renvoit le rectangle de la pièce
        return self.rect
    
    def get_picture(self):  # renvoit l'image de la pièce
        return self.picture
    
    def get_alive(self):    # renvoit si la pièce est vivante
        return self.alive

    def get_info(self):     # renvoit tous les paramètres de la pièce
        return vars(self)
    
    def update_coordinate(self, new_coordinate):    # change les coordonnées de la pièce
        self.coordinate = new_coordinate
       
    def update_pos(self,new_pos):   # change la pos de la pièce
        self.pos = new_pos

        if (self.char == 'pion') and (self.awaken == False):    # si c'est un pion et qu'il est pas encore éveillé alors:
            if (self.color == 'red') and (self.pos[1] == 5):    # si il est rouge et qu'il a traversé la rivière
                self.update_awaken()                            # l'éveil
            elif (self.color == 'black') and (self.pos[1] == 4):# si il est noir et qu'il a traversé la rivière alors
                self.update_awaken()                            # l'éveil


    def update_awaken(self):    # éveil la pièce
        self.awaken = True

    def update_alive(self):     # tue la pièce si elle est vivante
        if self.alive == True:
            self.alive = False

    def came_back_to_life(self):    # rescucite la pièce si elle est morte
        if self.alive == False:
            self.alive = True

    def test_eatable(self,case_to_test,list_object_pieces): # vérifie si l'objet à la case donnée à la même 
        for object in list_object_pieces:                   # couleur que l'objet qui utilise la méthode
            if object.get_alive() == True:                  # si oui : renvoit False sinon : renvoit l'objet
                if object.get_pos() == case_to_test:        # si il n'y en a pas sur la case testé renvoit None
                    if self.get_color() == object.get_color():
                        return False
                    else:
                        return object
        return None
    
    def get_pos_mid_elephant(self,current_pos,new_pos): # Permet d'obtenir la pose au milieu
                                                        # du déplacement des éléphants
        if current_pos[0] > new_pos[0]:
            pos_mid_x = new_pos[0] + 1
        else:
            pos_mid_x = new_pos[0] - 1

        if current_pos[1] > new_pos[1]:
            pos_mid_y = new_pos[1] + 1
        else:
            pos_mid_y = new_pos[1] - 1
        
        return (pos_mid_x,pos_mid_y)

    def get_pos_diff(self,current_pos,new_pos):         # permet d'obtenir la somme de la différence de distance entre 2 pos de x et y
        pos_diff_x = abs(current_pos[0] - new_pos[0]) 
        pos_diff_y = abs(current_pos[1] - new_pos[1])
        pos_diff = pos_diff_x + pos_diff_y
        if pos_diff_x == 1 and pos_diff_y == 1 :    # mouvement du garde: 
            return 0.5  # valeur permettant de reconnaître le garde
        if pos_diff_x == 2 and pos_diff_y == 2 :    # mouvement de l'élephant
            return 1.5  # valeur permettant de reconnaître l'élephant
        return pos_diff
    
    def get_axis_diff(self,current_pos,new_pos):    # renvoit par quel axis la pièce se déplace ('x' ou 'y' ou 'both')
        pos_diff_x = current_pos[0] - new_pos[0]    
        pos_diff_y = current_pos[1] - new_pos[1]
        if pos_diff_y == 0:
            return 'x'
        elif pos_diff_x == 0:
            return 'y'
        else:
            return 'both'
    

    def test_case(self,case_to_test,list_object_pieces):  # case_to_test est la pos de la case que l'on va essayer   # pos = par rapport à mon tableau et pose / coordinate = pose x et pose y sur la fenêtre
        
        # test case change pour chaque char différents :

        pos_item = self.get_pos()   # Pos item désigne la pos de l'objet qui a prévu de se déplacer

        if self.char == 'canon':    # / La bombarde 

            # Pour le canon, on doit surtout faire attention à quel axis on utilise et qu'il y ait uniquement une pièce entre là où
            # est le canon et là où il veut aller (si il va y manger)

            axis_used = self.get_axis_diff(pos_item,case_to_test)   # test si il utilise les deux abscices ou un des deux uniquement

            eatable = self.test_eatable(case_to_test,list_object_pieces)    # test si la case d'arrivée est mangeable (== couleur différente)

            number_of_obstacles = 0 # compteur d'obstacle

            if eatable != False :

                # Si il utilise l'abscice x alors :
                if axis_used == 'x':

                    if pos_item[0] > case_to_test[0]:  # si la pos de l'objet est plus grande que celle de la case d'arrivée alors 
                        to_start = case_to_test[0]     # on définit le début et 
                        to_end = pos_item[0]           # la fin de notre boucle

                    else:   
                        to_start = pos_item[0]
                        to_end = case_to_test[0]    
                    
                    for i in range(to_start+1,to_end):  # on va vérifier toutes les pièces entre le canon (ce qui expliqe le +1 à to_start, pour ne pas compter la pose du canon) jusqu'à la pose ciblée
                        # i ici c'est l'absice car notre pièce ne se déplace que sur l'absice, ainsi on change pas son ordonnée (x,y)
                        eatable_mid = self.test_eatable((i,pos_item[1]),list_object_pieces) # Si y a une pièce
                        if eatable_mid != None:
                            number_of_obstacles += 1    # alors on rajoute un obstacle


                elif axis_used == 'y':

                    if pos_item[1] > case_to_test[1]:   # Pareil que au dessus sauf que l'on vérifie l'axe des y
                        to_start = case_to_test[1]
                        to_end = pos_item[1]

                    else:
                        to_start = pos_item[1]
                        to_end = case_to_test[1]    

                    for i in range(to_start+1,to_end): # on rajoute 1 au début et non à la fin car on veut savoir les cases comprises entre le chariot et sa destination, sans inclure lui même et sa destination
                        eatable_mid = self.test_eatable((pos_item[0],i),list_object_pieces)
                        if eatable_mid != None:
                            number_of_obstacles += 1
                
                # si il n'y a aucun obstacle et rien a mangé et que un axis d'utilisé alors c'est juste un déplacement
                if (number_of_obstacles == 0) and (eatable == None) and (axis_used != 'both'):
                    return eatable  # eatable peut soit retourné None ou False ou un Objet (quand c'est un objet ça veut dire qu'il peut le manger)
                # si il n'y a 1 obstacle et un truc a mangé et que un axis d'utilisé alors il peut mangé ce que y a au bout
                elif (number_of_obstacles == 1) and (eatable != None) and (axis_used != 'both'):
                    return eatable

        # Maintenant le cavalier :
        elif self.char == 'cavalier':   # / Le cheval

            # très brouyon mais on note ses "mouvements" dans un dictionnaire, la clé est le déplacement et la valeur est la valeur intermédiaire
            # où on doit vérifier si y a une pièce pour savoir si il peut se déplacer à la case d'arrivée
            mouvements_cavalier = {"[-2,1]":[-1,0],"[-2,-1]":[-1,0],"[-1,2]":[0,1],"[1,2]":[0,1],"[2,1]":[1,0],"[2,-1]":[1,0],"[-1,-2]":[0,-1],"[1,-2]":[0,-1]}
            
            eatable_mid_pos = None
            for key in mouvements_cavalier.keys():
                key_list_int = list(map(int,key.strip("[]").split(",")))
                '''
                Ce commentaire est pour cette ligne : key_list_int = list(map(int,key.strip("[]").split(",")))
                .strip("[]") permet de retirer les caractères "[" et "]" qui se trouve à l'extrémité (début ou/et fin) de mon
                mot donc parfait ici (ne pas oublier que key est un string car les clés d'un dictionnaires sont des string).
                .split(",") permet de séparer, les caractères par paquets délimités par le paramètre, ici ","; ces paquets
                sont des listes de chaînes de caractère dans mon cas.
                or pour pouvoir utiliser ces valeurs il me faut des int donc j'ai utilisé la fonction map(), qui prend
                deux paramètres : une fonction à effectuer sur chaque terme et un contenant dans lequel il y a plusieurs termes.
                Ici le contenant est ma liste de string et la fonction est int()
                Et enfin comme map() renvoit un type de valeur illisible, il faut ensuite le retransformer dans le type que l'on veut, ici list().
                
                En résumé :

                "[-2,1]", avec .strip("[]") devient : "-2,1", qui avec .split(",") devient ["-2","1"] qui avec map(int,["-2","1"]) 
                devient <map object at 0x000002B75B359E70> qui avec list() devient [-2,1]

                Leçon à retenir, les dictionnaires ne prennent que des strings en clés.
                '''
                if (pos_item[0] + key_list_int[0],pos_item[1] + key_list_int[1]) == case_to_test:   # la on va vérifier si la case qu'on teste est atteignable avec les clés du dictionnaire
                    eatable_mid_pos = (mouvements_cavalier[key][0] + pos_item[0],mouvements_cavalier[key][1] + pos_item[1]) # si oui alors on récupère aussi la case qu'on doit téster

            # Si il n'y a rien sur la case intermédiaire alors :
            if eatable_mid_pos != None:

                eatable = self.test_eatable(case_to_test,list_object_pieces)

                eatable_mid = self.test_eatable(eatable_mid_pos,list_object_pieces)
                # Si il peut manger, et si cela reste dans le terrain 
                if (eatable != False) and (eatable_mid == None) and (0 <= case_to_test[0] <= 8) and (0 <= case_to_test[1] <= 9):
                    return eatable  # il peut y aller/manger


        elif self.char == 'chariot':    # / La tour

            # ce qui faut faire gaffe avec le chariot c'est juste est ce qu'il utilise qu'un axe et si il y a une pièce entre lui
            # et sa destination, en gros c'est presque comme le canon

            blocked = False # variable qui change si une pièce est dans la trajectoire du canon et ainsi le gène

            eatable = self.test_eatable(case_to_test,list_object_pieces)
            
            axis_used = self.get_axis_diff(pos_item,case_to_test)

            # comme pour le canon :
            if axis_used == 'x':

                if pos_item[0] > case_to_test[0]:
                    to_start = case_to_test[0]
                    to_end = pos_item[0]
                
                else:
                    to_start = pos_item[0]
                    to_end = case_to_test[0]    
                
                for i in range(to_start+1,to_end):
                    eatable_mid = self.test_eatable((i,pos_item[1]),list_object_pieces)
                    if eatable_mid != None:
                        blocked = True
            
            elif axis_used == 'y':

                if pos_item[1] > case_to_test[1]:
                    to_start = case_to_test[1]
                    to_end = pos_item[1]

                else:
                    to_start = pos_item[1]
                    to_end = case_to_test[1]    

                for i in range(to_start+1,to_end): # on rajoute 1 au début et non à la fin car on veut savoir les cases comprises entre le chariot et sa destination, sans inclure lui même et sa destination
                    eatable_mid = self.test_eatable((pos_item[0],i),list_object_pieces)
                    if eatable_mid != None:
                        blocked = True
            
            # On teste si il est bloqué, si il utilise qu'un axis et si il peut manger sa destination ou si elle est libre
            if (axis_used != 'both') and (blocked == False) and (eatable != False):
                return eatable


        elif self.char == 'elephant':   # / Le fou
            # On doit faire attention à ce que l'élephant reste de son côté du terrain, qu'il se déplace bien de
            # 2 en diagonale (x + 2, y + 2) et que la case au milieu de son déplacement soit libre et qu'il puisse manger ou
            # que l'arrivé soit libre
            if self.color == 'red':

                eatable = self.test_eatable(case_to_test,list_object_pieces)    # On vérifie si il peut aller à l'arrivée

                eatable_mid = self.test_eatable(self.get_pos_mid_elephant(pos_item,case_to_test),list_object_pieces) 
                # : vérifie si il y a une pièce entre la case d'arrivée et la case de départ

                # On rappelle que que get_pos_diff : 1.5 désigne 2 en x et 2 en y                                (et la dernière condition vérifie qu'il ne sort pas de son côté)
                if (self.get_pos_diff(pos_item,case_to_test)== 1.5) and (eatable != False) and (eatable_mid == None) and (0 <= case_to_test[1] <= 4):
                    return eatable
                
            elif self.color == 'black': # Pareil que pour le rouge mais on change les paramètres pour tester si il est de son côté

                eatable = self.test_eatable(case_to_test,list_object_pieces)

                eatable_mid = self.test_eatable(self.get_pos_mid_elephant(pos_item,case_to_test),list_object_pieces)
                # : vérifie si il y a une pièce entre la case d'arrivée et la case de départ

                if (self.get_pos_diff(pos_item,case_to_test)== 1.5) and (eatable != False) and (eatable_mid == None) and (5 <= case_to_test[1] <= 9):
                    return eatable

        elif self.char == 'garde':  # / Le conseiller
            # Le garde doit réster dans le palais (la croix) et il ne peut se déplacer que en diagonale de 1

            eatable = self.test_eatable(case_to_test,list_object_pieces)

            if self.color == 'red':
                case_possible_garde_red = [(3,0),(5,0),(4,1),(3,2),(5,2)]   # : on stocke les poses où il peut aller dans le palais
                # get_pos_diff : 0.5 désigne (x + 1, y + 1) donc le déplacement en diagonale du cavalier
                if (self.get_pos_diff(pos_item,case_to_test)==0.5) and (eatable != False) and (case_to_test in case_possible_garde_red):
                    return eatable

            elif self.color == 'black': # pareil que pour le rouge
                case_possible_garde_black = [(3,9),(5,9),(4,8),(3,7),(5,7)]
                if (self.get_pos_diff(pos_item,case_to_test)==0.5) and (eatable != False) and (case_to_test in case_possible_garde_black):
                    return eatable  

        elif self.char == 'pion':   # / Le soldat
            # le pion doit pouvoir avancer et s'éveiller lorsqu'il traverse la rivière sans oublier qu'il peut manger les pièces qu'il croise (si ils sont de couleurs différentes (lui et la pièce))
            eatable = self.test_eatable(case_to_test,list_object_pieces)

            if self.color == 'red': # si rouge :
                # si éveillé ses déplacements autorisés sont 1 à droite ou 1 à gauche ou 1 vers chez les noirs
                if self.awaken == True:
                    if (self.get_pos_diff(pos_item,case_to_test)==1) and (case_to_test != (pos_item[0],pos_item[1]-1)) and (eatable != False):
                        return eatable
                # si non éveillé ses déplacements autorisés sont 1 vers chez les noirs       
                elif case_to_test == (pos_item[0],pos_item[1]+1) and (eatable != False):
                    return eatable

            elif self.color == 'black': # comme pour les rouges sauf qu'il se dirige vers chez les rouges

                if self.awaken == True:
                    if (self.get_pos_diff(pos_item,case_to_test)==1) and (case_to_test != (pos_item[0],pos_item[1]+1)) and (eatable != False):
                        return eatable
                        
                elif case_to_test == (pos_item[0],pos_item[1]-1) and (eatable != False):
                    return eatable

        elif self.char == 'general':    # / Le roi
            # Ici on fait uniquement attention a ses déplacements (on s'occupe d'échec/mat/... autre part)

            if self.color == 'red': # Si il est rouge :
                case_possible_general_red = [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)] # on lui donne les cases où il peut aller dans son palais
                eatable = self.test_eatable(case_to_test,list_object_pieces)    # si il peut manger
                # et si son déplacement se fait bien d'un uniquement
                if case_to_test in case_possible_general_red and (eatable != False) and (self.get_pos_diff(pos_item,case_to_test)==1):
                    return eatable
                
            elif self.color == 'black': # Pareil que chez les rouges mais avec des coordonnées de palais différentes
                case_possible_general_black = [(3,7),(3,8),(3,9),(4,7),(4,8),(4,9),(5,7),(5,8),(5,9)]
                eatable = self.test_eatable(case_to_test,list_object_pieces)
                if case_to_test in case_possible_general_black and (eatable != False) and (self.get_pos_diff(pos_item,case_to_test)==1):
                    return eatable

        else:   # Si on a pas le bon char alors :
            return "Mauvaise pièce :" + self.char
        
        # renvoit False si le déplacement n'est pas possible
        return False
