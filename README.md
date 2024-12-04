# CPEN333-Final-Project
This project is a group assignment for CPEN333A. You are to work with your own group-mate, and one set of code files for each group is submitted to Canvas.

You can use the group tools available on Canvas to communicate with your groupmate (see the menu on the left).

Make sure you read the announcements regularly regarding the project.

The project is due Fri Dec 6, by 4:59 PM (the last day of classes). Please plan ahead, no late submission will be accepted.

### Academic honesty and standard:
As always, remind yourself of the UBC academic honesty and standard and submit work that is yours or your own group's work only. Do not share/discuss your design thinking or any part of your code with anybody outside your own group. Using any outside snippet of code (that is neither from the course materials posted on Canvas, nor the Python's official online documentation) is not allowed. Any code snippet or code design from the the online documentation must be properly cited in your code. 

### Submission
Once you complete the implementations of the two parts of the project as described, submit your work to the associated submission dropbox for the project by the deadline. The code must include sufficient comment statements to document it well. No email or late submission is accepted, please do plan ahead accordingly. Coordinate among your group on who is to submit as only one set of files is to be submitted by the deadline (in the case of multiple submissions, we will only consider the last submission). Fully follow the project specification. Deliverables are:

<ul>  
  <li><strong>Part1 code file</strong> (one .py file): Submit one python3 file including the complete code for Part1 of the project. Make sure the file name includes the words part1 in its name, e.g. part1.py.</li>
  <li><strong>Part1 additional documentation file</strong> (one .pdf file): Submit a short documentation file (up to 3 pages) for the open-ended aspects of the project. This file does not replace the documentation you must have in the code as usual (readable code in the first place and useful comments statements), but it is meant to allow your group to provide your calculations, additional explanation, and your design consideration for any open-ended aspect of the project that you would need to document. For example, the document should include your calculation/geometry to explain under what conditions your program decides that the prey is captured; how the new coordinates are created/updated; how the new prey is created. You should also include any challenges that you faced, as well as, some incremental technical/implementation improvement(s) that you would consider (explain only, but do not include in the submitted code) for the future. The purpose of the latter is to further demonstrate and document your understanding of the dynamics of the game and its limitations.</li>
  <li><strong>Part1_alternative code file</strong> (one .py file, include part1_alternative as a part of the filename): submit the complete implementation of part1, using one different approach in the game implementation related to a rather substantial concept. See below for details.
  <li><strong>Part2 code files</strong> (two .py files):  Submit the two python3 files for Part2 of the project: the client.py program (include the words part2 and client in the name of the file, e.g. part2_client.py) and the server.py program (include the words part2 and server in the name of the file, e.g. part2_server.py).</li>
  <li><strong>iPeer survey</strong> (linked on canvas under Project module):  There will be an iPeer peer evaluation that you will fill out to rate each of your group-mates' level of contribution and effort in design, implementation and testing. This is an assessment point considered for a fair evaluation of individual grades. It is due is the same as the project files submission due. Completing the iPeer evaluation is required for each student and is considered for marking.</li>
</ul>
It is important to have regular communications with your group-mate on setting or re-assessing task assignments, integration and testing. It is natural to overestimate or underestimate, but you should adjust accordingly.

Code review among group-mates is expected, that is, every group member's code used in the project must be reviewed by your other group-mate. This way, you not only help find bugs and improve coding, but every group-mate will learn about all aspects of the project. You cannot claim that that other group-mate coded this part, so you do not know about it.

==================== 

### Part 1: Implementing a multithreaded game with graphic user interface
Write one python3 file the includes all the code for this part of the project. Make sure the file name includes the words part1 in its name.

We are to implement a simplified snake game in this project. Here are some characteristics of the program:

<ul>
  <li>Here is a video of the sample run of the game to show the basic intended behaviour:</li>
  https://youtu.be/gWvkkm2bASYLinks to an external site.
  <ul>
    <li>Note that the video uses "one" possible set of values for the widths of prey and the snake.</li>
    <li>The decision on when the prey is considered captured is left for your group (this does not mean choosing the easiest one in a lazy manner). You must consider/document/implement a reasonable approach (e.g. when the prey is fully overlapped by the head of the moving snake (if the selected widths allow), ...)</li>
    <li>A new prey can be placed anywhere on canvas (considering the specified THRESHOLD) in its simplest form, but you should consider more reasonable limitations (e.g. not on the score text, not on the current position of the snake, ...)</li>
    <li>For a general, but longer and sped-up demo of a generic snake game see here: https://en.wikipedia.org/wiki/Snake_(video_game_genre)#/media/File:Snake_can_be_completed.gifLinks to an external site.</li>
  </ul>
</ul>

Please read the docstring for each of the methods and comments for each portion of the program that is left for you to implement.

Some notes:

<ul>
  <li>The snake's current position and length is represented by the field snakeCoordinates of the Game class. It is a list of tuples. Each tuple is an (x, y) coordinate. In the GUI, the snake is represented by the snakeIcon which is a Tkinter canvas line with the width SNAKE_ICON_WIDTH based on the snakeCoordinate list.</li>
  <li>The new prey is created at the beginning of the game and each time the snake captures one. In the GUI, the prey is represented by the preyIcon which is a Tkinter canvas rectangle. The method createNewPrey randomly generates an x and a y, and then sets the prey rectnagleCoordinates as (x - 5, y - 5, x + 5, y + 5) which is added as a task to the queue. On the GUI, the prey is currently a 10 by 10 rectangle.</li>
  <ul>  
    <li>Currently, the magic number 10 (and its half, 5, and any other value related to it) is used for the prey width. You must modify the code so that instead of using the magic number 10, you use the constant PREY_ICON_WIDTH (add this to the code right after the line for SNAKE_ICON_WIDTH), so that we can easily change the width in one place.</li>
    <li>You program should work with any reasonable values used for the SNAKE_ICON_WIDTH or SNAKE_ICON_WIDTH (including the current values in the skeleton, obviously).</li>
  </ul>
  
  <li>Add any missing type hints for the method parameters, and returns.</li>
  <li>You are allowed to use reasonably different values for the width (WINDOW_WIDTH) or/and length (WINDOW_HEIGHT) of the canvas widget, but justifications must be documented.</li>
  <li>The queue is a FIFO queue of all the pending tasks that each portion of the program created and added to the queue. Each item in the queue is a dictionary.</li>
  <ul>
    <li>The keys in the dictionary is one of "game_over", "move", "prey", or "score".</li>
    <li>The value depends on the key.</li>
    <ul>
      <li>The value for the key "game_over" is a Boolean value (True or False)</li>
      <li>The value for the key "score" is an integer representing the new score.</li>
      <li>The value for the key "prey" is the new rectangleCoordinates of the form (x1, y1, x2, y2).</li>
      <li>The value for the key "move" is the snakeCoordinates which is a list of tuples.</li>
    </ul>
  </ul>
  <li>The implementations of the GUI and the Queue classes, as well as the main thread is given to you. You are to complete the implementation of some of the methods in the Game class. Those two types and their operations must be used by the Game class whenever needed.</li>
  <li>Note that the * in an argument of the form *var in a function call is an unpacking operator. From the documentationLinks to an external site.: "An asterisk * denotes iterable unpacking. Its operand must be an iterable. The iterable is expanded into a sequence of items, which are included in the new tuple, list, or set, at the site of the unpacking." Also in PEP 448Links to an external site.. (A note that * has different meaning for the method's formal parameter as opposed to a function argument.)</li>
</ul>

The amount of code that you will be writing is not much, but you need to understand the problem and figure out how to work with the provided classes and code to complete the project. This is a common situation when you join a company in real-life and need to continue on and complete a project based on present code and client requirements. 

You are allowed to add inner functions to any of the methods but do not add any new type, or new methods. Do not modify the code skeleton, except for where required/specified.

Make sure that your code is readable and add comments whenever needed to explain your code.

</ul>

==================== 

Part 1_alternaive: 
Submit another complete implementation of part1 (all in one .py file, include part1_alternative as a part of the name of the file), but with one modification for the implementation related to an important aspect of the game related to this course: e.g. multi-tasking synchronization/communication, GUI, ... . Some examples of acceptable new implementation approaches would be:

* instead of tkinter, using a different GUI framework, such as pygame, ...
* or instead of using the thread-safe queue, using a different thread-safe mechanism for managing and communicating the tasks 
* or ...

Include a comment statement at the top of the file, explaining what different approach was used for the implementation.

Note that this portion of the project will have a weight of roughly 10% (depending on the effort and the approach; so consider this part1_alternative portion, if your group is aiming for a high grade).

==================== 

Part 2: Simple Chat Application
In this part of the project, you are going to implement a simple chat application. You will use the python 3 standard library modules of socket, multiprocessing, threading and tkiner. No other modules are to be used.

The program consists of three .py files: main.py (use as is), client.py and server.py. The client and server are imported into our main.py, where we will use the main() functions (as see below in the template).

Normally, the server and each of the chat clients run on different machines, but without loss of generally, we are going to implement this application, so that they run on the same computer. You can use the IP address 127.0.0.1 (known as loopback address or localhost) which is a special IP address that refers to the current computer. 

We can run main.py, which as you can see from the template below, uses python's multiprocessing to create a server process and two client processes.

The main.py imports our other two python files that you are to implement: client.py and server.py (put the three of them in the same folder while developing).

We use TCP socket programming using Python's socket module as discussed in the lecture. Refer to the official documentation at https://docs.python.org/3/library/socket.htmlLinks to an external site..

Note that there is a one second sleep in main.py to help ensure server is up and running before the clients, but this is a temporary solution.  You should make sure that the clients work well if the server is not yet up and running.

Notes, hints and requirements:

- Watch this video that shows the basic look and functionality of the intended implementation for the app:
https://youtu.be/dI7jZVx_wG0Links to an external site.
- Your implementation should follow the requirements (functionality and features, the overall look, ...) . For certain aspects of the project though, there is some reasonable flexibility for improved implementation (if in doubt, please do ask).
- Fully document your code (comments, docstrings, type hints, ...) as usual.
- Use the provided code skeleton and app structure.
- Your program should also work when there are more than two clients (e.g. when a third thread is created (in main.py) and used for a third client).
- Your program should consider terminations (i.e. some reasonable graceful termination of the client exiting, and continuous operation of the rest of the threads)
- Do not include any other import other than the ones in the skeleton code.
- Write the code with changeability in mind. 
- Wherever needed (and only wherever needed), use threading inside the client and inside the server programs. 
- Design the members of each class carefully and document them well.
