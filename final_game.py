"""importing modules"""
import pygame as pg
import random as rd
import sys
import os

"""
opening the right path
make sure that the Resources folder is in the folder with the code

"""

folder_with_sprites = os.sep + 'Resources' + os.sep
path_to_code = os.getcwd()
folder_with_code =  os.path.basename(path_to_code)
path = path_to_code + os.path.join(folder_with_code , folder_with_sprites)

"""main game settings"""
WIDTH = 1000 #width of screen
HEIGHT = 572 #height of screen
FPS = 20  #may need adjusting depending on what type of computer the code is run on
GRAVITY = 2 #makes a jump look more realistic

# defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

"""initializing pygame and creating a window"""
pg.init()
pg.mixer.init()
pg.display.init()
pg.font.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Graveyard Archeress Alpha") #naming the game
clock = pg.time.Clock() #setting a clock

"""downloading sound effects and background music"""
start= pg.mixer.Sound( path +'Destroy.wav')
start.play()
bgmusic = pg.mixer.music.load( path +'Memoraphile - Spooky Dungeon.mp3')
pg.mixer.music.play(-1)

arrow_shotSound = pg.mixer.Sound( path + 'arrow.wav')
zombie_hitSound = pg.mixer.Sound( path + 'zombiehit.wav')
ork_hitSound = pg.mixer.Sound( path + 'orkhit.wav')
bigboss_hitSound = pg.mixer.Sound( path + 'bigbosshit.wav')
player_hitSound = pg.mixer.Sound(path +'playerhit.wav')
potion_collectSound =  pg.mixer.Sound(path +'potion.wav')

lostSound =  pg.mixer.Sound(path +'gameover.wav')
winSound = pg.mixer.Sound(path +'win.wav')


"""---------------------------------------------------

Creating the ground, platforms and borders

----------------------------------------------------"""
all_sprites = pg.sprite.Group() #creating a list where all the sprites will go

"""creating the ground"""

groundimg = pg.image.load( path + 'ground.png').convert_alpha() #ground tile image

class Ground(pg.sprite.Sprite):
    """sprite for the groundtiles"""
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = groundimg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#assigning the ground tile multiple positions so that it covers the whole bottom of the screen
def ground(x,y,w,h):
    """creating several tiles for the ground, returns a list with all the tiles"""
    ground_tiles = pg.sprite.Group()
    i = 0
    while i < len(gr_loc):
        ground = Ground(gr_loc[i], HEIGHT-ty, tx, ty)
        ground_tiles.add(ground)
        i = i+1

    return ground_tiles

gr_loc = [] #ground location
tx   = 64 #tile width
ty   = 64 #tile height

i  = 0
while i <= (WIDTH/tx)+tx: 
    gr_loc.append(i*tx)
    i = i+1

ground_tiles = ground( gr_loc, HEIGHT - ty,  tx, ty) #calling the ground fucntion to return the list with the groundtiles
all_sprites.add(ground_tiles) #adding the ground to all the sprites

"""creating the platforms"""

platform_img = pg.image.load( path + 'platform1.png').convert_alpha() #platform image

class Platform(pg.sprite.Sprite):
    """sprite for the platforms"""
    def __init__(self, sx, x, y, move):
        pg.sprite.Sprite.__init__(self)
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.startx = sx
        self.rect.x = x
        self.rect.y = y
        self.move = move
        self.speed = 10

    def update(self):
        if self.move == True:
            self.rect.x += self.speed 
        if self.rect.x > self.startx + 150:
            self.speed = self.speed * -1
        elif self.rect.x < self.startx - 50:
            self.speed = self.speed * -1

def platform():
    """returns a list of all platforms created inside"""
    platforms = pg.sprite.Group()
    
    plat1 = Platform(50, 50, 90, False)
    plat2 = Platform(190, 190, 220, True)
    plat3 = Platform(180, 180, 390, False)
    plat4 = Platform(600, 600, 370, False)
    plat5 = Platform(710, 710, 250, True)
    plat6 = Platform(650, 650, 90, False)
    plat7 = Platform(1000, 1000, 400, False)
    plat8 = Platform(1550, 1550, 80 , False)
    plat9 = Platform(1700, 1700, 190, False)
    plat10 = Platform(1250, 1250, 300 , True)
    plat11 = Platform(1750, 1750, 400 , True)
    plat12 = Platform(-250, -250, 380 , True)
    
    platforms.add(plat1, plat2, plat3, plat4, plat5, plat6, plat7, plat8, plat9, plat10, plat11, plat12)
        
    return platforms

platforms = platform() #calling the platform function to return the list with platforms
all_sprites.add(platforms) #adding the platforms to all the sprites

"""creating the borders"""

#the border images
signR = pg.image.load( path + 'ArrowSign.png').convert_alpha() #points right
signL = pg.image.load( path + 'ArrowSignL.png').convert_alpha() #points left

class BorderR(pg.sprite.Sprite):
    """sprite for the border on the right side"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = signL
        self.rect = self.image.get_rect()
        self.rect.x = 3000
        self.rect.y = HEIGHT -  ty - self.rect.height

    def update(self):
        """this is how the player is stopped from moving further than the border"""
        if player.rect.right > self.rect.left:
           player.rect.right = self.rect.left

class BorderL(pg.sprite.Sprite):
    """sprite for the border on the left side"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = signR
        self.rect = self.image.get_rect()
        self.rect.x = -1000
        self.rect.y = HEIGHT -  ty - self.rect.height

    def update(self):
        """this is how the player is stopped from moving further than the border"""
        if player.rect.left < self.rect.right:
           player.rect.left = self.rect.right

borderR = BorderR() #returns the border
all_sprites.add(borderR) #adds border to all the sprites
borderL = BorderL()
all_sprites.add(borderL)


"""------------------------------------------------------

Creating the game player, enemies and attacks

-------------------------------------------------------"""

"""creating the player"""

playr_right = [pg.image.load( path + f'mainR{frame}.png') for frame in range(5)] #player animations
playr_left = [pg.image.load( path + f'mainL{frame}.png') for frame in range(5)]
playr_leftfacing = pg.image.load( path + 'mainFL.png') #player image facing the left side
playr_rightfacing = pg.image.load( path + 'mainFR.png') #player image facing the right side

class Player(pg.sprite.Sprite):
    """sprite for the player"""
    def __init__(self, score):
        # this line is required to properly create the sprite
        pg.sprite.Sprite.__init__(self)
        # download the sprite image
        self.image = playr_rightfacing
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        #position the sprite
        self.rect.x = 100
        self.rect.y = HEIGHT - ty - self.rect.height + 1
        #assign speed variables in the x and y positions
        self.velx = 0
        self.vely = 0
        self.frame = 0 #assign frame of animation
        self.isJumping = False
        self.isStanding = False
        self.falling = False
        self.score = score
        self.health = 100
        self.streak = 0 
        self.PUCount = 0 #counts the powerups acquired
        self.facing = 1 #checks which side the player is facing
        
    def control(self, x):
        """
        movement/speed of the player in the horizontal directions
        controlled by the keys on the keyboard
        """
        self.velx += x

    def update(self):
        """
        any code here will happen every time the game loop updates
        this update section contains the sprite animation for the player,
        the collision with platforms, the ground, and the sides
        """

        #kill the player if healthbar is empty
        if self.health <= 0:
            self.kill()

        #moving left animation
        if self.velx < 0:
            self.frame += 1
            if self.frame +1 > 15:
                self.frame = 0
            self.image = playr_left[self.frame //3]
            self.facing = -1
            
        #moving right animation
        elif self.velx > 0:
            self.frame += 1
            if self.frame +1> 15:
                self.frame = 0
            self.image = playr_right[self.frame//3]
            self.facing = 1


        if self.rect.right > WIDTH:
           self.rect.right = WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0

        #updates position of player on the x-axis
        self.rect.x += self.velx

        #when hitting the bottom of the platforms when jumping up we need to fall to the ground again:
        if self.falling:
            self.vely = 10 #speed in the y direction downwards
            self.vely += GRAVITY #acceleration
            self.rect.y += self.vely * GRAVITY #updating the player position with the fall movements
            self.falling = False #setting falling to false again, otherwise it would stay true and the player wouldn't be able to jump

        if not self.isJumping: #if the player is not jumping already, we can start a jump
            self.vely += GRAVITY
            self.rect.y += self.vely * GRAVITY 
            self.isStanding = False #the player is not standing
            """
            if player jumps and falls and then passes the ground or platforms,
            we need the jump to stop and the player to land on the ground/platform:
            """
            if pg.sprite.spritecollide(self, ground_tiles, False, False): #we only ever collide with the top of the ground, so this function is fine
                self.rect.y =  HEIGHT - ty - self.rect.height + 1 #adjust position of player
                self.vely = 0 #change the jumping speed to 0
            elif self.collidetop(): #for the platforms, we can collide from any direction, so this needs to be a little different
                self.adjust_collision_top() #adjust the position of the player to land on the platform, instead of going through it
                self.vely = 0 #change the jumping speed to 0

        self.adjust_collision_bottom() #need to call on functions to be able to happen every iteration
        self.player_hit()
        self.enemy_hit()
        self.enemy_hitpu()

    def collidetop(self):
        """if the player collides with the top of a platform while falling, return True"""
        for platform in platforms:
            if self.rect.y + self.rect.height + self.vely >= platform.rect.top and self.vely > 0:
                if self.rect.y + self.rect.height + self.vely <= platform.rect.top + 60:
                    if platform.rect.x - 30 <= self.rect.x <= platform.rect.x + platform.rect.width - 30 :
                        return True
            
    def adjust_collision_top(self):
        """
        if the player collides with the top of a platform while falling,
        return the adjusted position on top of that platform
        """
        for platform in platforms:
            if self.rect.y + self.rect.height + self.vely >= platform.rect.top and self.vely > 0:
                if self.rect.y + self.rect.height + self.vely <= platform.rect.top + 30:
                    if platform.rect.x - 30 <= self.rect.x <= platform.rect.x + platform.rect.width - 30 :
                        self.rect.y = platform.rect.top - self.rect.height + 1
                        

    def adjust_collision_bottom(self):
        """
        if the player collides with the bottom of a platform while jumping,
        make the player bump the bottom and then fall
        """
        for platform in platforms:
            if platform.rect.bottom - 30 <= self.rect.y + (0.5 * self.rect.height) + self.vely <= platform.rect.bottom and self.vely < 0:
                if platform.rect.x - 30 <= self.rect.x <= platform.rect.x + platform.rect.width - 30:
                    self.rect.y = platform.rect.bottom
                    self.falling = True

    def jump(self):
        """if the player is not yet already jumping AND is standing (colliding), we can start a new jump"""
        if self.isJumping == False and self.isStanding == True:
            self.vely = -18

    def shoot(self):
        """lets the player shoot arrows by pressing space bar"""
        arrow = Arrow(self.rect.centerx, self.rect.centery, self.facing) #position and create arrow
        all_sprites.add(arrow)  #add arrow to all sprites
        arrows.add(arrow) #add the arrow to the arrows sprite list

    def enemy_hit(self):
        """ adds points if an arrow hits an enemy, also kills the enemy if their health bar is empty"""
        for arrow in arrows:
            for zombie in zombies:
                if arrow.rect.colliderect(zombie.rect):
                    zombie_hitSound.play() #plays the sound effect of the enemy getting hit
                    self.score+=1
                    if zombie.health > 10:
                        zombie.health -= 10
                    else:
                        zombie.kill()
                    self.streak += 1
                    arrow.kill()

            for ork in orks:
                if arrow.rect.colliderect(ork.rect):
                    ork_hitSound.play()
                    self.score +=1
                    if ork.health > 5:
                        ork.health -= 5
                    else:
                        ork.kill()
                    self.streak +=1
                    arrow.kill()
                    
            for bb in bigboss:
                if arrow.rect.colliderect(bb.rect):
                    bigboss_hitSound.play()
                    self.score +=1
                    if bb.health > 2:
                        bb.health -= 2
                    else:
                        bb.kill()
                    self.streak +=1
                    arrow.kill()

                
    def player_hit(self):
        """if the player collides with the enemy, the player respawns and loses points"""
        hits = pg.sprite.spritecollide(self, zombies, False, False) #checks collision
        if hits:
            self.rect.x = 50
            self.rect.y = 100
            self.score -= 5
            player_hitSound.play()
            if self.health > 0:
                self.health -= 10
            else:
                self.kill()
            
        hits1 = pg.sprite.spritecollide(self, orks, False, False)
        if hits1:
            self.rect.x = 50
            self.rect.y = 100
            self.score -= 5
            player_hitSound.play()
            if self.health > 0:
                self.health -= 10
            else:
                self.kill()
                
        hits2 = pg.sprite.spritecollide(self, bigboss, False, False)
        if hits2:
            self.rect.x = 50
            self.rect.y = 100
            self.score -= 5
            player_hitSound.play()
            if self.health > 0:
                self.health -= 20
            else:
                self.kill()
            
    def healthbar(self, window):
        """draws the healthbar of the player on the screen"""
        pg.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y - 20, 50, 10)) #red
        pg.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y - 20 , 50 - (0.5 * (100 - self.health)), 10)) #green on top

    def shoot_pu(self):
        powerup = PowerUp(self.rect.centerx, self.rect.centery, self.facing) #position and create power up
        all_sprites.add(powerup)  #add power up to all sprites
        powerups.add(powerup)

    def enemy_hitpu(self):
        """ adds points if a powerup hits an enemy, also kills the enemy if health bar empty"""
        for powerup in powerups:
            for zombie in zombies:
                if powerup.rect.colliderect(zombie.rect):
                    zombie_hitSound.play()
                    self.score+=1
                    self.streak +=1
                    zombie.kill()
                    powerup.kill()

            for ork in orks:
                if powerup.rect.colliderect(ork.rect):
                    ork_hitSound.play()
                    self.score +=1
                    if ork.health > 5:
                        ork.health -= 75
                    else:
                        ork.kill()
                    self.streak +=1
                    powerup.kill()

            for bb in bigboss:
                if powerup.rect.colliderect(bb.rect):
                    bigboss_hitSound.play()
                    self.score +=1
                    if bb.health > 20:
                        bb.health -= 20
                    else:
                        bb.kill()
                    self.streak +=1
                    powerup.kill()

#spawn the player
player = Player(0)
all_sprites.add(player)

"""creating the arrow attack"""

#arrow image
arrow_imgL = pg.image.load( path + 'arrowL.png').convert_alpha()
arrow_imgR = pg.image.load( path + 'arrowR.png').convert_alpha()

class Arrow(pg.sprite.Sprite):
    """sprite for the arrows"""
    def __init__(self, x, y, facing):
        pg.sprite.Sprite.__init__(self)
        self.image = arrow_imgR
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.facing = facing
        self.speedx = 35 * facing

    def update(self):
        """makes the arrow move on the screen"""
        self.rect.x += self.speedx 
        #kill if it moves off the right side of the screen
        if self.rect.right > WIDTH or self.rect.left <0:
            self.kill()
            player.streak = 0

        if self.facing < 0:
            self.image = arrow_imgL
        else:
            self.image =  arrow_imgR
            
arrows = pg.sprite.Group() #own group for collision

"""creating the powerup"""

#potion and powerup attack images
potion_img = pg.image.load( path + 'potion.png').convert_alpha()
powerup_imgR = pg.image.load( path + 'arrowFR.png').convert_alpha()
powerup_imgL =  pg.image.load( path + 'arrowFL.png').convert_alpha()

class Potion(pg.sprite.Sprite): #powerup acquiry
    """sprite for the potion that needs to be acquired to gain a powerup attack"""
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = potion_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if player.rect.colliderect(self.rect):
            self.kill()
            player.PUCount += 1
            potion_collectSound.play()
            
class PowerUp(pg.sprite.Sprite):
    """sprite for the powerup attack"""
    def __init__(self, x, y, facing):
        pg.sprite.Sprite.__init__(self)
        self.image = powerup_imgL
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.facing = facing
        self.speedx = 45 * facing
        
    def update(self):
        """makes the powerup move on the screen"""
        self.rect.x += self.speedx
        #kill if it moves of the right side of the screen
        if self.rect.right > WIDTH or self.rect.left <0:
            self.kill()

        if self.facing < 0:
            self.image = powerup_imgL
        else:
            self.image =  powerup_imgR

powerups = pg.sprite.Group() #own group for collision
#spawning powerups
pu = Potion(90, 50) 
pu1 = Potion(900, 250)
pu2  =  Potion(700, 50)
pu3 = Potion(450, 350)

powerups.add(pu, pu1, pu2, pu3)
all_sprites.add(pu, pu1, pu2, pu3)


"""creating the first enemy: zombies"""

#zombie animations
zombie_left =[pg.image.load( path + f'ZomL{frame}.png') for frame in range(6)]
zombie_right = [pg.image.load( path + f'ZomR{frame}.png') for frame in range(6)] #enemy animation
hurtR = pg.image.load( path + 'hurtR.png').convert_alpha()
hurtL =pg.image.load( path + 'hurtL.png').convert_alpha()

class Zombies(pg.sprite.Sprite):
    """sprite for the zombies"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = zombie_left[1]
        self.rect = self.image.get_rect()
        self.rect.x = rd.randrange(1050, 1500)
        self.rect.y = HEIGHT - ty - self.rect.height +5
        self.speedx = rd.randrange(-7,-3) #assign random speed
        self.frame = 0
        self.health = 100

    def update(self):
        """makes the enemy move and appear on the screen at random and have an animation"""
        self.rect.x += self.speedx
        if self.rect.left < 25: #before the zombie goes off the left side of the screen:
            self.speedx = rd.randrange(3,7) #change the speed to positive, so the zombie changes directions
        elif self.rect.right > WIDTH - 25: #right side
            self.speedx = rd.randrange(-7,-3)

        #animations moving left and right
        if self.speedx > 0:
            self.frame += 1
            if self.frame +1> 18:
                self.frame = 0
            self.image = zombie_right[self.frame//3]
    
        else:
            self.frame += 1
            if self.frame +1> 18:
                self.frame = 0
            self.image = zombie_left[self.frame//3]

    def healthbar(self, window):
        """creates the health bar of the zombie"""
        pg.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y - 20, 50, 10)) #red
        pg.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y - 20 , 50 - (0.5 * (100 - self.health)), 10)) #green on top

zombies = pg.sprite.Group()
#random spawning of the zombies
for i in range(3):
    z = Zombies()
    all_sprites.add(z)
    zombies.add(z)

"""creating the second enemy: orks"""

#animation
ork_left =  [pg.image.load( path + f'WL{frame}.png') for frame in range(7)]
ork_right =  [pg.image.load( path + f'WR{frame}.png') for frame in range(7)]

class Ork(pg.sprite.Sprite):
    """sprite for the orks"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = ork_left[2]
        self.rect = self.image.get_rect()
        self.rect.x = rd.randrange(2100, 2900)
        self.rect.y = HEIGHT - ty - self.rect.height + 5
        self.speedx = rd.randrange(-10,-5)
        self.frame = 0
        self.health = 100

    def update(self):
        """makes the enemy move and appear on the screen at random after first enemy is defeated + animation"""
        if not zombies:
            self.rect.x += self.speedx
            if self.rect.left < 0:
                self.speedx = rd.randrange(5,10)
            elif self.rect.right > WIDTH:
                self.speedx = rd.randrange(-10,-5)
                
        if self.speedx > 0:
            self.frame += 1
            if self.frame +1> 21:
                self.frame = 0
            self.image = ork_right[self.frame//3]

        elif self.speedx < 0:
            self.frame += 1
            if self.frame +1> 21:
                self.frame = 0
            self.image = ork_left[self.frame//3]
            

    def healthbar(self, window):
        """creates the health bar of the ork"""
        pg.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y - 20, 50, 10)) #red
        pg.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y - 20 , 50 - (0.5 * (100 - self.health)), 10)) #green on top

orks = pg.sprite.Group()
for i in range(3):
    o = Ork()
    all_sprites.add(o)
    orks.add(o)

"""creating the ultimate enemy: Desert Robot"""

#animations
bigboss_left = [pg.image.load( path + f'BbL{frame}.png') for frame in range(12)]
bigboss_right  =[pg.image.load( path + f'BbR{frame}.png') for frame in range(12)]

class BigBoss(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = bigboss_left[5]
        self.rect = self.image.get_rect()
        self.rect.x = 1800
        self.rect.y = HEIGHT - ty - self.rect.height + 15
        self.speedx = 17
        self.frame = 0
        self.health = 100
        self.canshoot = True
        self.facing =1
        
    def update(self):
        """
        makes the enemy move and appear on the screen at random
        after first and second enemy are defeated + animation
        """
        if not orks:
            self.rect.x += self.speedx
            if self.rect.left < 25:
                self.speedx = rd.randrange(15, 20)
            elif self.rect.right > WIDTH - 25:
                self.speedx = rd.randrange(-20,-15)

        if self.speedx > 0:
            self.facing = 1
            self.frame += 1
            if self.frame +1> 27:
                self.frame = 0
            self.image = bigboss_right[self.frame//3]

        elif self.speedx < 0:
            self.frame += 1
            self.facing = -1
            if self.frame+1 > 27:
                self.frame = 0
            self.image = bigboss_left[self.frame//3]

        #if the enemy can shoot, it will shoot and then not be able to shoot until variable is true again
        if self.canshoot: 
            self.enemy_attack()
            self.canshoot = False

        self.hit_player()

    def healthbar(self, window):
        """creates the health bar of the Desert Robot"""
        pg.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y - 20, 50, 10)) #red
        pg.draw.rect(window, (0,255,0), (self.rect.x, self.rect.y - 20 , 50 - (0.5 * (100 - self.health)), 10)) #green on top

    def enemy_attack(self):
        """creates the enemy attack"""
        attack = Attack(self.rect.centerx, self.rect.centery, self.facing) #position and create attack
        all_sprites.add(attack)  #add attack to all sprites
        attacks.add(attack) #add the attack to the attack sprite list


    def hit_player(self):
        """when the enemy attack collides with the player, reduce points and health"""
        for attack in attacks:
            if attack.rect.colliderect(player.rect):
                player_hitSound.play()
                player.score -= 1
                if player.health > 1:
                    player.health -= 5
                else:
                    player.kill()
                attack.kill()

#spawning the boss
bigboss = pg.sprite.GroupSingle()
bb = BigBoss()
all_sprites.add(bb)
bigboss.add(bb)

"""adding the enemy attack"""

#attack images
shotR = pg.image.load( path + 'enemyshotR.png').convert_alpha()
shotL  =pg.image.load( path + 'enemyshotL.png').convert_alpha()

class Attack(pg.sprite.Sprite):
    """sprite for the enemy attack"""
    def __init__(self, x, y, facing):
        pg.sprite.Sprite.__init__(self)
        self.image = shotL
        self.rect = self.image.get_rect()
        self.rect.y = y + 20
        self.rect.x = x
        self.facing = facing
        self.speedx = 40 * facing


    def update(self):
        """makes the attack move on the screen"""
        self.rect.x += self.speedx
        if self.rect.right > WIDTH + 500  or self.rect.left < -500: #kill if the attack is off the screen and missed the player
            self.kill()

        #decides which side the attack image should be facing
        if self.facing < 0:
            self.image = shotL
        else:
            self.image =  shotR

attacks =  pg.sprite.Group()

"""--------------------------------------------

loading extra visual stuff
and loading the background image

--------------------------------------------"""

#bones and extra stuff images
bone = pg.image.load( path + 'bone1.png').convert_alpha()
skull = pg.image.load( path + 'skull1.png').convert_alpha()
bone1 = pg.image.load( path + 'bone2.png').convert_alpha()
skull1 =pg.image.load( path + 'skull2.png').convert_alpha()
tree = pg.image.load( path + 'Tree.png').convert_alpha()
signR = pg.image.load( path + 'ArrowSign.png').convert_alpha()
signL = pg.image.load( path + 'ArrowSignL.png').convert_alpha()
skeleton = pg.image.load( path + 'skeleton.png').convert_alpha()
tomb = pg.image.load( path + 'tomb.png').convert_alpha()
tomb1 = pg.image.load( path + 'tomb2.png').convert_alpha()
bush = pg.image.load( path + 'bush.png').convert_alpha()

#background
bg = pg.image.load( path + 'BG.png').convert_alpha() #background image
bg_rect = bg.get_rect() #background rectangle


"""
THE GAME LOOP
"""

running = True
speed = 25
shootloop=0
while running:

    clock.tick(FPS) #refresh rate of screen
    
    """events taken from the user input, decides movement, shooting and quit screen"""

    
    for event in pg.event.get():
        
        if event.type == pg.QUIT: 
            running = False
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == ord('a'):
                player.control(-speed)
            if event.key == pg.K_RIGHT or event.key == ord('d'):
                player.control(speed)
            if event.key == pg.K_UP or event.key == ord('w'):
                player.jump()
            if event.key == pg.K_SPACE and shootloop == 0:
                player.shoot()
                arrow_shotSound.play()
                shootloop  =1
            if event.key == pg.K_SLASH or event.key == ord('e'):
                if player.PUCount > 0:
                    player.shoot_pu()
                    player.PUCount -=1
                    #powerSound.play()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == ord('a'):
                player.control(speed)
                player.image = playr_leftfacing
            if event.key == pg.K_RIGHT or event.key == ord('d'):
                player.control(-speed)
                player.image = playr_rightfacing
            if event.key == ord('q') or event.key == pg.K_ESCAPE:
                running = False


    """general update section"""
    all_sprites.update()

    #this loop ensures that the player can't shoot unlimited arrows by pressing the space bar continuosly
    if shootloop > 0:
        shootloop +=1
    if shootloop > 5:
        shootloop = 0

    #if player is colliding with ground or platforms, set the variables so that a jump is possible
    cg = pg.sprite.spritecollide(player, ground_tiles, False, False)
    cp = pg.sprite.spritecollide(player, platforms, False, False)
    if cg or cp:
        player.isJumping = False
        player.isStanding = True
            
    #if the enemy's attack hit the player or disappeared off the screen, then the enemy can shoot again
    for bb in bigboss:
        if not attacks:
            bb.canshoot = True


        
    #little animation of the zombie getting hit
    for arrow in arrows:
        for zombie in zombies:
            if arrow.rect.colliderect(zombie.rect):
                if zombie.speedx > 0:
                    zombie.image = hurtR
                else:
                    zombie.image = hurtL
    
    """update section: side scroller control (only moves platforms and second enemy)"""
    if not zombies:
        if player.rect.right >= WIDTH * 0.75:
            for platform in platforms:
                if player.velx > 0:
                    platform.rect.x -= abs(player.velx)
                    platform.startx -= abs(player.velx)
                    borderR.rect.x -= 4
                    borderL.rect.x -= 4
                    for ork in orks:
                        ork.rect.x -= 3
                        
                        
        elif player.rect.left <= WIDTH * 0.2:
            for platform in platforms:
                if player.velx < 0:
                    platform.rect.x += abs(player.velx)
                    platform.startx += abs(player.velx)
                    borderL.rect.x += 4
                    borderR.rect.x += 4
                    for ork in orks:
                        ork.rect.x += 3


    """drawing"""
    #order matters
    window.fill(BLACK) #fill the screen with black, for backup
    window.blit(bg, bg_rect) #blit the background on the screen
    
    font1 = pg.font.SysFont('Arial', 36) #decide on a font
    text1 = font1.render("Streak:  " + str(player.streak) , 1, (YELLOW)) #save the score
    window.blit(text1, (20,20)) #blit the score on the screen
    
    font = pg.font.SysFont('Arial', 36) #decide on a font
    text = font.render("Score:  " + str(player.score) , 1, (YELLOW)) #save the score
    window.blit(text, (870,20)) #blit the score on the screen

    #draw all the sprites and healthbars on the screen
    
    if player.health > 0:
        player.healthbar(window)
        if not bigboss:
            font3 = pg.font.SysFont('Arial', 70) 
            text3 = font3.render('YOU  WON' , 1, (GREEN)) #when the last enemy dies, show the player that they won
            window.blit(text3, (350,250))
            winSound.play() #winning sound effect
    else:
        font2 = pg.font.SysFont('Arial', 70) 
        text2 = font2.render('GAME OVER' , 1, (RED)) #when the player dies, show them that they lost
        window.blit(text2, (350,250)) 
        lostSound.play() #play losing sound effect
        
    #visual stufff behing the sprites
    window.blit(tomb, (530, HEIGHT - ty - 35))
    window.blit(tree, (800, HEIGHT - ty - 120 ))
    window.blit(tomb1, (80, HEIGHT -  ty - 37))
    
    all_sprites.draw(window)

    #visual stuff on top of the sprite layer
    window.blit(bone, (0, HEIGHT - ty))
    window.blit(bone1, (560, HEIGHT - ty - 20 ))
    window.blit(skull, (900, HEIGHT - ty + 10))
    window.blit(skeleton, (200, HEIGHT - 25))
    window.blit(bush, (350, HEIGHT - ty - 35))

    for zombie in zombies:
        zombie.healthbar(window)
    for ork in orks:
        ork.healthbar(window)
    for bb in bigboss:
        bb.healthbar(window)
        
    pg.display.flip() #flip the display so pygames can draw the next iteration on it

pg.quit() #close the game window
sys.exit()

