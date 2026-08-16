import unittest

from greeting import greet


class GreetingTests(unittest.TestCase):
    def test_greet(self) -> None:
        self.assertEqual(greet("Ada"), "Hello, Ada!")
