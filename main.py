import subprocess
import pygame
import sys
import os
from entities import *

# Set up display
pygame.init()
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moral Compass")
clock = pygame.time.Clock()

question1 = ("1. Would you like to steal a loaf of bread to feed your starving family?", [("yes","actions([[stole,1],[helped_someone,5]])."), ("no","actions([[rejected_stole,1],[rejected_helped_someone,5]]).")])
question2 = ("2. Would you like to help an old lady cross the street?", [("yes","actions([[helped_someone,1]])."), ("no","actions([[rejected_helped_someone,1]]).")])
question3 = ("3. Would you like to join us in robbing this bank?", [("yes", "actions([[stole, 5]])."), ("no","actions([[rejected_stole,5]]).")]) 
question4 = ("4. Would you like to donate to charity?", [("yes", "actions([[donated_to_charity, 1], [helped_someone, 5], [saved_a_life, 5]])."), ("no","actions([[rejected_donated_to_charity,1], [rejected_helped_someone, 5], [rejected_saved_a_life, 5]]).")])
question5 = ("5. I can't afford to have these new pups, would you be willing to adopt them?", [("yes", "actions([[adopted_a_pet, 2], [saved_a_life, 2]])."),("no","actions([[rejected_adopted_a_pet, 2], [rejected_saved_a_life, 2]]).")]) 
question6 = ("6. I have the questions for the next exam, would you like them?", [("yes", "actions([[cheated, 1]])."),("no","actions([[rejected_cheated, 1]]).")])
question7 = ("7. I know it's your day off, but if you go to work today you save the whole world, will you go to work?", [("yes","actions([[went_to_work, 1], [saved_the_world, 1]])."),("no","actions([[rejected_went_to_work, 1], [rejected_saved_the_world, 1]]).")])

# Entities
player = Player("./resources/protagonistL.jpg","./resources/protagonistR.jpg",(120,120),screen_width/2-50,screen_height/2-50)
npc1 = Entity("./resources/loaf_of_bread.jpg",(200,200),200,200,question1)
npc2 = Entity("./resources/old_woman.jpg",(200,200),220,500,question2)
npc3 = Entity("./resources/bank.jpg",(200,200),500,800,question3)
npc4 = Entity("./resources/charity.jpg",(200,200),900,750,question4)
npc5 = Entity("./resources/puppies.jpg",(200,200),1300,700,question5)
npc6 = Entity("./resources/testanswers.jpg",(200,200),1600,600,question6)
npc7 = Entity("./resources/savetheworld.jpg",(200,200),1650,200,question7)
background = Entity("./resources/background.jpg",(1920,1080),0,0,"")
moralend = Entity("./resources/moral_end.jpg",(1920,1080),0,0,"")
immoralend = Entity("./resources/immoral_end.jpg",(1920,1080),0,0,"")

entitylist = pygame.sprite.Group()
# entitylist.add(background)
entitylist.add(npc1)
entitylist.add(npc2)
entitylist.add(npc3)
entitylist.add(npc4)
entitylist.add(npc5)
entitylist.add(npc6)
entitylist.add(npc7)

# Text and Menus
moral_msg = Text([screen_width/2,screen_height/2-100],"Congratulations, you are a moral utilitarian!",'freesansbold.ttf',50,(0,0,0))
immoral_msg = Text([screen_width/2,screen_height/2-100],"Unfortunately, you are an immoral utilitarian",'freesansbold.ttf',50,(255,255,255))
header = Text([screen_width/2,50],"Morality Meter: 0",'freesansbold.ttf',50,(255,255,255))

# Main game loop
running = True
endScreen = False

morality = 0

while running:
    if entitylist.__len__() == 0 and not endScreen:
        header.update("Your overall morality is: " + morality)
        endScreen = True

    if endScreen:
        if int(morality) >= 0:
            header.color = (0,0,0)
            header.center = [screen_width/2,screen_height/2]
            header.update("Your overall morality is: " + morality)
        else:
            header.color = (255,255,255)
            header.center = [screen_width/2,screen_height/2]
            header.update("Your overall morality is: " + morality)
        if int(morality) >= 0:
            moralend.draw(screen)
            moral_msg.blit(screen)
        else:
            immoralend.draw(screen)
            immoral_msg.blit(screen)
        header.blit(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
    else:
        # Update game state
        entitylist.update()

        # Draw everything
        screen.fill((0,0,0))
        background.draw(screen)
        entitylist.draw(screen)
        player.draw(screen)
        header.blit(screen)

        # Check for collision for questions
        for sprite in entitylist:
            if sprite.rect.colliderect(player.questionrect):
                sprite.question.update()
                sprite.question.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for sprite in entitylist:
                        if sprite.rect.colliderect(player.questionrect):
                            mousepos = pygame.mouse.get_pos()
                            # print(mousepos)
                            for button in sprite.question.buttons:
                                # print("left:",button.left,"right:",button.right,"top:",button.top,"bottom:",button.bottom)
                                if button.left <= mousepos[0] <= button.right and button.top <= mousepos[1] <= button.bottom:
                                    button.clicked = True
                                    with open("data.pl","a") as f:
                                        f.write(button.result+"\n")
                                    print(button.result)
                            entitylist.remove(sprite)
                            try:
                                result = subprocess.run(
                                    # swipl -g "moral_action(stole,Score)." -t halt test.pl
                                    ["swipl", "-g", "find_morality(Total).", "-t", "halt", "core_logic.pl"],
                                    capture_output=True,
                                    text=True,
                                    check=True,
                                )
                                print("Command Output:")
                                print(result.stdout)
                                morality = result.stdout.strip()
                                header.update("Morality Meter: " + morality)
                            except subprocess.CalledProcessError as e:
                                print("Error calling command:", e.stderr)
        
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if keys[pygame.K_a]:
            player.changeLeft()
            move_x = 8
        if keys[pygame.K_d]:
            player.changeRight()
            move_x = -8
        if keys[pygame.K_w]:
            move_y = 8
        if keys[pygame.K_s]:
            move_y = -8

        # Check for collisions before moving entities
        collision = False
        for sprite in entitylist:
            sprite.rect.x += move_x
            sprite.rect.y += move_y
            if pygame.sprite.collide_rect(player, sprite):
                collision = True
            sprite.rect.x -= move_x
            sprite.rect.y -= move_y
        if not collision:
            for sprite in entitylist:
                sprite.rect.x += move_x
                sprite.rect.y += move_y
            background.rect.x += move_x
            background.rect.y += move_y

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
if os.path.exists("data.pl"):
    os.remove("data.pl")
pygame.quit()
sys.exit()