import sys
import argparse

class CustomArgumentParser(argparse.ArgumentParser):
    def _get_action_from_name(self, name):
        if name is None:
            return None
        for action in self._actions:
            if action.option_strings and '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action
        return None

    def error(self, message):
        exception = sys.exc_info()[1]
        if exception:
            if not hasattr(exception, 'argument'):
                exception.argument = self._get_action_from_name(exception.argument_name)
            raise exception
        super().error(message)