# School Mapping

School Mapping is a small Python project for representing a school floor plan as grid coordinates and finding routes through it with A* pathfinding.

The project includes a terminal UI built with Textual. It displays the map as a grid, lets you select a start and end location, and highlights the shortest valid path between them.

## Project Files

- `main_ui.py` - Runs the interactive Textual map UI.
- `A_star_pathing.py` - Contains the A* pathfinding function.
- `school_map.py` - Stores the school map coordinates, room labels, and valid room entry points.
- `map to cordinates.jpeg` - Reference image used to convert the school map into coordinates.

## How It Works

The map is stored in `school_map.py` as a NumPy array where each row has this format:

```python
[x, y, label]
```

The `label` identifies what is at that coordinate. `0` is used for hallways, while other numbers represent rooms or locations such as the gym, commons, cafeteria, media center, entrances, restrooms, and office areas.

`A_star_pathing()` finds the shortest valid route between two coordinates. It walks through hallway tiles and can also use special room entry rules from `valid_entries` so rooms are only entered from realistic access points.

## Requirements

- Python 3
- NumPy
- Textual

Install the required packages with:

```bash
python3 -m pip install numpy textual
```

## Run the Interactive Map

Start the terminal UI with:

```bash
python3 main_ui.py
```

In the app:

- Click a map location to choose the start point.
- Click another map location to choose the end point.
- The shortest path will be highlighted.
- Press `r` to reset the selected points after a path has been drawn.

## Run the Pathfinding Demo

You can also run the pathfinding file directly to print an example route:

```bash
python3 A_star_pathing.py
```
