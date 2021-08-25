import unittest
from unittest.mock import patch

import sys
sys.path.append('../')
from toy_robot_app.common import FacingDirection
from toy_robot_app.toy_robot_placement_impl import ToyRobotPlacement


class ToyRobotPlacementTest(unittest.TestCase):
    def setUp(self) -> None:
        self.toy_robot_placement = ToyRobotPlacement()

    @patch('toy_robot_app.toy_robot_placement_impl.ToyRobotPlacement._handle_place')
    def test_apply_command(self, handle_place_mock):
        args = ('1', '2', 'NORTH')
        self.toy_robot_placement.apply_command('PLACE', *args)
        handle_place_mock.assert_called_with(args)

    def test_set_position_if_valid(self):
        result = self.toy_robot_placement._set_position_if_valid(0, self.toy_robot_placement.MAX_UNIT_SIZE - 1)
        self.assertTrue(result)

        result = self.toy_robot_placement._set_position_if_valid(self.toy_robot_placement.MAX_UNIT_SIZE,
                                                                 self.toy_robot_placement.MAX_UNIT_SIZE - 1)
        self.assertFalse(result)

    def test_handle_place_normal(self):
        args = ('1', '2', 'NORTH')
        self.toy_robot_placement._handle_place(args)
        self.assertEqual(self.toy_robot_placement._x_coord, 1)
        self.assertEqual(self.toy_robot_placement._y_coord, 2)
        self.assertEqual(self.toy_robot_placement._current_facing, FacingDirection.NORTH)

    @patch('toy_robot_app.toy_robot_placement_impl.ToyRobotPlacement._set_position_if_valid')
    def test_handle_place_error(self, set_position_mock):
        args = ('x', '2', 'SOUTH')
        self.toy_robot_placement._handle_place(args)
        set_position_mock.assert_not_called()

        args = ('1', '2', 'EEAST')
        self.toy_robot_placement._handle_place(args)
        set_position_mock.assert_not_called()

    def test_handle_move(self):
        # Normal case
        normal_x = self.toy_robot_placement.MAX_UNIT_SIZE - 2
        normal_y = self.toy_robot_placement.MAX_UNIT_SIZE - 2
        args = (str(normal_x), str(normal_y), 'EAST')
        self.toy_robot_placement._handle_place(args)
        self.toy_robot_placement._handle_move(args)
        self.assertEqual(self.toy_robot_placement._x_coord, normal_x + 1)
        self.assertEqual(self.toy_robot_placement._y_coord, normal_y)
        self.assertEqual(self.toy_robot_placement._current_facing, FacingDirection.EAST)

        # Ignore out-of-table move
        self.toy_robot_placement._handle_move(args)
        self.assertEqual(self.toy_robot_placement._x_coord, normal_x + 1)
        self.assertEqual(self.toy_robot_placement._y_coord, normal_y)
        self.assertEqual(self.toy_robot_placement._current_facing, FacingDirection.EAST)

    def test_handle_right(self):
        # Place first
        normal_x = self.toy_robot_placement.MAX_UNIT_SIZE - 2
        normal_y = self.toy_robot_placement.MAX_UNIT_SIZE - 2
        args = (str(normal_x), str(normal_y), 'EAST')
        self.toy_robot_placement._handle_place(args)

        self.toy_robot_placement._handle_right(args)
        self.assertEqual(self.toy_robot_placement._x_coord, normal_x)
        self.assertEqual(self.toy_robot_placement._y_coord, normal_y)
        self.assertEqual(self.toy_robot_placement._current_facing, FacingDirection.SOUTH)

    def test_handle_left(self):
        # Place first
        normal_x = self.toy_robot_placement.MAX_UNIT_SIZE - 2
        normal_y = self.toy_robot_placement.MAX_UNIT_SIZE - 2
        args = (str(normal_x), str(normal_y), 'EAST')
        self.toy_robot_placement._handle_place(args)

        self.toy_robot_placement._handle_left(args)
        self.assertEqual(self.toy_robot_placement._x_coord, normal_x)
        self.assertEqual(self.toy_robot_placement._y_coord, normal_y)
        self.assertEqual(self.toy_robot_placement._current_facing, FacingDirection.NORTH)


if __name__ == '__main__':
    unittest.main()
