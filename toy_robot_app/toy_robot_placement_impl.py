from toy_robot_app.common import FacingDirection
from toy_robot_app.toy_robot_placement_interface import ToyRobotPlacementInterface


class ToyRobotPlacement(ToyRobotPlacementInterface):
    def __init__(self):
        self._x_coord = 0
        self._y_coord = 0
        self._current_facing = FacingDirection.NORTH
        self.MAX_UNIT_SIZE = 5

    def apply_command(self, command: str, *args):
        method_name = '_handle_' + command.lower()
        try:
            method_to_call = getattr(self, method_name)
            method_to_call(args)
        except Exception as e:
            print(f'Invalid command={command}, ignore this line')

    def _set_position_if_valid(self, x_coord, y_coord) -> bool:
        if (x_coord < 0 or x_coord >= self.MAX_UNIT_SIZE) or \
                (y_coord < 0 or y_coord >= self.MAX_UNIT_SIZE):
            return False
        else:
            self._x_coord = x_coord
            self._y_coord = y_coord
            return True

    def _handle_place(self, args: tuple):
        try:
            x_coord_str, y_coord_str, direction_str = args
            facing_direction = FacingDirection[direction_str]
            x_coord = int(x_coord_str)
            y_coord = int(y_coord_str)
        except Exception as e:
            print(f"Incorrect Argument list for PLACE command, ignore this line. error={e}")
            return

        if self._set_position_if_valid(x_coord, y_coord):
            self._current_facing = facing_direction

    def _handle_move(self, args: tuple):
        current_x = self._x_coord
        current_y = self._y_coord
        if self._current_facing == FacingDirection.NORTH:
            current_y += 1
        elif self._current_facing == FacingDirection.SOUTH:
            current_y -= 1
        elif self._current_facing == FacingDirection.EAST:
            current_x += 1
        elif self._current_facing == FacingDirection.WEST:
            current_x -= 1

        self._set_position_if_valid(current_x, current_y)

    def _handle_left(self, args: tuple):
        next_facing_value = (self._current_facing.value - 1)
        if next_facing_value < 0:
            next_facing_value += 4

        self._current_facing = FacingDirection(next_facing_value)

    def _handle_right(self, args: tuple):
        next_facing_value = (self._current_facing.value + 1)
        if next_facing_value >= 4:
            next_facing_value -= 4

        self._current_facing = FacingDirection(next_facing_value)

    def _handle_report(self, args: tuple):
        output = 'Output: ' + ','.join([str(self._x_coord), str(self._y_coord), self._current_facing.name])
        print(output)
