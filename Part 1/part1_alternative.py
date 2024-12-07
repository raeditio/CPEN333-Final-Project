# Group#: G13
# Student Names: Ryan Jung and Daniel Juca

"""
    This program implements a variety of the snake 
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour, 
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    
class SharedState():
    """
    This class encapsulates the shared state of the game, using thread-safe mechanisms
    to handle concurrent updates. It replaces the need for a queue by providing
    shared variables protected by a lock.
    """
    def __init__(self):
        # Shared variables for game state management
        self.lock = threading.Lock()
        self.game_over_flag = False
        self.snake_coordinates = SNAKE_STARTING_COORDS
        self.prey_coordinates = (0, 0, 0, 0)
        self.score = 0
        

class SharedStateHandler():
    """
        This class implements shared state handling using locks 
        and thread-safe variables instead of a queue.
    """
    def __init__(self):
        self.sharedState = sharedState
        self.gui = gui
        self.updateGui()

    def updateGui(self):
        """
        Reads the shared state variables and updates the GUI elements accordingly.
        Uses temporary variables to detect changes in the state and ensures updates
        are only applied when necessary.
        """
        t_snake_coordinates = [0]
        t_score = -1
        t_prey_coordinates = (-1,-1)

        with self.sharedState.lock:

            snChange = t_snake_coordinates != self.sharedState.snake_coordinates
            pChange = t_prey_coordinates != self.sharedState.prey_coordinates
            scChange = t_score != self.sharedState.score

            if self.sharedState.game_over_flag:
                self.gui.gameOver()
            if snChange:
                self.gui.canvas.coords(gui.snakeIcon, *[x for coord in self.sharedState.snake_coordinates for x in coord])
                t_snake_coordinates = self.sharedState.snake_coordinates
            if pChange:
                self.gui.canvas.coords(gui.preyIcon, *self.sharedState.prey_coordinates)
                t_prey_coordinates = self.sharedState.prey_coordinates
            if scChange:
                self.gui.canvas.itemconfigure(gui.score, text=f"Your Score: {self.sharedState.score}")
                t_score = self.sharedState.score

            if not self.sharedState.game_over_flag:
                self.gui.root.after(100, self.updateGui)



            
            



class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.sharedState = sharedState
        self.score = 0
        
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = SNAKE_STARTING_COORDS
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True

        #center coordinates of prey
        self.preyCoordinates = (0,0)

        self.createNewPrey()


    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15     #speed of snake updates (sec)
        while self.gameNotOver:
            #complete the method implementation below
            self.move()
            time.sleep(SPEED)

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement the prey has been 
            captured, it updates the score and creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        #New Head Coord
        NewSnakeCoordinates = self.calculateNewCoordinates()
        
        #check for gameover
        self.isGameOver(NewSnakeCoordinates)
        
        #if no game over add new coordinates
        self.snakeCoordinates.append(NewSnakeCoordinates)
        with self.sharedState.lock:
            self.sharedState.snake_coordinates.append(NewSnakeCoordinates)

        #Check if prey captured
        if self.preyCaptured(NewSnakeCoordinates):
            
            #if captured add score and create new prey, length increases so don't remove tail
            self.score += 1
            with self.sharedState.lock:
                self.sharedState.score = self.score
            self.createNewPrey()
        else:

            #if no prey captured length doesn't increase so tail is removed
            self.snakeCoordinates.pop(0)
            with self.sharedState.lock:
                self.sharedState.snake_coordinates.pop(0)



    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        
        if self.direction == "Left":
            return lastX-SNAKE_ICON_WIDTH,lastY
        if self.direction == "Right":
            return lastX+SNAKE_ICON_WIDTH,lastY
        if self.direction == "Up":
            return lastX,lastY-SNAKE_ICON_WIDTH
        if self.direction == "Down":
            return lastX,lastY+SNAKE_ICON_WIDTH


    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the `gameNotOver` field 
            and sets the game over flag in the shared state. 
        """
        x, y = snakeCoordinates

        #check for hit wall
        hit_wall = x > WINDOW_WIDTH or x < 0 or y > WINDOW_HEIGHT or y < 0

        #bit self
        bit_self = (x,y) in self.snakeCoordinates

        if  hit_wall or bit_self:
            self.gameNotOver = False

            with self.sharedState.lock:
                self.sharedState.game_over_flag = not self.gameNotOver

    def getPreyCorners(self,preycoords : tuple)->list:
        """Generates the four corner coordinates of the prey rectangle 
        based on its top-left corner.

        Args:
            preycoords (tuple): The top-left (x, y) coordinates of the prey.

        Returns:
            list: A list of four tuples representing the coordinates of 
                the top-left, top-right, bottom-left, and bottom-right corners.
        """
    
        #x and y of top left corner of prey
        (pxtl, pytl) = preycoords
        #store corner cords of prey
        preytl = (pxtl,pytl)
        preytr = (pxtl + PREY_ICON_WIDTH, pytl)
        preybl = (pxtl, pytl + PREY_ICON_WIDTH)
        preybr = (pxtl + PREY_ICON_WIDTH, pytl + PREY_ICON_WIDTH)
        
        return[preytl,preytr,preybr,preybl]


    def getSnakePortionCorners(self,coords : tuple, direction : str)->list:
        """
        Calculates the four corner coordinates of a single portion of the snake
        based on the middle coordinate of its leading edge and direction of movement.

        Args:
            coords (tuple): The middle (x, y) coordinates of the leading edge of the snake portion.
            direction (str): The movement direction ("Left", "Right", "Up", "Down").

        Returns:
            list: A list of four tuples representing the coordinates of 
                the top-left, top-right, bottom-left, and bottom-right corners.
        """
        (nx,ny) = coords

        if direction == "Left":
            #corner coords of snake
            snaketl = (nx, ny - SNAKE_ICON_WIDTH // 2)
            snaketr = (nx + SNAKE_ICON_WIDTH, ny - SNAKE_ICON_WIDTH // 2)
            snakebr = (nx + SNAKE_ICON_WIDTH, ny + SNAKE_ICON_WIDTH//2)
            snakebl = (nx, ny + SNAKE_ICON_WIDTH//2)
        
        elif direction == "Right":
            #corner coords of snake
            snaketl = (nx - SNAKE_ICON_WIDTH, ny - SNAKE_ICON_WIDTH//2)
            snaketr = (nx, ny - SNAKE_ICON_WIDTH//2)
            snakebr = (nx, ny + SNAKE_ICON_WIDTH // 2)
            snakebl = (nx - SNAKE_ICON_WIDTH, ny + SNAKE_ICON_WIDTH // 2)
            
        elif direction == "Up":
            #corner coords of snake
            snaketl = (nx - SNAKE_ICON_WIDTH // 2, ny)
            snaketr = (nx + SNAKE_ICON_WIDTH // 2, ny)
            snakebr = (nx + SNAKE_ICON_WIDTH // 2, ny + SNAKE_ICON_WIDTH)
            snakebl = (nx - SNAKE_ICON_WIDTH // 2, ny + SNAKE_ICON_WIDTH)

        elif direction == "Down":
            #corner coords of snake
            snaketl = (nx - SNAKE_ICON_WIDTH // 2, ny - SNAKE_ICON_WIDTH)
            snaketr = (nx + SNAKE_ICON_WIDTH // 2, ny - SNAKE_ICON_WIDTH)
            snakebr = (nx + SNAKE_ICON_WIDTH // 2, ny)
            snakebl = (nx - SNAKE_ICON_WIDTH // 2, ny)

        return [snaketl,snaketr,snakebr,snakebl]

    def getFullSnakeCorners(self) -> list:
        """
        Retrieves the corner coordinates for all portions of the snake. 
        Iterates through the snake's coordinates, calculates the corners
        of each portion, and adds them to a list.

        Returns:
            list: A list of lists where each inner list contains the 
                corner coordinates of a snake portion.
        """
        fullSnakeCorners = []
        dir = "z"
        
        #temp/first x,y, and direction values
        (tx,ty) = self.snakeCoordinates[0]

        #work from tail to head
        for (x,y) in (self.snakeCoordinates[1:]):

            #check which direction snake moving
            if x>tx:
                dir = "Right"
                fullSnakeCorners.append(self.getSnakePortionCorners((x,y),dir))   #add corner coordinates of portion to list 
                #update temp values
                (tx,ty) = (x,y)

            elif x<tx:
                dir = "Left"
                fullSnakeCorners.append(self.getSnakePortionCorners((x,y),dir))   #add corner coordinates of portion to list    
                #update temp values
                (tx,ty) = (x,y)

            elif y>ty:
                dir = "Down"
                fullSnakeCorners.append(self.getSnakePortionCorners((x,y),dir))   #add corner coordinates of portion to list     
                #update temp values
                (tx,ty) = (x,y)
            elif y<ty:
                dir = "Up"
                fullSnakeCorners.append(self.getSnakePortionCorners((x,y),dir))   #add corner coordinates of portion to list 
                #update temp values
                (tx,ty) = (x,y)
                
        return fullSnakeCorners

    def overlapCheck(self, preyCorners : list, snakeCorners : list)-> bool:
        """
        Checks for overlap between the prey rectangle and a given portion 
        of the snake. Determines if any corner of one rectangle lies inside 
        the other.

        Args:
            preyCorners (list): A list of tuples representing the prey's corners.
            snakeCorners (list): A list of tuples representing a snake portion's corners.

        Returns:
            bool: True if overlap is detected, False otherwise.
        """
        overlap = False

        #check which icon bigger to see which rectangle we use as boundary and which we check each of its corners
        if SNAKE_BIGGER:

            #x/y,min/max of snake
            (xmin,ymin) = snakeCorners[0]#top left
            (xmax,ymax) = snakeCorners[2]#bottom right

            #corners of prey
            corners = preyCorners

        else:
            #x/y,min/max of prey
            (xmin,ymin) = preyCorners[0]#top left
            (xmax,ymax) = preyCorners[2]#bottom right

            #corners of snake
            corners = snakeCorners
            
        for corner in corners:

            #corner's x and y coordinate
            (cornerx,cornery) = corner

            #check if corner inside
            if xmin<cornerx<xmax and ymin<cornery<ymax:

                overlap = True
                break

        return overlap

    def createNewPrey(self) -> None:
        """ 
            Generates random top-left coordinates for the new prey while ensuring
            it does not overlap with the snake. Updates the shared state with
            the new prey's position. We are choosing to allow prey to be created where the score is
        """

        THRESHOLD = 15   #sets how close prey can be to borders

        #find corner coordinates of all portions of snake to check generated prey corners against
        fullSnakeCorners = self.getFullSnakeCorners()
        
        while True:
            
            #Get random ints for top left point of rectangle making sure follows threshold
            x_topleft = random.randint(THRESHOLD,WINDOW_WIDTH-THRESHOLD-PREY_ICON_WIDTH)
            y_topleft = random.randint(THRESHOLD,WINDOW_HEIGHT-THRESHOLD-PREY_ICON_WIDTH)

            #get coordinates of potential prey's corners
            preyCorners = self.getPreyCorners((x_topleft,y_topleft))

            #check if overlap between potential prey and snake
            if any(self.overlapCheck(preyCorners, snakeCorners) for snakeCorners in fullSnakeCorners):
                
                continue    #overlap, regenerate prey

            break   #no overlap, prey position valid
        
        #store valid top left coordinates
        self.preyCoordinates = preyCorners[0]
        
        #get bottom right coordinates
        (x_bottomright,y_bottomright) = preyCorners[2]

        # Add a "prey" task to the queue
        with self.sharedState.lock:
            self.sharedState.prey_coordinates = ((x_topleft,y_topleft,x_bottomright,y_bottomright))
        


        
    def preyCaptured(self, nSnakeCoord : tuple) -> bool:
        """
        Determines if the prey has been captured by the snake.
        Checks for overlap between the prey rectangle and the 
        new head coordinates of the snake.

        Args:
            nSnakeCoord (tuple): The (x, y) coordinates of the snake's new head position.

        Returns:
            bool: True if the prey has been captured, False otherwise.
        """
        
        #corner coordinates
        snakeCorners = self.getSnakePortionCorners(nSnakeCoord,self.direction)
        preyCorners = self.getPreyCorners(self.preyCoordinates)

        #check for overlap
        return self.overlapCheck(preyCorners,snakeCorners)

        


if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300 
    SNAKE_ICON_WIDTH = 15
    #add the specified constant PREY_ICON_WIDTH here 
    PREY_ICON_WIDTH = 10
    #storing max icon width to use in preventing overlapping
    SNAKE_BIGGER = (SNAKE_ICON_WIDTH>PREY_ICON_WIDTH)

    SNAKE_STARTING_COORDS = [(495, 55), (485, 55), (475, 55),
                            (465, 55), (455, 55)] 

    BACKGROUND_COLOUR = "green"   #you may change this colour if you wish
    ICON_COLOUR = "yellow"        #you may change this colour if you wish
    
    sharedState = SharedState() # Instantiate the shared state for thread-safe communication

    game = Game()        #instantiate the game object
    
    gui = Gui()    #instantiate the game user interface
    
    SharedStateHandler() #instantiate a shared state handler object
    
    

    
     
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()