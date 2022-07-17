#import the pygame module

import pygame
import os
import random
import shelve

pygame.init()
#need to initialize this to call the font library
pygame.font.init()

FPS = 60
FPS_clock = pygame.time.Clock()

#setting up window
WIDTH, HEIGHT = 800,600
window = pygame.display.set_mode((WIDTH,HEIGHT))

#setting up caption
pygame.display.set_caption('Soonmoo')

#images
#soonmoo_image = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\fat_moo.png')
soonmoo_image = pygame.image.load(os.path.join("images","fat_moo.png"))
#donut_image = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\donut.png')
donut_image = pygame.image.load(os.path.join("images","donut.png"))
#cupcake_image = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\cupcake.png')
cupcake_image = pygame.image.load(os.path.join("images","cupcake.png"))
#ammo_image = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\pawprint2.png')
ammo_image = pygame.image.load(os.path.join("images","pawprint2.png"))
#donut_ammo = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\shit2.png')
donut_ammo = pygame.image.load(os.path.join("images","shit2.png"))
#spell = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\heal.png')
spell = pygame.image.load(os.path.join("images","heal.png"))
#menu1 = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\mooface1.png')
menu1 = pygame.image.load(os.path.join("images","mooface1.png"))
#menu2 = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\mooface2.png')
menu2 = pygame.image.load(os.path.join("images","mooface2.png"))
#menu3 = pygame.image.load(r'C:\Users\Anthony Fung\Documents\Summer 2020\mooface3.png')
menu3 = pygame.image.load(os.path.join("images","mooface3.png"))

class character:
    #half a second, before you can shoot again
    #this is similar to a static member in C++,
    #where there is only one version of this attribute for all the objects instantiated from this class
    #cooldown = 30
    def __init__(self, x, y):
        self.cool_down = 30
        self.image = None
        self.ammo_img = None
        self.x = x
        self.y = y
        self.cool_down_counter = 0
        self.ammo_list = []
        self.ammo_vel = None
        self.health = 100

    def draw(self):
        window.blit(self.image,(self.x, self.y))
        #draw ammo
        for ammo in self.ammo_list:
            ammo.draw()

    #obj represents soonmoo, we are seeing if the donut ammo collides with soonmoo
    def move_ammo(self, obj):
        self.cooldown()
        for ammo in self.ammo_list:
            ammo.move(self.ammo_vel)
            if ammo.y > 580:
                self.ammo_list.remove(ammo)
            elif ammo.collision(obj):
                self.ammo_list.remove(ammo)
                obj.health -= 10

    def shoot(self):
        if self.cool_down_counter == 0:
            #create ammo object and add it to the ammo list
            ammo_obj = ammo(self.x + self.ammo_offset, self.y, self.ammo_img)
            self.ammo_list.append(ammo_obj)
            #start counting after you have created the ammo
            self.cool_down_counter = 1

    def cooldown(self):
        if self.cool_down_counter >= self.cool_down:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def healthbar(self):
        #red rectangle
        pygame.draw.rect(window,(255,0,0),(self.x, self.y + 74, 70, 8))
        #green rectangle
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + 74, 70 * (self.health / 100), 8))

class cat(character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = soonmoo_image
        self.ammo_img = ammo_image
        self.ammo_offset = 29
        self.mask = pygame.mask.from_surface(self.image)
        self.ammo_vel = -3
        self.my_score = 0

    # overwriting the parent class function
    # this checks if the soonmoo ammo collided with the donuts (hence objs)
    def move_ammo(self, objs):
        self.cooldown()
        # we need to check if each ammo shot by soonmoo will collide with any objs (donuts)
        for ammo in self.ammo_list:
            ammo.move(self.ammo_vel)
            # check if out of bounds, if so, remove
            if ammo.y < 0:
                self.ammo_list.remove(ammo)
                continue
            for obj in objs:
                #check if obj (donuts) collided with soonmoo ammo
                if ammo.collision(obj):
                    #remove soonmoo ammo if it hits an enemy
                    self.ammo_list.remove(ammo)
                    obj.health -= 10
                    if obj.health <= 0:
                        self.my_score += 10
                        objs.remove(obj)

    def draw(self):
        super().draw()
        self.healthbar()

class enemy(character):
    def __init__(self, x, y, vel):
        #this inherits the properties, methods (functions) and attributes (variables) of the parent class
        super().__init__(x, y)
        self.image = donut_image
        self.ammo_img = donut_ammo
        self.mask = pygame.mask.from_surface(self.image)
        self.vel = vel
        self.ammo_vel = random.randint(2, 4)

        #when the object is created, each object donut can shoot every 1 second to 4 seconds
        #intervals are randomized
        self.cool_down = random.randint(60,240)
        self.ammo_offset = 10
        self.health = 10

    def move(self):
        self.y += self.vel

    def offscreen(self):
        return self.y >= 570

#second enemy (cupcake)
class enemy2(character):
    def __init__(self, x, y, velx, vely):
        super().__init__(x, y)
        self.image = cupcake_image
        self.ammo_img = donut_ammo
        self.mask = pygame.mask.from_surface(self.image)
        self.velx = velx
        self.vely = vely
        self.ammo_vel = 3
        self.cool_down = 180
        self.ammo_offset = 10
        self.health = 20

    def move(self):
        self.y += self.vely
        self.x += self.velx
        if self.x >= 770:
            self.velx *= -1
        elif self.x <= 0:
            self.velx *= -1

    def offscreen(self):
        return self.y >= 570

    def healthbar(self):
        #red rectangle
        pygame.draw.rect(window,(255,0,0),(self.x, self.y + 42, 32, 3))
        #green rectangle
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + 42, 32 * (self.health / 20), 3))

    def draw(self):
        super().draw()
        self.healthbar()

class ammo:
    def __init__ (self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
    def draw(self):
        window.blit(self.image, (self.x, self.y))
    def move(self, vel):
        self.y += vel
    def collision(self, obj):
        return collide(self, obj)

#heal spell
class power_up(ammo):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.vel = 2
    def move(self):
        self.x += self.vel
    def collision(self, obj):
        return collide(self, obj)
    def offscreen(self):
        return self.x > 770

#universal function, doesn't below to any class
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x, offset_y)) != None

#using global variables
expand = -200
bound_lim = -1500

def main():
    running = True
    lives = 1
    level = 0
    score = 0
    highscore = 0

    #starting wave size for donut
    wave = 5
    #starting wave size for cupcake
    wave2 = 1
    #wave list for donuts
    donut_wave = []
    #wave list for cupcakes
    cc_wave = []
    #list for potion
    potion_list = []
    # soonmoo's velocity (x only), there is no y velocity
    smx_change = 0
    lost = False
    lost_counter = 0
    # create font for score, level, lives
    my_font = pygame.font.SysFont('calibri', 20)
    #font for the lost message
    lost_font = pygame.font.SysFont('calibri',50)

    lost_label = lost_font.render("Game Over", 1, (0,0,0))

    #created a cat object called soonmoo
    #initial position x=360,y=500, image defined
    soonmoo = cat(360,500)

    #created donut and cupcake objects and pushed them into a list (vector)
    #randomized the initial position
    def generate_enemy():
        #need to say these are global so that the program will know to use these
        #or else it will think they are local and produce an error
        global expand
        global bound_lim
        for i in range(wave):
            donut = enemy(random.randrange(50, 750), random.randrange(bound_lim,-100), 1)
            donut_wave.append(donut)
        #this will generate the cupcakes at level 3 since the if condition checks:
        #if the cc_wave list is empty AND the level is 2,
        #then that means these will be generated, and come on screen when the level is 3
        if level >= 2:
            #print("generate")
            for i in range(wave2):
                cupcake = enemy2(random.randrange(50, 750), random.randrange(bound_lim,-100), 2, 1)
                cc_wave.append(cupcake)
        #expand the range that enemies can generate in so that they are less clustered as the wave gets bigger
        bound_lim += expand

    def generate_power_up():
        potion = power_up(random.randrange(-1500,-100), random.randrange(30,350), spell)
        potion_list.append(potion)

    def redraw_win():
        window.fill((173, 216, 230))

        # call the draw method in the character class for object soonmoo
        soonmoo.draw()

        #draw the donuts objects in the list one by one
        for i in range(len(donut_wave)):
            donut_wave[i].draw()

        #draw the cupcake objects in the list one by one
        for i in range(len(cc_wave)):
            cc_wave[i].draw()

        if len(potion_list) > 0:
            potion_list[0].draw()

        lives_label = my_font.render(f"lives : {lives}", 1, (0,0,0))
        level_label = my_font.render(f"level : {level}", 1, (0,0,0))
        score_label = my_font.render(f"score : {score}", 1, (0,0,0))

        window.blit(lives_label, (50, 10))
        window.blit(level_label, (670, 10))
        window.blit(score_label, (360, 10))

        if lost:
            window.blit(lost_label, (400 - lost_label.get_width() / 2, 250))

            #open file which is a dict
            s = shelve.open('highscore_data')
            #access the score that's inside the file and store it to a var called highscore
            highscore = s['hs']

            s.close()

            highscore_label = lost_font.render(f"highscore : {highscore}", 1, (0,0,0))
            window.blit(highscore_label, (400 - highscore_label.get_width() / 2, 300))

        # This will make the surface object returned from pygame.display.set_mode() appear on the screen
        # which in this case is the variable window
        # blit command copies and pastes images onto the surface object, window
        # that is why when you delete this command, the screen is black
        pygame.display.update()

    while running:

        redraw_win()
        FPS_clock.tick(FPS)

        if lives == 0:
            lost = True

        if lost:
            #open the file
            s = shelve.open('highscore_data')
            #if the current score is greater than the one stored in the file
            if not s or s['hs'] < score:
                #update the file with the newer highscore
                s['hs'] = score

            s.close()

            if lost_counter < FPS * 3:
                lost_counter += 1
                continue
            else:
                running = False

        #if all the enemy of the current wave is passed (enemy wave is 0)
        #generate the enemies, and increase wave size for the next wave
        if len(donut_wave) == 0 and len(cc_wave) == 0:
            generate_enemy()
            wave += 1
            if level >= 2:
                wave2 += 1
            level += 1
            # generate heal spell every 5 levels
            if level % 5 == 0:
                generate_power_up()

        #if soonmoo's health is zero, refill the health bar and decrement the lives
        if soonmoo.health <= 0:
            lives -= 1
            soonmoo.health = 100

        #this keeps updating the score every loop
        #if soonmoo ammo collides with the enemy, soonmoo.my_score will increment by 10
        score = soonmoo.my_score

        for event in pygame.event.get():
            #if we press 'x' on the top right corner of the window, exit loop
            if event.type == pygame.QUIT:
                running = False

        #dictionary (map) gets called
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            smx_change = -5
        if key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            smx_change = 5
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            smx_change = 0
        if key[pygame.K_SPACE]:
            soonmoo.shoot()

        soonmoo.x += smx_change
        if soonmoo.x > 730:
            soonmoo.x = 730
        if soonmoo.x < 5:
            soonmoo.x = 5

        #if donut goes off the screen, remove it from the enemy list (donut_wave)
        #decrease lives
        #this checks all enemies on enemy list
        n = 0
        while n < len(donut_wave):
            if donut_wave[n].offscreen() or collide(soonmoo,donut_wave[n]):
                if donut_wave[n].offscreen():
                    lives -= 1
                else:
                    #if the donuts collide with soonmoo, do more damage (20)
                    soonmoo.health -= 20
                donut_wave.remove(donut_wave[n])
            else:
                n += 1

        m = 0
        while m < len(cc_wave):
            if cc_wave[m].offscreen() or collide(cc_wave[m],soonmoo):
                if cc_wave[m].offscreen():
                    lives -= 1
                else:
                    soonmoo.health -= 30
                cc_wave.remove(cc_wave[m])
            else:
                m += 1

        for i in range(len(donut_wave)):
            donut_wave[i].move()
            if donut_wave[i].y > 0:
                donut_wave[i].shoot()
                donut_wave[i].move_ammo(soonmoo)

        for i in range(len(cc_wave)):
            cc_wave[i].move()
            if cc_wave[i].y > 0:
                cc_wave[i].shoot()
                cc_wave[i].move_ammo(soonmoo)

        #check if soonmoo ammo has collided with the heal potion
        #if so, set soonmoo's health back to 100 and remove the potion
        if len(potion_list) > 0:
            potion_list[0].move()
            for i in range(len(soonmoo.ammo_list)):
                if potion_list[0].collision(soonmoo.ammo_list[i]):
                    potion_list.remove(potion_list[0])
                    soonmoo.health = 100
                    break
                elif potion_list[0].offscreen():
                    potion_list.remove(potion_list[0])
                    break

        #note that the bullets will be twice as fast as we set them to
        #since we called move_ammo twice
        #it needs to be called twice for collision detection of both enemy types
        soonmoo.move_ammo(donut_wave)
        soonmoo.move_ammo(cc_wave)

def menu():
    run = True
    menu_font = pygame.font.SysFont('calibri',50)
    menu_font2 = pygame.font.SysFont('calibri',30)
    menu_label = menu_font.render('Press [S] to Play', 1, (0,0,0))
    menu_label2 = menu_font2.render('[<-][->] to Move', 1, (0,0,0))
    menu_label3 = menu_font2.render('[SPACE] to Shoot', 1, (0,0,0))

    while run:
        window.fill((173, 216, 230))
        window.blit(menu_label, (400 - menu_label.get_width() / 2, 200))
        window.blit(menu_label2, (400 - menu_label2.get_width() / 2, 250))
        window.blit(menu_label3, (400 - menu_label3.get_width() / 2, 280))
        window.blit(menu1, (500, 374))
        window.blit(menu2, (100, 374))
        window.blit(menu3, (300, 10))
        for event in pygame.event.get():
            #if we press 'x' on the top right corner of the window, exit loop
            if event.type == pygame.QUIT:
                run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            main()
        pygame.display.update()
#calling the function "menu" which calls the main if key p is pressed
menu()