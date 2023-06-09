# Breakthrough Board Game

It is Breakthrough board game made with pygame python.

Game has basic AI to play with it. Player can choose to start first or second.
## Important notice
The file "Button.py" is taken from user [@baraltech](https://github.com/baraltech) repository [Menu-System-PyGame](https://github.com/baraltech/Menu-System-PyGame).
He also has a video talking about how it works [here](https://www.youtube.com/watch?v=GMBqjxcKogA&t=177s).

## Game rules
Each player moves one piece per turn.

If the target position is empty, a piece can be moved one space forward or diagonally forward. A piece may be also moved to a square occupied by an enemy piece, if the target position is one space diagonally forward.

The game ends if one player reaches opponent's home row.

## How to run from executable
- Go to [release page](https://github.com/memo1918/Breakthrough-board-game/releases)
- Download the latest .zip (not the source code).
- extract the zip and run the .exe

Note: Windows might see the .exe file as a virus. This is beacuse it is not signed. If you don't want to turn off your firewall or simply trust, you can run from the source.

## How to run from source
- Download the code from the top right corner of github. Code -> Download ZIP
- Install python 3.11.0 if you don't have it already. [Download link](https://www.python.org/downloads/release/python-3110/) (I haven't test with other versions)
- Install pygame module. You can do it by running the command below on a terminal.
```cmd
pip install pygame
```
- Run Main.py
```cmd
python Main.py
```
Note: Make sure file structure look like this

    ├── Classes                      
    │   ├── Computer.py
    │   ├── Button.py
    │   ├── Board.py
    │   ├── Square.py     
    │   └── Piece.py        
    └── Main.py
    
#### Optional arguments when running
- ```-s | --size```: Changes the board size (defualt: 6)
- ```-r | --resolution```: Changes the resolution,widht and height, of the game screen (defualt: 720)
- ```-d | --depth```: Changes the algorithms search depth (defualt: 3)

Example
```cmd
python Main.py -s 6 -r 720 -d 3
```
or if you have the executable
```cmd
Breakthrough.exe -s 6 -r 720 -d 3
```
