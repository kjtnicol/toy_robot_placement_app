from toy_robot_app.toy_robot_placement_impl import ToyRobotPlacement


class ToyRobotAppRunner:
    def __init__(self, input_file_name: str):
        self._input_file_name = input_file_name
        self._toy_robot_placement = ToyRobotPlacement()

    def load_file_and_run(self):
        with open(self._input_file_name, 'r') as input_file:
            for line in input_file:
                try:
                    command_list = line.split()
                    command = command_list[0]
                    args = command_list[1].split(',') if len(command_list) > 1 else []
                except Exception as e:
                    print(f'Invalid command line=[{line}]')
                    return

                self._toy_robot_placement.apply_command(command, *args)
