class ShotLocation:
    def show_shots(self,shoot_grid):
        print(" ")
        for row in shoot_grid:
            print (" ".join(row))
        print(" ")