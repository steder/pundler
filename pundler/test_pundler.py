"""
"""
try:
    from io import StringIO
except ImportError:
    import StringIO
import sys
import textwrap
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from mock import patch

from pundler import core


class TestPundler(unittest.TestCase):
    def test_(self):
        self.assertEqual(1+1, 2)


class TestGetRequirementsFile(unittest.TestCase):
    """
    """
    @patch("os.path.exists")
    def test_no_requirements_file(self, mock_exists):
        mock_exists.return_value = False
        self.assertIsNone(core.get_requirement_file(), None)

    @patch("os.path.exists")
    def test_requirements_in_exists(self, mock_exists):
        mock_exists.side_effect = lambda x: x == 'requirements.in'
        self.assertEquals(core.get_requirement_file(), 'requirements.in')

    @patch("os.path.exists")
    def test_requirements_yml_exists(self, mock_exists):
        mock_exists.side_effect = lambda x: x == 'requirements.yml'
        self.assertEquals(core.get_requirement_file(), 'requirements.yml')



class TestGetRequirements(unittest.TestCase):
    """
    """
    def test_get_requirements_empty(self):
        result = list(core.get_requirements(None))
        self.assertEqual(result, [])

    # @patch("builtins.open")
    # def test_get_requirements_in_file_empty(self, mock_open):
    #     manager = mock_open.return_value.__enter__.return_value
    #     manager.readlines.return_value = StringIO("")

    #     result = list(core.get_requirements("requirements.in"))
    #     self.assertEquals(result, [])

    # @patch("builtins.open")
    # def test_get_requirements_in_file(self, mock_open):
    #     manager = mock_open.return_value.__enter__.return_value
    #     manager.readlines.return_value = StringIO(textwrap.dedent("""dep1
    #     dep2"
    #     """))
    #     result = list(core.get_requirements("requirements.in"))
    #     self.assertEquals(result, ['dep1'])
