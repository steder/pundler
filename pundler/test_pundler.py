"""
"""
try:
    import builtins as builtins
except:
    import __builtin__ as builtins # NOQA

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
import six

from pundler import core


class TestPundler(unittest.TestCase):
    def test_(self):
        self.assertEqual(1+1, 2)


class TestGetRequirementsFile(unittest.TestCase):
    @patch("os.listdir")
    def test_no_requirements_file(self, mock_listdir):
        mock_listdir.return_value = []
        self.assertEquals(core.get_requirement_files(), [])

    @patch("os.listdir")
    def test_requirements_in_exists(self, mock_listdir):
        mock_listdir.return_value = ['requirements.in']
        self.assertEquals(core.get_requirement_files(), ['requirements.in'])

    @patch("os.listdir")
    def test_requirements_yml_exists(self, mock_listdir):
        """We don't yet support yaml"""
        mock_listdir.return_value = ['requirements.yml']
        self.assertEquals(core.get_requirement_files(), [])



class TestGetRequirements(unittest.TestCase):
    @patch.object(builtins, "open")
    def test_get_requirements_empty(self, mock_open):
        result = list(core.get_requirements("requirements.in"))
        self.assertEqual(result, [])

    @patch.object(builtins, "open")
    def test_get_requirements_in_file_empty(self, mock_open):
        manager = mock_open.return_value.__enter__.return_value
        manager.readlines.return_value = StringIO(six.u(""))

        result = list(core.get_requirements("requirements.in"))
        self.assertEquals(result, [])

    @patch.object(builtins, "open")
    def test_get_requirements_in_file(self, mock_open):
        manager = mock_open.return_value.__enter__.return_value
        manager.readlines.return_value = StringIO(textwrap.dedent(six.u("""dep1
        dep2
        """)))
        result = list(core.get_requirements("requirements.in"))
        self.assertEquals(result, ['dep1', 'dep2'])
