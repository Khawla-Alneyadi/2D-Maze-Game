# Smart Computer Graphics Project - Fall 2024
# Student's Name: Khawla Alneyadi - 202212912 //  Salama Alkaabi - 202211492
import tkinter as tk # GUI library for creating the game interface
import random # For randomizing maze generation
import time # For managing the game timer

class MazeGame:
    def __init__(self, master):
        """Initialize the game and its variables."""
        self.master = master
        self.master.title("Maze Game") # Set the window title
        self.master.geometry("800x800") # Set the window size
        self.master.config(bg="white") # Set the background color
        self.player_color = "blue"  # Default color for the player

        # Game parameters
        self.level = 1 # Start at level 1
        self.max_levels = 5 # Define the maximum number of levels
        self.grid_size = 20  # Define the size of the maze grid (20x20)
        self.cell_size = 40  # Each cell in the maze is 40 pixels wide and tall
        self.time_limit = 50  # Time limit in seconds for the first level
        self.timer_running = False  # Timer state (running or stopped)
        self.start_time = None # Time when the level started

        # Maze & Player information
        self.maze = None # The grid representation of the maze
        self.player_pos = None # The player's position in the maze
        self.goal_pos = None # The goal's position in the maze
        self.total_powerups = 0  # Power-ups collected across levels
        self.current_level_powerup = 0  # Power-ups collected in the current level

        # display the home screen
        self.create_home_screen()

    def create_home_screen(self):
        # Set up the home screen frame
        self.home_frame = tk.Frame(self.master, bg="white", bd=10, relief="solid", padx=20, pady=20)
        self.home_frame.pack(fill="both", expand=True)
        # Welcome message
        tk.Label(self.home_frame, text="Welcome to the Maze Game!", font=("Helvetica", 30, "bold"), bg="white").pack(pady=20)
        # Player color selection
        tk.Label(self.home_frame, text="Choose your color:", font=("Helvetica", 16), bg="white").pack(pady=10)
    
    
        # Frame to hold the color buttons
        color_buttons = tk.Frame(self.home_frame, bg="white")
        color_buttons.pack(pady=10)

        # Color buttons with dot visualization
        self.color_buttons = {}
        for color in ["green", "blue", "purple", "orange", "brown"]:
            button = tk.Canvas(color_buttons, width=50, height=50, bg="white", highlightbackground="black", highlightthickness=1)
            button.create_oval(10, 10, 40, 40, fill=color, outline=color)  # Draw a dot in the button
            button.grid(row=0, column=["green", "blue", "purple", "orange", "brown"].index(color), padx=10, pady=10)
            button.bind("<Button-1>", lambda event, c=color: self.set_player_color(c))  # Bind color selection to click
            self.color_buttons[color] = button

        # Highlight the default color (blue)
        self.color_buttons["blue"].config(highlightbackground="black", highlightthickness=4)
        
        # Label to show the currently selected color
        self.color_label = tk.Label(self.home_frame, text="Selected Color: blue", font=("Helvetica", 12), bg="white")
        self.color_label.pack(pady=10)
        
        # Game instructions
        tk.Label(self.home_frame, text="Instructions:", font=("Helvetica", 16), bg="white").pack(pady=14)
        instructions = (
            "1. Navigate the maze to reach the red goal.\n"
            "2. Collect at least one yellow power-up before reaching the goal.\n"
            "3. Complete all levels before time runs out!"
        )
        tk.Label(self.home_frame, text=instructions, font=("Helvetica", 12), justify="left", bg="white").pack(pady=10)
        
        # Start Game button
        tk.Button(self.home_frame, text="Start Game", font=("Helvetica", 16, "bold"),
                  command=self.start_game, bg="lightgreen", relief="raised").pack(pady=20)

    def set_player_color(self, color):
        self.player_color = color  # Store the selected color
        self.color_label.config(text=f"Selected Color: {color}")

        # Highlight the selected color
        for btn_color, btn in self.color_buttons.items():
            if btn_color == color:
                btn.config(highlightbackground="black", highlightthickness=4)  # Highlight selected
            else:
                btn.config(highlightbackground="white", highlightthickness=1)  # Default border

    def start_game(self):
        self.home_frame.destroy()  # Remove the home screen
        self.canvas = tk.Canvas(self.master, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size)
        self.canvas.pack()

        # Game interface
        self.create_widgets()

        # Start the game
        self.create_maze()
        self.start_timer()

        # Redraw the player with the selected color
        self.draw_maze()

    def create_widgets(self):
        # Instructions label
        self.instructions = tk.Label(self.master, text=f"Level {self.level} - Reach the goal!",
                                     font=("Helvetica", 12, "bold"))
        self.instructions.pack()

        # Buttons for navigation and restarting
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        # Button to move to the next level
        self.next_button = tk.Button(self.button_frame, text="NEXT", state=tk.DISABLED, command=self.next_level)
        self.next_button.grid(row=0, column=1)

        # Button to go back to the home screen
        self.home_button = tk.Button(self.button_frame, text="HOME", command=self.go_to_home)
        self.home_button.grid(row=0, column=0)

        # Timer display
        self.timer_label = tk.Label(self.master, text=f"Time left: {self.time_limit} seconds")
        self.timer_label.pack()

        # Power-up tracker
        self.powerup_label = tk.Label(self.master, text=f"Total Power-Ups Collected: {self.total_powerups}")
        self.powerup_label.pack()

        # Bind arrow keys for player movement
        self.bind_keys()

    def go_to_home(self):
        """Navigate back to the home screen and reset the game."""
        self.level = 1  # Reset level to 1
        self.time_limit = 50  # Reset time limit for Level 1
        self.total_powerups = 0  # Reset total power-ups collected
        self.current_level_powerup = 0  # Reset level-specific power-ups

        self.canvas.pack_forget()  # Hide the game canvas
        self.instructions.pack_forget()  # Hide instructions
        self.button_frame.pack_forget()  # Hide button frame
        self.timer_label.pack_forget()  # Hide timer
        self.powerup_label.pack_forget()  # Hide power-up tracker
        self.create_home_screen()  # Show the home screen

    def bind_keys(self):
        self.master.bind("<Left>", lambda event: self.move_player(-1, 0))     # Move left when the left arrow key is pressed
        self.master.bind("<Right>", lambda event: self.move_player(1, 0))     # Move right when the right arrow key is pressed
        self.master.bind("<Up>", lambda event: self.move_player(0, -1))     # Move up when the up arrow key is pressed
        self.master.bind("<Down>", lambda event: self.move_player(0, 1))     # Move down when the down arrow key is pressed

    def start_timer(self):
        self.timer_running = True # Indicate that the timer is active
        self.start_time = time.time() # Record the start time
        self.update_timer() # Begin updating the timer display

    def update_timer(self):
        if self.timer_running:
            # Calculate the elapsed time since the timer started
            elapsed_time = int(time.time() - self.start_time)
            # Calculate how much time remains
            remaining_time = self.time_limit - elapsed_time
            if remaining_time >= 0:
                 # Update the timer label to show remaining time
                self.timer_label.config(text=f"Time left: {remaining_time} seconds")
                # Call this method again after 1 second to continue updating
                self.master.after(1000, self.update_timer)
            else:
                # Time is up, stop the timer and trigger the time-up scenario
                self.timer_running = False
                self.time_up()

    def time_up(self):
        """Reset to level 1 if the player runs out of time, including resetting yellow blocks."""
        self.instructions.config(text="Time's up! Restarting from Level 1.")
        self.level = 1
        self.time_limit = 50  # Reset time limit for Level 1
        self.total_powerups = 0  # Reset total power-ups collected
        self.current_level_powerup = 0  # Reset power-ups collected in the current level
        self.powerup_label.config(text=f"Total Power-Ups Collected: {self.total_powerups}")  # Update display
        self.create_maze()  # Restart maze at level 1
        self.start_timer()

    def create_maze(self):
        # Initialize the maze grid with walls
        self.maze = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Define the player's starting position and goal
        self.player_pos = [1, 1]  # Start near the top-left corner
        self.goal_pos = [self.grid_size - 2, self.grid_size - 2]  # Goal near the bottom-right corner

        # Open paths at the start and goal positions
        self.maze[self.player_pos[0]][self.player_pos[1]] = 0
        self.maze[self.goal_pos[0]][self.goal_pos[1]] = 0

        # Generate a solvable maze structure using depth-first search (DFS)
        self.generate_maze(self.player_pos[0], self.player_pos[1])

        # Add extra walls and a power-up for difficulty and variety
        self.add_extra_walls()
        self.place_power_up()

        # Ensure the goal is accessible
        self.ensure_goal_accessibility()

        # Draw the generated maze on the canvas
        self.draw_maze()

    def generate_maze(self, x, y):
        # Define possible directions for movement: right, left, down, up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)  # Randomize direction to create variation

        # Attempt to move in each direction
        for dx, dy in directions:
            # Calculate the new position after moving
            nx, ny = x + dx * 2, y + dy * 2
            # Check if the new position is within bounds and still a wall
            if 1 <= nx < self.grid_size - 1 and 1 <= ny < self.grid_size - 1 and self.maze[ny][nx] == 1:
                # Create a path at the new position
                self.maze[ny][nx] = 0  # Create a path
                self.maze[y + dy][x + dx] = 0  # Open connecting path
                self.generate_maze(nx, ny)   # Recursively continue generating the maze from the new position


    def add_extra_walls(self):
        extra_walls = (self.level - 1) * 10  # Difficulty scales with level
        for _ in range(extra_walls):
            # Randomly pick a position within the maze
            x, y = random.randint(1, self.grid_size - 2), random.randint(1, self.grid_size - 2)
            # Ensure the chosen position is not the player's start or the goal
            if [y, x] != self.player_pos and [y, x] != self.goal_pos and self.maze[y][x] == 0:
                self.maze[y][x] = 1  # Temporarily add a wall
                if not self.is_solvable():
                    self.maze[y][x] = 0  # Revert if it makes the maze unsolvable

    def place_power_up(self):
        while True:
            # Randomly select a position in the maze
            x, y = random.randint(1, self.grid_size - 2), random.randint(1, self.grid_size - 2)
            # Ensure the power-up is not at the player's position or the goal
            if [y, x] != self.player_pos and [y, x] != self.goal_pos and self.maze[y][x] == 0:
                self.maze[y][x] = 2  # Mark cell with power-up
                break

    def ensure_goal_accessibility(self):
         # Extract the x and y coordinates of the goal position.
        goal_x, goal_y = self.goal_pos[1], self.goal_pos[0]
        # Define the four possible directions: right, left, down, and up.
        # These directions will be used to check and clear paths around the goal.
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Open up paths around the goal position
        for dx, dy in directions:
            nx, ny = goal_x + dx, goal_y + dy
            if 1 <= nx < self.grid_size - 1 and 1 <= ny < self.grid_size - 1:
                self.maze[ny][nx] = 0 # Clear any walls blocking the goal

    def draw_maze(self):
        self.canvas.delete("all")     # Clear the canvas to remove any previous drawings
        # Iterate through each cell in the maze grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Determine the color for the current cell
                if self.maze[i][j] == 0: #path cell
                    color = "white"
                elif self.maze[i][j] == 1: # wall cell
                    color = "gray"
                elif self.maze[i][j] == 2: # power-up cell
                    color = "yellow"
                # Draw the cell as a rectangle on the canvas
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size, # Top-left corner of the rectangle
                                              (j + 1) * self.cell_size, (i + 1) * self.cell_size, #Bottom-right corner of the rectangle
                                              fill=color, outline="black") # Fill the cell with the appropriate color & add a black border around the cell

        # Draw the player with the current color
        self.canvas.create_oval(self.player_pos[1] * self.cell_size + 10, # Left boundary 
                                self.player_pos[0] * self.cell_size + 10, # Top boundary
                                (self.player_pos[1] + 1) * self.cell_size - 10, # Right boundary
                                (self.player_pos[0] + 1) * self.cell_size - 10, # Bottom boundary 
                                fill=self.player_color) # Fill the player circle with the player's selected color

        # Draw the goal as a red circle (oval) in the maze
        self.canvas.create_oval(self.goal_pos[1] * self.cell_size + 10, # Left boundary 
                                self.goal_pos[0] * self.cell_size + 10, # Top boundary
                                (self.goal_pos[1] + 1) * self.cell_size - 10, # Right boundary
                                (self.goal_pos[0] + 1) * self.cell_size - 10, # Bottom boundary 
                                fill="red") # Fill the goal circle with red

    def move_player(self, dx, dy):
    # Calculate the player's new x and y coordinates after the move.
    # dx represents the horizontal change (-1 for left, +1 for right).
    # dy represents the vertical change (-1 for up, +1 for down).
        new_x = self.player_pos[1] + dx # Update the x-coordinate (column).
        new_y = self.player_pos[0] + dy # Update the y-coordinate (row).

        # Check if the move is within bounds and on a valid cell
        if 1 <= new_x < self.grid_size - 1 and 1 <= new_y < self.grid_size - 1:
            if self.maze[new_y][new_x] == 0:  # Move to an empty path
                self.player_pos = [new_y, new_x]
            elif self.maze[new_y][new_x] == 2:  # Collect power-up
                self.maze[new_y][new_x] = 0  # Remove power-up from the maze
                self.player_pos = [new_y, new_x]
                self.current_level_powerup += 1
                self.total_powerups += 1  # Update total power-up count
                self.powerup_label.config(text=f"Total Power-Ups Collected: {self.total_powerups}")

            self.draw_maze()  # Redraw the maze to reflect the move

            if self.player_pos == self.goal_pos:  # Check if the player reached the goal
                if self.current_level_powerup > 0:  # Ensure power-up was collected
                    self.timer_running = False
                    self.congratulate_player()
                else:
                    self.instructions.config(text="You must collect a power-up first!")
                    self.retry_level()

    def retry_level(self):
        self.current_level_powerup = 0     # Reset the power-ups collected for this level to 0.
        self.instructions.config(text=f"Retry Level {self.level}")     # Update the instructions to inform the player they are retrying the level.
        self.create_maze()     # Recreate the maze for the current level.
        self.start_timer()     # Restart the timer for the current level.

    def congratulate_player(self):
        self.instructions.config(text="Congratulations! You've reached the goal.")     # Update the instructions to congratulate the player for completing the level.
        self.next_button.config(state=tk.NORMAL)     # Enable the "NEXT" button to allow the player to move to the next level.

    def next_level(self):
        self.level += 1     # Increase the current level by 1.
        if self.level <= self.max_levels:
            # Adjust time limit for higher levels (harder as you progress)
            self.time_limit = 50 - (self.level - 1) * 10 if self.level < 5 else 15
            self.current_level_powerup = 0  # Reset level-specific power-up count
            self.instructions.config(text=f"Level {self.level} - Reach the goal!")         # Update the instructions to display the new level.
            self.create_maze()         # Generate a new maze for the next level.
            self.next_button.config(state=tk.DISABLED)  # Disable until level is completed "Next"
            self.start_timer()    # Restart the timer for the new level.

        else:
            # Game complete
            self.instructions.config(
                text=f"Congratulations! You collected all {self.total_powerups} power-ups and completed the game!")
            self.next_button.config(state=tk.DISABLED)
            self.canvas.delete("all")  # Clear the canvas to signify game completion

    def reset_game(self):
        self.level = 1     # Reset the game to start at level 1.
        self.time_limit = 50     # Reset the timer to the default time limit for the first level.
        self.total_powerups = 0     # Reset all power-ups collected in the game to 0.
        self.current_level_powerup = 0 # Reset power-ups for the current level as well.
        self.instructions.config(text=f"Level {self.level} - Reach the goal!")     # Update the instructions to indicate the reset level.
        self.powerup_label.config(text=f"Total Power-Ups Collected: {self.total_powerups}")
        self.create_maze()
        self.start_timer()

    def is_solvable(self):
        # Convert the player's position and the goal's position to tuples for easy comparison.
        start = tuple(self.player_pos)
        goal = tuple(self.goal_pos)
        # Create a set to track visited positions to avoid revisiting them.
        visited = set()
        # Initialize a queue with the starting position for breadth-first search (BFS).
        queue = [start]

        # Perform BFS to explore paths from the start to the goal.
        while queue:
            # Get the current position to explore.
            current = queue.pop(0)  # Dequeue
            if current == goal:
            # If the current position is the goal, the maze is solvable.
                return True  # Path exists
            visited.add(current)   # Mark the current position as visited.

        # Explore all possible neighboring positions.
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, left, down, up
                nx, ny = current[1] + dx, current[0] + dy # Calculate neighbor's coordinates
                # Check if the neighbor is within bounds, unvisited, and a valid path.
                if (1 <= nx < self.grid_size - 1 and 1 <= ny < self.grid_size - 1 and
                        (ny, nx) not in visited and self.maze[ny][nx] == 0):
                    queue.append((ny, nx))  # Add the valid neighbor to the queue for further exploration.


        return False  # No path found

def main():
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
