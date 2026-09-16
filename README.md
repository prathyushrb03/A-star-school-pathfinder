# School Mapping

School Mapping is a small Python project for representing a school floor plan as grid coordinates and finding routes through it with A* pathfinding.

The project includes a terminal UI built with Textual. It displays the map as a grid, lets the user select a start and end location, and highlights the shortest valid path between them.

## Project Files

- `src/app.py` - Runs the interactive Textual map UI.
- `src/A_star_pathing.py` - Contains the A* pathfinding function.
- `src/school_map.py` - Stores the school map coordinates, room labels, and valid room entry points.
- `school_pathfinder.toml` - Stores the project requirements and run commands used by the installer.
- `install.sh` - Installs the requirements listed in `school_pathfinder.toml`.
- `map to cordinates.jpeg` - Reference image used to convert the school map into coordinates.

## How It Works

The map is stored in `school_map.py` as a NumPy array where each row has this format:

```python
[x, y, label]
```

The `label` identifies what is at that coordinate. `0` is used for hallways, while other numbers represent rooms or locations such as the gym, commons, cafeteria, media center, entrances, restrooms, and office areas.

`A_star_pathing()` finds the shortest valid route between two coordinates. It walks through hallway tiles and can also use special room entry rules from `valid_entries` so rooms are only entered from realistic access points.

## Installation

Install the required packages from `school_pathfinder.toml` with:

```bash
./install.sh
```

## Run the Interactive Map

Start the browser-hosted map server with:

```bash
./.venv/bin/python serve.py
```

Then open:

```text
http://localhost:8000
```

In the app:

- Click a map location to choose the start point.
- Click another map location to choose the end point.
- The shortest path will be highlighted.
- Press `r` to reset the selected points after a path has been drawn.

## Run the GitHub Pages Version

`serve.py` starts a local Python server with `textual_serve`, so it works on your computer
at `http://localhost:8000` but cannot run directly on GitHub Pages. GitHub Pages only
serves static files.

The static version is `index.html`. It loads Pyodide in the browser, fetches the Python
files in `src/`, and runs the map/pathfinding code client-side. For local testing, run:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

Disclosure: `index.html` was written with substantial help from ChatGPT in writing that 
The original school map data and Python pathfinding code live in `src/`, and the original
textual-based terminal UI can be launched from `serve.py`.

## Run the Pathfinding Demo

You can also run the pathfinding file directly to print an example route:

```bash
PYTHONPATH=src ./.venv/bin/python -m A_star_pathing
```
