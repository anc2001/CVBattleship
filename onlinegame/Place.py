class Place:
    def place_ship(self, orientation,x,y, grid_player):
        if orientation == "v":
            grid_player[x][y] = "1"
            grid_player[x+1][y] = "1"
            grid_player[x+2][y] = "1"

        if orientation == "h":
            grid_player[x][y] = "1"
            grid_player[x][y+1] = "1"
            grid_player[x][y+2] = "1"