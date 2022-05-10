#########################################
# Program: raspi_demo                   #
# Purpose: Create a Network catch game  #
# Author:  Tim Rudenko                  #
# Classes: Player, Network_Interface    #
#########################################

from sense_hat import SenseHat
import random
import time
import socket
import threading
import encodings

sense = SenseHat()
pix = sense.set_pixel
running = True

HOST = "10.41.10.38"
PORT = 43594


class Player(object):
    """ Player Object instantiates with a default of 
        (3, 3) position and a choice of a color
    """
    def __init__(self, color):
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
    
    def shoot(self) -> None:
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
        #return (self.x, self.y)


class Network_Interface(object):

    def __init__(self, host, port) -> None:
        self.__host = host
        self.__port = port

    def send(self, data1: int, data2: int) -> None:

        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.__host, self.__port)) 
            s.listen(5)
            clientsocket, address = s.accept()
            clientsocket.send(str(data1).encode('utf8'))
            time.sleep(0.50)
            clientsocket.send(str(data2).encode('utf8')) 


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
def movement(player: Player, event, Network: Network_Interface) -> None:

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
        Network.send(player.x, player.y)
        print(f"Try Send: {player.x}, {player.y}")


def main() -> None:

    sense.clear()
    color_coordinate()
    player1 = Player((255, 255, 255))
    network = Network_Interface(HOST,PORT)

    while running:
        for event in sense.stick.get_events():
            movement(player1, event, network) 


if __name__ == '__main__':
   main() 

