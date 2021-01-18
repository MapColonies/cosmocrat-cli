import argparse
from abc import ABC as AbstractBaseClass, abstractmethod

class BaseActionValidator(AbstractBaseClass, argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value_to_validate = values
        self.validate(value_to_validate)
        setattr(namespace, self.dest, value_to_validate)

    @abstractmethod
    def validate(self, value):
        pass