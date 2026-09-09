# School Mapping

This project is a small Python pathfinding utility for a school map.

`school_map.py` stores the school layout as a NumPy array of coordinates. Each row represents one point on the map: 

```python
[x, y, label]
```

The `label` value identifies either a hallway/path tile or a named location such as the gym, commons, cafeteria, media center, entrances, restrooms, and other rooms.

`map to cordinates.jpeg` shows how the example map was converted into coordinates.

## What It Does

The main feature is `A_star_pathing()`, which finds the shortest valid path between two map coordinates using the A* pathfinding algorithm.

It can:

- Find a route from one coordinate to another.
- Treat hallway tiles as valid walking paths.
- Allow extra labels as valid path tiles when a destination is only reachable through another room or area.
- Return the path as a NumPy array of `(x, y)` coordinates from start to finish.

When run directly, `school_map.py` prints an example path between two points on the map.

## Requirements

- Python 3
- NumPy

Install NumPy with:

```bash
pip install numpy
```

## Usage

Run the script:

```bash
python school_map.py
```

## TODO

- Add a frontend so the map is easier to use.
