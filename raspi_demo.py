#########################################
# Program: raspi_demo                   #
# Purpose: Create a Network catch game  #
# Author:  Tim Rudenko                  #
# Classes: Player                       #
#########################################

from sense_hat import SenseHat
import random
import time


sense = SenseHat()
pix = sense.set_pixel
running = True


class Player(object):
    """ Player Object instantiates with a default of 
        (3, 3) position and a choice of a color
    """
    def __init__(self, color) -> None:
        self.x = 3
        self.y = 3
        self.color = color
        self.position = sense.set_pixel(self.x, self.y, self.color)
    
    def down(self) -> None:
        """ Shuts down the LED of player position
        """
        self.position = sense.set_pixel(self.x, self.y, (0,0,0))

    def up(self) -> None:
        """ Turns on the LED of player position
        """
        self.position = sense.set_pixel(self.x, self.y, self.color)
    
    def shoot(self) -> tuple:
        """ Shoots a projectile from the player position
            Returns player postion at the time of shooting as tuple
        """
        position = self.x + 2 

        while position < 7:
            sense.set_pixel(position - 1 , self.y, (0,0,0))
            sense.set_pixel(position, self.y, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            position += 1
            time.sleep(0.04)

        sense.set_pixel(position - 1, self.y, (0,0,0))
        return (self.x, self.y)
    

# Sets pregame coordinates
def color_coordinate() -> None:
    x = (0,7)
    y = (7,0)

    for i in range(8):
        random_num = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        print(random_num)
        pix(0, i, random_num)

    for i in range(1, 7):
        random_num = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        print(random_num)
        pix(i,0 , random_num)


# Controls Player movement methods of the player object
# Movement() also sets the boundries for the grid preventing 
# an exception from being raised.
def movement(player: Player, event) -> None:
    if event.direction == 'down' and player.y < 7:
        player.down()
        player.y += 1
        player.up()
        
    elif event.direction == 'up' and player.y > 1:
        player.down()
        player.y -= 1
        player.up()

    elif event.direction == 'right' and player.x < 6:
       player.down() 
       player.x += 1
       player.up()

    elif event.direction == 'left' and player.x > 1:
        player.down()
        player.x -= 1
        player.up()

    elif event.direction == 'middle':
        signal = (player.shoot())
        print(signal)


def main() -> None:
    sense.clear()
    color_coordinate()
    player1 = Player((255, 255, 255))

    while running:
        for event in sense.stick.get_events():
            movement(player1, event) 


if __name__ == '__main__':
   main() 

