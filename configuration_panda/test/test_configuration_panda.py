import os
from unittest import TestCase
import pytest

from ..configuration_panda import ConfigurationPanda
from ..exceptions import (
    DuplicateJSONFile, InvalidParameter, ExistingEnvironmentVariable)


class Test_ConfigurationPanda(TestCase):
    """
    Exercises the functionality of the ConfigurationPanda class.

    """

    @classmethod
    def setUpClass(cls):
        test_file_path = os.path.dirname(__file__)

        os.environ['PRIMARY_CONFIGURATION_FILES'] = \
            test_file_path + '/primary_configuration_files'
        os.environ['SECONDARY_CONFIGURATION_FILES'] = \
            test_file_path + '/secondary_configuration_files'
        os.environ['DUPLICATE_CONFIGURATION_FILES'] = \
            test_file_path + '/duplicate_configuration_files'

    # def tearDown(self):
    #     #Remove all environment variables set during setUp().
    #     for variable in self.configuration_panda.environment_variables:
    #         del os.environ[variable]

    def test_constructor_with_invalid_environment_variables(self):
        """
        Prove __init__() throws InvalidParameter when given a bad env_var.

        """
        with pytest.raises(InvalidParameter):
            ConfigurationPanda(['NON_EXISTENT_ENV_VAR'])

    def test_constructor_attribute_existence(self):
        """
        Prove that the constructor executed in the setUp() method
        correctly sets object attributes based on the ldap.json
        and environment_variables.json mock configuration files
        included in the 'primary_configuration_files' directory.

        """
        configuration_panda = ConfigurationPanda(
            ['PRIMARY_CONFIGURATION_FILES'])

        assert hasattr(configuration_panda, 'ldap')
        assert hasattr(configuration_panda, 'environment_variables')

    def test_constructor_duplicate_configuration_filenames(self):
        """
        Prove that ConfigurationPanda.__init__() throws a
        DuplicateJSONFile when more an attempt is made to
        load data onto an existing object attribute (which would only happen
        if a filename being loaded has a name collision with an existing
        object attribute).

        """

        # Test for duplicate file names in distinct directories.
        self.assertRaises(
            DuplicateJSONFile,
            ConfigurationPanda,
            ['PRIMARY_CONFIGURATION_FILES', 'DUPLICATE_CONFIGURATION_FILES']
        )

        # Test for duplicate file names as a result of passing the
        # same environment variable into the constructor multiple times.
        self.assertRaises(
            DuplicateJSONFile,
            ConfigurationPanda,
            ['PRIMARY_CONFIGURATION_FILES', 'PRIMARY_CONFIGURATION_FILES']
        )

    def test_constructor_with_overriding_env_var(self):
        """
        Prove that ConfigurationPanda.__init__() throws an
        ExistingEnvironmentVariable exception when an attempt is made
        to set the value of an existing environment variable.

        """

        self.assertRaises(ExistingEnvironmentVariable,
                          ConfigurationPanda,
                          ['PRIMARY_CONFIGURATION_FILES'])

    def test_constructor_for_environment_variable_assignment(self):
        """
        Prove that ConfigurationPanda.__init__() sets environment variables
        from the contents of a file called 'environment_variables.json'
        when it located during the JSON file search.

        """

        self.assertEqual(os.environ['MY_FAVORITE_FOOD'], "Dumplings")
        self.assertEqual(os.environ['MY_WORST_NIGHTMARE'], "The Noodle Dream")