2D Maze Game:
An interactive 2D maze game developed in Python, combining fun gameplay with smart computer graphics concepts.  
This project was created as part of the **Smart Computer Graphics (CSBP421)** course.


Features:
- **Procedural Maze Generation** → Every maze is unique using Depth-First Search (DFS).
- **Solvability Check** → Ensures mazes are always solvable using Breadth-First Search (BFS).
- **Player Customization** → Choose your favorite character color.
- **Power-Ups** → Collect yellow power-ups before reaching the goal.
- **Progressive Difficulty** → 5 levels with decreasing time (50s → 15s).
- **Retry & Reset Options** → Replay a level or return to the home screen anytime.
- **Victory Celebration** → Win all levels and get a congratulatory message.


Technologies Used:
- **Python 3**
- **Tkinter** → GUI (home screen, buttons, labels, canvas)
- **Random** → Random walls & power-ups
- **Time** → Countdown timer
- **Algorithms** → DFS (maze generation), BFS (solvability)

How to Play:
1. Start the game from the **home screen**:
   - Pick your character’s color.
   - Read the instructions.
   - Click **Start Game**.
2. Use the **arrow keys** to navigate the maze.
3. Collect at least **one yellow power-up** before reaching the **red goal**.
4. Beat all **5 levels** within the time limits to win!

Project Structure:
2D-Maze-Game/
├── 2D Maze.py # Main Python code
├── report/
│ └── CSBP421 - Project Report.docx
├── presentation/
│ └── Smart Computer Graphics Presentation.pptx
├── requirements.txt # Dependencies
├── .gitignore
└── README.md


