import numpy as np

from A_star_pathing import A_star_pathing
from school_map import map, label_lookup

from textual.app import App, ComposeResult
from textual.containers import Grid, VerticalScroll, Horizontal, Vertical
from textual.widgets import Button, Digits, Footer, Header, Static

class WidgetMap(Grid):

  # all of these are class variables not object attributes as it is dependant on map
  min_x = int(np.min(map[:, 0]))
  max_x = int(np.max(map[:, 0]))
  min_y = int(np.min(map[:, 1]))
  max_y = int(np.max(map[:, 1]))

  map_width = max_x - min_x + 1
  map_height = max_y - min_y + 1

  map_cords = {(int(x), int(y)) for x, y, _label in map}
  map_indicies = {}
  for x, y, index in map: map_indicies[(int(x), int(y))] = int(index)

  label_names = {value: key for key, value in label_lookup.items()} # reversed dictionary

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) #allows id= to pass to WidgetMap
    self.start_point = None
    self.end_point = None

  def get_cell_label(self, x, y):
    index = self.map_indicies[(x, y)]
    return self.label_names.get(index, str(index))

  def compose(self) -> ComposeResult:
    for y in range(self.max_y, self.min_y - 1, -1):
        for x in range(self.min_x, self.max_x + 1):
            if (x, y) in self.map_cords:

              if self.map_indicies[(x,y)] == label_lookup["Hallway"]: #Hallways
                yield Button(" ", id=f"cell_{x}_{y}_{self.map_indicies[(x,y)]}", classes="cell hallway-cell")

              else: #rooms
                yield Button(self.get_cell_label(x, y), id=f"cell_{x}_{y}_{self.map_indicies[(x,y)]}", classes="cell map-cell")

            else: #empty
              yield Button(" ", id=f"cell_{x}_{y}_Empty", classes="cell empty-cell")

  def on_button_pressed(self, event: Button.Pressed) -> None: 
    # get the button's id information when it is clicked
    str_id = str(event.button.id)
    button_info = str_id.split("_")

    x = int(button_info[1])
    y = int(button_info[2])
    label = button_info[3]
    if label != "Empty":
      label = self.get_cell_label(x, y)

      clicked_button = [x, y, label]

      if self.start_point == None:
        self.start_point = clicked_button
      elif self.end_point == None:
        self.end_point = clicked_button

  def reset_selection(self):
    self.start_point = None
    self.end_point = None

class MapApp(App):

  BINDINGS = [("r", "reset_selection", "Reset")]
  label_names = {value: key for key, value in label_lookup.items()} # reversed dictionary

  CSS = f"""
  #selection-bar {{
      height: 3;
      dock: top;
  }}

  .selected-box {{
      width: 1fr;
      height: 3;
      border: solid white;
      padding: 0 1;
  }}

  #map-grid {{
      layout: grid;
      grid-size: {WidgetMap.map_width} {WidgetMap.map_height};
      grid-columns: 1fr;
      grid-rows: 1fr;
      width: 100%;
      height: 100%;
  }}

  .cell {{
      width: 100%;
      height: 100%;
      min-width: 1;
      min-height: 1;
      padding: 0;
  }}

  .hallway-cell {{
      background: #D2B48C;
      color: #D2B48C;
      border: white;
  }}

  .path-hallway-cell {{
      background: red;
      color: black;
      border: white;
  }}

  .map-cell {{
      background: white;
      color: black;
      border: black;
  }}

  .empty-cell {{
      background: transparent;
      color: transparent;
      border: none;
  }}
  """

  def __init__(self):
    super().__init__() #still call parent __init__ from textual
    self.start_point = None
    self.end_point = None
    self.best_path = None
  
  def compose(self) -> ComposeResult:
    yield WidgetMap(id="map-grid")
    yield Header()
    with Horizontal(id="selection-bar"):
      yield Static(f"Start Point: {self.start_point if self.start_point != None else 'Make a selection'}", id="start-point", classes="selected-box")
      yield Static(f"End Point: {self.end_point if self.end_point != None else 'Make a selection'}", id="end-point", classes="selected-box")
    yield Footer()

  def on_button_pressed(self, event:Button.Pressed) -> None:

    map_widget = self.query_one("#map-grid", WidgetMap)
    self.start_point = map_widget.start_point
    self.end_point = map_widget.end_point

    # access the object and edit the labels
    self.query_one("#start-point", Static).update(f"Start Point: {self.start_point if self.start_point != None else 'Make a selection'}")
    self.query_one("#end-point", Static).update(f"End Point: {self.end_point if self.end_point != None else 'Make a selection'}")

    if self.start_point != None and self.end_point != None:
      self.best_path = A_star_pathing(np.array(self.start_point), np.array(self.end_point), map)
      for cordinate in self.best_path:
        indexed_cordinate = np.append(cordinate, map_widget.map_indicies[cordinate[0],cordinate[1]])
        cord_id = f"cell_{indexed_cordinate[0]}_{indexed_cordinate[1]}_{indexed_cordinate[2]}"
        button = map_widget.query_one(f"#{cord_id}", Button)
        button.remove_class("hallway-cell")
        button.remove_class("map-cell")
        button.add_class("path-hallway-cell")
  

  def action_reset_selection(self): # this runs on start also for some reason but its not really an issue
    map_widget = self.query_one("#map-grid", WidgetMap) # accessing the instance
    map_widget.reset_selection()
    self.start_point = map_widget.start_point
    self.end_point = map_widget.end_point

    # access the object and edit the labels
    self.query_one("#start-point", Static).update(f"Start Point: {self.start_point if self.start_point != None else 'Make a selection'}")
    self.query_one("#end-point", Static).update(f"End Point: {self.end_point if self.end_point != None else 'Make a selection'}")

    # reset button classes
    if self.best_path is not None: #add this to deal with start issues
      for cordinate in self.best_path:
        indexed_cordinate = np.append(cordinate, map_widget.map_indicies[cordinate[0],cordinate[1]])
        cord_id = f"cell_{indexed_cordinate[0]}_{indexed_cordinate[1]}_{indexed_cordinate[2]}"
        button = map_widget.query_one(f"#{cord_id}", Button)
        button.remove_class("path-hallway-cell")
        if indexed_cordinate[2] == label_lookup["Hallway"]:
          button.add_class("hallway-cell")
        else:
          button.add_class("map-cell")

    self.best_path = None # make sure to clean up best path



def main() -> None:
  MapApp().run()


if __name__ == "__main__":
  main()
