# Amazing Maze

A comprehensive toolkit for generating, visualizing, and solving mazes, featuring a robust Python backend and a premium interactive Web Visualizer.

## Features

### 🐍 Python Toolkit (`maze_toolkit.py`)
- **Generation Algorithms**: Recursive Backtracker (DFS), Kruskal's Algorithm.
- **Solving**: Breadth-First Search (BFS) solver.
- **Visualization**: ASCII-based maze rendering in the terminal.
- **Type Safety**: Fully type-hinted codebase.

### 🌐 Web Visualizer (`maze_visual.html`)
A state-of-the-art, interactive maze visualizer built with vanilla JavaScript and HTML5 Canvas.

- **Premium UI**: Modern "Cyberpunk/Dark" aesthetic with glassmorphism effects and responsive layout.
- **Algorithms**:
  - **Generators**: Recursive Backtracker (DFS), Growing Tree (customizable bias), Kruskal's Algorithm (Union-Find).
  - **Solvers**: BFS (Optimized queue), A* (PriorityQueue based).
- **Performance**:
  - Optimized for large mazes (up to 400x400).
  - Efficient memory usage with TypedArrays (`Int8Array`, `Int32Array`).
  - Smooth animations with batch rendering.
- **Interactive Features**:
  - **Zoom & Pan**: Explore massive mazes with intuitive zoom controls.
  - **Custom Shapes**: Rectangular and Circular (Masked) mazes.
  - **Export**: Save your unique mazes as SVG.
  - **Manual Start/Goal**: Left-click to set Start, Right-click to set Goal.

## Usage

### Python
Run the toolkit directly to generate and solve a maze in your terminal:
```bash
python3 maze_toolkit.py
```

### Web Visualizer
Simply open `maze_visual.html` in any modern web browser. No server required!
- **Generate**: Choose an algorithm and click "Generate".
- **Solve**: Click "BFS Solve" or "A* Solve" to watch the pathfinding in action.
- **Controls**: Use the sidebar to adjust size, speed, and shape.

## Recent Updates (v2.1)
- **UI Redesign**: Complete overhaul with a professional dark theme.
- **Optimization**: Implemented `PriorityQueue` for A* and pointer-based queue for BFS, significantly improving performance.
- **Bug Fixes**: Fixed rendering artifacts during generation.
- **New Features**: Added Zoom controls and increased maximum grid size.

## License
MIT
