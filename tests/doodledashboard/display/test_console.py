import click
import unittest
from unittest.mock import Mock

from click.testing import CliRunner
from parameterized import parameterized

import os
from os import path

from doodledashboard.displays.console import ConsoleDisplay, ConsoleDisplayCreator
from doodledashboard.notifications.outputs import TextNotificationOutput, ImageNotificationOutput


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def resolve_data_path(filename):
    data_dir = path.join(get_current_directory(), "data/")
    return path.join(data_dir, filename)


class TestConsoleDisplay(unittest.TestCase):

    def test_id(self):
        self.assertEqual("console", ConsoleDisplayCreator().get_id())

    def test_warning_shown_for_unsupported_notifications(self):
        image_notification = None
        cmd = create_cmd(lambda: ConsoleDisplay(False).draw(image_notification))
        result = CliRunner().invoke(cmd, catch_exceptions=False)

        self.assertEqual("Notification type 'None' not supported by this display", result.output)


class TestTextNotification(unittest.TestCase):

    @parameterized.expand([
        ((1, 1), "", resolve_data_path("empty.txt")),
        ((10, 3), "a", resolve_data_path("single-letter.txt")),
        ((10, 3), "centred", resolve_data_path("single-centred-word.txt")),
        ((10, 3), "I'm centred", resolve_data_path("multiline-centred.txt")),
        ((10, 3), "Hello World! This is too long", resolve_data_path("trim-multiline-centred.txt")),
    ])
    def test_centred(self, console_size, input_text, expected_ascii_terminal_path):
        text_output = TextNotificationOutput(input_text)

        console = ConsoleDisplay(show_notification_name=False, period=0, get_size=lambda: console_size)
        cmd = create_cmd(lambda: console.draw(text_output))
        result = CliRunner().invoke(cmd, catch_exceptions=False)

        with open(expected_ascii_terminal_path, "r") as f:
            expected_terminal_output = f.read()
        self.assertEqual(expected_terminal_output, result.output)

    def test_console_resizes_dynamically(self):
        mock_size_getter = Mock()
        mock_size_getter.side_effect = [(5, 1), (5, 2)]

        text_output = TextNotificationOutput("Hello World")

        console = ConsoleDisplay(show_notification_name=False, period=0, get_size=mock_size_getter)
        cmd1 = create_cmd(lambda: console.draw(text_output))
        cmd2 = create_cmd(lambda: console.draw(text_output))
        result1 = CliRunner().invoke(cmd1, catch_exceptions=False)
        result2 = CliRunner().invoke(cmd2, catch_exceptions=False)

        self.assertEqual("Hello", result1.output)
        self.assertEqual("Hello\nWorld", result2.output)


class TestImageNotification(unittest.TestCase):

    def test_conversion(self):
        console_size = (10, 5)
        input_image = resolve_data_path("black-box.gif")
        expected_ascii_output_file = resolve_data_path("black-box.gif.10x5.txt")

        image_output = ImageNotificationOutput(input_image)

        console = ConsoleDisplay(show_notification_name=False, period=0, get_size=lambda: console_size)
        cmd = create_cmd(lambda: console.draw(image_output))
        result = CliRunner().invoke(cmd, catch_exceptions=False)

        with open(expected_ascii_output_file, "r") as f:
            expected_terminal_output = f.read()
        self.assertIn(expected_terminal_output, result.output)


def create_cmd(func):
    @click.command()
    def c(f=func):
        f()

    return c


if __name__ == "__main__":
    unittest.main()
