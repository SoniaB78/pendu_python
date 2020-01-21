from random import randint
from time import sleep
import pygame
from pygame.locals import *

class Pendu():

    def __init__(self):

        self.nbDeCoupsRestants = 7
        self.lettreTappees = []
        self.lettreTappeesSTR = ""
        self.motAAfficher = []

    def creationListeDeMots(self,theme):
        self.themeChoisi = theme.capitalize()
        "Création de la liste des mots en fonction du theme en attribut"
        self.affichageComplet
        self.listeDeMots = []

        if theme == "chiens":
            fichier = ".\\chiens\\index.csv"
        elif theme == "pays":
            fichier = ".\\pays\\index.csv"
        elif theme == "instruments":
            fichier = ".\\instruments\\index.csv"
        elif theme == "fruits":
            fichier = ".\\fruits\\index.csv"
        with open(fichier, encoding='utf-8') as f :
            for ligne in f:
                ligne_recuperee = f.readline()
                ligne_coupee = ligne_recuperee.split(";")


                mot = ligne_coupee[0]
                #imageDeFin = ligne_coupee[1]
                #lienURL  = ligne_coupee[2]
                self.listeDeMots.append(mot)


    def selectionMot(self):
        "Tire un mot au hasard dans la liste listeDeMots"
        self.motATrouver = self.listeDeMots[randint(0,len(self.listeDeMots)-1)]

        return self.motATrouver

    def lettreJoueePresente(self,lettreJouee):
        "Vérifie si la lettre est présente dans le mot"

        if lettreJouee != "" and not lettreJouee in self.lettreTappees:
            self.lettreTappees.append(lettreJouee)
            self.lettreTappeesSTR += lettreJouee


        if lettreJouee in self.motATrouver:
            return True
        else:
            self.nbDeCoupsRestants -= 1
            return False

    def partiePerdue(self):
        "Vérifie si perdu"
        if self.nbDeCoupsRestants <= 0:
            return True
        else:
            return False

    def partieGagnee(self):
        "Vérifie si gagné"
        if "-" in self.motAAfficher:
            return False
        else:
            return True

    def affichageMot(self):
        "Crée le mot a afficher avec des '-' si la lettre n'a pas été tentée"
        self.motAAfficher = []
        for lettreMot in self.motATrouver:
            if lettreMot in self.lettreTappees:
                self.motAAfficher.append(lettreMot)
            elif lettreMot == " " or lettreMot == "-":
                self.motAAfficher.append("   ")
            else:
                self.motAAfficher.append("-")

        motEnStr = ""
        for lettre in self.motAAfficher:
            motEnStr += lettre

        self.motAAfficher = motEnStr

        return self.motAAfficher

    def affichageComplet(self):
        print("Il reste",self.nbDeCoupsRestants,"coups")
        print("Lettre jouées :",self.lettreTappees)
        print(self.affichageMot())







##  Programme Principal
pygame.init()


police = pygame.font.SysFont("impact", 50)





fenetre = pygame.display.set_mode((1080,720))
jeu = Pendu()

#Gestion des fonds des différentes fenetres
fondTheme = pygame.image.load(".\\fond\\fondTheme.jpg")
fondJeu = pygame.image.load(".\\fond\\fondJeu.jpg")








continuerChoixTheme = True
#   Fenetre choix du thème
##  Position sur la fenêtre
positionTexteChoix =    (380,20)
positionTexteChiens =   (450,150)
positionTexteFruits =   (460,250)
positionTexteInstru =   (410,350)
positionTextePays =     (470,450)


while continuerChoixTheme:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        #Gestion des appuis touche (+ conversion QWERTY => AZERTY)
        if event.type == KEYDOWN:
            carac= event.dict['unicode']
            if carac == '1' :
                jeu.creationListeDeMots("chiens")
                continuerChoixTheme = False
            elif carac == '2':
                jeu.creationListeDeMots("fruits")
                continuerChoixTheme = False
            elif carac == '3':
                jeu.creationListeDeMots("instruments")
                continuerChoixTheme = False
            elif carac == '4':
                jeu.creationListeDeMots("pays")
                continuerChoixTheme = False

    texteChoix  = police.render("Choix du thème", 1, (255,0,255))
    texteChiens = police.render("1:Chiens", 1, (255,0,0))
    texteFruits = police.render("2:Fruits", 1, (255,0,0))
    texteInstru = police.render("3:Instruments", 1, (255,0,0))
    textePays   = police.render("4:Pays", 1, (255,0,0))


    fenetre.blit(fondTheme,(0,0))

    fenetre.blit(texteChoix , positionTexteChoix)
    fenetre.blit(texteChiens, positionTexteChiens)
    fenetre.blit(texteFruits, positionTexteFruits)
    fenetre.blit(texteInstru, positionTexteInstru)
    fenetre.blit(textePays  , positionTextePays)

    pygame.display.flip()

    sleep(0.2)


#   Fenetre de fin && programme principal
##  Position sur la fenêtre
positionImagePendu =    (0, 50)
positionThemeChoisi =   (720,120)
positionLettresTappees =(500,360)
positionAffichageMot =  (500,550)


jeu.selectionMot()
jeu.affichageComplet()
lettreATester = list()
#BOUCLE DE JEU
continuerJeu = True
while continuerJeu :
    #Gestion des évenement (fermer et appui touche)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        #Gestion des appuis touche (+ conversion QWERTY => AZERTY)
        if event.type == KEYDOWN:
            carac= event.dict['unicode']
            carac = carac.upper()
            jeu.lettreJoueePresente(carac)


            #   S'éxécute uniquement quand j'appuie sur une touche

            jeu.affichageComplet()


    themeChoisi = police.render(jeu.themeChoisi, 1, (255,255,255))
    lettreTap = police.render(str(jeu.lettreTappeesSTR), 1, (255,255,0))
    mot = police.render(jeu.motAAfficher, 1, (66,255,66))

    fenetre.blit(fondJeu,(0,0))

    fenetre.blit(themeChoisi,positionThemeChoisi)
    fenetre.blit(lettreTap, positionLettresTappees)
    fenetre.blit(mot, positionAffichageMot)

    lienImagePendu = ".\\images pendu\\{}.png".format(7-jeu.nbDeCoupsRestants)
    image = pygame.image.load(lienImagePendu)

    fenetre.blit(image, positionImagePendu)


    pygame.display.flip()

    if jeu.nbDeCoupsRestants == 0:
        sleep(1)
        lienImagePendu = ".\\images pendu\\8.png"
        image = pygame.image.load(lienImagePendu)
        fenetre.blit(image, positionImagePendu)
        pygame.display.flip()
        sleep(1)
        lienImagePendu = ".\\images pendu\\9.png"
        image = pygame.image.load(lienImagePendu)
        fenetre.blit(image, positionImagePendu)
        pygame.display.flip()
        sleep(1.5)
    else:
        sleep(0.2)


    if jeu.partieGagnee() or jeu.partiePerdue() : continuerJeu = False



#   Fenetre de fin
##  Position sur la fenêtre
positionTexteDeFin = (400,500)
positionPhrase = (400,150)
positionMot = (400,250)


continuerFin = True
while continuerFin:
    if jeu.partieGagnee():
        fenetre.fill(0x00FF00)
        texteDeFin = "GAGNE"

    if jeu.partiePerdue():
        fenetre.fill(0xFF0000)
        texteDeFin = "PERDU"

    for event in pygame.event.get():
        if event.type == QUIT:
            continuerFin = False


    phrase = police.render("Le mot était", 1, (255,0,255))
    mot = police.render(jeu.motATrouver, 1, (255,0,255))
    texteDeFin = police.render(texteDeFin, 1, (255,255,255))

    fenetre.blit(phrase, positionPhrase)
    fenetre.blit(mot, positionMot)
    fenetre.blit(texteDeFin, positionTexteDeFin)


    pygame.display.flip()

    sleep(0.5)

pygame.quit()







