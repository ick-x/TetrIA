import pygame as pygame
import pygame.font

pygame.init()

largeur_ecran = 1280
hauteur_ecran = 780
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Écran d'Accueil")


police = pygame.font.Font(None, 36)  # Police de caractères, taille de 36
couleur_texte = (255, 255, 255)

#Création du texte
texte_start = police.render("Start", True, couleur_texte)
texte_record = police.render("Record", True, couleur_texte)
texte_leave = police.render("Leave", True, couleur_texte)

#Load de la photo
image_accueil = pygame.image.load("tetris_logo.png")

#Largeur et hauteur de l'image
largeur_image = 400
hauteur_image = 400

#Largeur et hauteur des boutons
largeur_bouton = 200
hauteur_bouton = 50 

x_image = (largeur_ecran - largeur_image) // 2 + 40
y_image = (hauteur_ecran - hauteur_image) // 2

x_bouton_start = (largeur_ecran - largeur_bouton) // 2
y_bouton_start = 400 # Espace de 20 pixels sous l'image

x_bouton_record = (largeur_ecran - largeur_bouton) // 2
y_bouton_record = y_bouton_start + hauteur_bouton + 10  # Espace de 10 pixels entre les boutons

x_bouton_leave = (largeur_ecran - largeur_bouton) // 2
y_bouton_leave = y_bouton_record + hauteur_bouton + 10  # Espace de 10 pixels entre les boutons

bouton_start = pygame.Rect(x_bouton_start, y_bouton_start, 200, 50)
bouton_record = pygame.Rect(x_bouton_record, y_bouton_record, 200, 50)
bouton_leave = pygame.Rect(x_bouton_leave,y_bouton_leave,200,50)

#Centrage du texte sur les boutons
rect_texte_start = texte_start.get_rect()
rect_texte_start.center = bouton_start.center

rect_texte_record = texte_record.get_rect()
rect_texte_record.center = bouton_record.center

rect_texte_leave = texte_leave.get_rect()
rect_texte_leave.center = bouton_leave.center


en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    ecran.fill("black")
    ecran.blit(image_accueil, (x_image, y_image))

    # Dessinez les boutons
    pygame.draw.rect(ecran, (0, 255, 0), bouton_start)  # Couleur verte pour le bouton "Start"
    pygame.draw.rect(ecran, (255, 0, 0), bouton_record)  # Couleur rouge pour le bouton "Record"
    pygame.draw.rect(ecran, (0, 0, 255), bouton_leave) 

    # Dessinez le texte sur les boutons
    ecran.blit(texte_start, rect_texte_start)
    ecran.blit(texte_record, rect_texte_record)
    ecran.blit(texte_leave, rect_texte_leave)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_start.collidepoint(event.pos):
                # Action lorsque le bouton "Start" est cliqué
                print("Bouton Start cliqué")
            elif bouton_record.collidepoint(event.pos):
                # Action lorsque le bouton "Record" est cliqué
                print("Bouton Record cliqué")
            elif bouton_leave.collidepoint(event.pos):
                # Action lorsque le bouton "Leave" est cliqué
                print("Bouton Leave cliqué")
                pygame.quit()
