# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:11:32 2015

@author: pick
"""

import copy
import os

from future.utils import iteritems

import odml
from odmltables.odml_table import OdmlTable
from odmltables.odml_table import OdmlDtypes
from odmltables.odml_csv_table import OdmlCsvTable
from odmltables.odml_xls_table import OdmlXlsTable

from create_test_odmls import (create_small_test_odml, create_showall_test_odml,
                                create_compare_test)

import unittest


class TestLoadOdmlFromTable(unittest.TestCase):
    def setUp(self):
        self.test_table = OdmlTable()
        self.filename = 'testtable'
        self.filetype = ''

    def tearDown(self):
        pass

    def test_load_from_csv(self):
        self.filetype = 'csv'
        table = OdmlCsvTable()
        table.load_from_function(create_small_test_odml)
        dict_in = [{key: dic[key] if dic[key] is not None
        else '' for key in dic} for dic in table._odmldict]
        table.change_header(Path=1, SectionName=2, SectionType=3,
                            SectionDefinition=4, PropertyName=5,
                            PropertyDefinition=6, Value=7,
                            DataUnit=9, DataUncertainty=10, odmlDatatype=11)
        table.write2file(self.filename + '.' + self.filetype)
        self.test_table.load_from_csv_table(self.filename + '.' + self.filetype)
        dict_out = self.test_table._odmldict
        self.assertEquals(dict_in, dict_out)

    def test_load_from_xls(self):
        self.filetype = 'xls'
        table = OdmlXlsTable()
        table.load_from_function(create_small_test_odml)
        dict_in = [{key: dic[key] if dic[key] is not None
        else '' for key in dic} for dic in table._odmldict]
        table.change_header(Path=1, SectionName=2, SectionType=3,
                            SectionDefinition=4, PropertyName=5,
                            PropertyDefinition=6, Value=7,
                            DataUnit=8, DataUncertainty=9, odmlDatatype=10)
        table.write2file(self.filename + '.' + self.filetype)
        self.test_table.load_from_xls_table(self.filename + '.' + self.filetype)
        dict_out = self.test_table._odmldict
        self.assertEquals(dict_in, dict_out)

    def test_load_from_file(self):
        self.filetype = 'odml'
        table = OdmlTable()
        table.load_from_function(create_small_test_odml)
        dict_in = copy.deepcopy(table._odmldict)
        table.write2odml(self.filename + '.' + self.filetype)
        new_test_table = OdmlTable(self.filename + '.' + self.filetype)
        dict_out = new_test_table._odmldict

        self.assertEquals(dict_in, dict_out)


class TestLoadSaveOdml(unittest.TestCase):
    """
    class to test loading the odml
    """

    def setUp(self):
        self.test_table = OdmlTable()
        self.expected_odmldict = [{'PropertyDefinition': None,
                                   'Value': ['bla'],
                                   'odmlDatatype': 'text',
                                   'DataUnit': None,
                                   'SectionType': None,
                                   'DataUncertainty': None,
                                   'SectionDefinition': None,
                                   'Path': '/section1:property1'}]

    def test_load_from_file(self):
        """
        test loading the odml-dictionary from an odml-file
        """
        filename = 'tmp_testfile.odml'
        doc = create_small_test_odml()
        odml.tools.xmlparser.XMLWriter(doc).write_file(filename)
        self.test_table.load_from_file(filename)
        os.remove(filename)
        self.assertEqual(self.test_table._odmldict, self.expected_odmldict)

    def test_load_from_function(self):
        """
        test loading the odml-dictionary from a function that generates an
        odml-document in python
        """
        self.test_table.load_from_function(create_small_test_odml)
        self.assertEqual(self.test_table._odmldict, self.expected_odmldict)

    def test_load_from_odmldoc(self):
        """
        test loading the odml-dictionary from an odml-document in python
        """
        doc = create_small_test_odml()
        self.test_table.load_from_odmldoc(doc)
        self.assertEqual(self.test_table._odmldict, self.expected_odmldict)

    def test_write2odml(self):
        """
        test writing the odmldict back to an odml-file
        """
        file1 = 'test.odml'
        file2 = 'test2.odml'
        doc = create_showall_test_odml()
        self.test_table.load_from_odmldoc(doc)
        odml.tools.xmlparser.XMLWriter(doc).write_file(file1)

        self.test_table.change_header(Path=1, SectionName=2, SectionType=3,
                                      SectionDefinition=4, PropertyName=5,
                                      PropertyDefinition=6, Value=7, DataUnit=9,
                                      DataUncertainty=10, odmlDatatype=11)
        self.test_table.write2odml(file2)

        self.test_table.load_from_file(file1)
        expected = self.test_table._odmldict
        self.test_table.load_from_file(file2)
        self.assertEqual(expected, self.test_table._odmldict)

        os.remove(file1)
        os.remove(file2)


class TestChangeHeader(unittest.TestCase):
    def setUp(self):
        self.test_table = OdmlTable()

    def test_simple_change(self):
        """
        Tests simple changing of the header
        """
        self.test_table.change_header(Path=1, SectionType=2, Value=3)
        self.assertEqual(self.test_table._header, ["Path", "SectionType",
                                                   "Value"])

    def test_index_zero(self):
        """
        Test change_header with using the index 0
        """
        # TODO: change as exception is changed
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=0, SectionType=1, Value=2)

    def test_negative_index(self):
        """
        Test change_header with using a negative index
        """
        # TODO: change Exception
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=-1)

    def test_empty_cols_allowed(self):
        """
        Test change_header leaving empty columns, while it is allowed
        """
        self.test_table.allow_empty_columns = True
        self.test_table.change_header(Path=1, SectionType=3, Value=4)
        self.assertEqual(self.test_table._header, ["Path", None, "SectionType",
                                                   "Value"])

    def test_same_indizes(self):
        """
        Test change_header with two columns with same indizes
        """
        # TODO: Exception
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=1, SectionType=1, Value=2)

    def test_wrong_keyword(self):
        """
        Test using change_header with a wrong keyword
        """
        # TODO: Exception
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=1, Sectionname=2, Value=3)


class TestOdmlTable(unittest.TestCase):
    """
    class to test the other functions of the OdmlTable-class
    """

    def setUp(self):
        self.test_table = OdmlTable()

    def test_change_titles(self):
        """
        changing the header_titles
        """
        expected = {"Path": "Pfad",
                    "SectionName": "Section Name",
                    "SectionType": "Section Type",
                    "SectionDefinition": "Section Definition",
                    "PropertyName": "Eigenschaft",
                    "PropertyDefinition": "Property Definition",
                    "Value": "Wert",
                    "DataUnit": "Einheit",
                    "DataUncertainty": "Data Uncertainty",
                    "odmlDatatype": "Datentyp"}
        self.test_table.change_header_titles(Path="Pfad",
                                             PropertyName="Eigenschaft",
                                             Value="Wert", DataUnit="Einheit",
                                             odmlDatatype="Datentyp")
        self.assertEqual(self.test_table._header_titles, expected)

    def test_merge(self):
        doc1 = create_compare_test(sections=2, properties=2, levels=2)

        # generate one additional Value, which is not present in doc2
        doc1.sections[1].properties[0].value.append('42')

        # generate one additional Property, which is not present in doc2
        doc1.sections[0].append(odml.Property(name='Doc1Property2', value=5))

        # generate one additional Section, which is not present in doc2
        new_prop = odml.Property(name='Doc1Property2', value=10)
        new_sec = odml.Section(name='Doc1Section')
        new_sec.append(new_prop)
        doc1.sections[0].append(new_sec)

        self.test_table.load_from_odmldoc(doc1)

        doc2 = create_compare_test(sections=3, properties=3, levels=3)
        table2 = OdmlTable()
        table2.load_from_odmldoc(doc2)

        backup_table = copy.deepcopy(self.test_table)

        self.test_table.merge(doc2, mode='append')
        backup_table.merge(table2, mode='append')

        self.assertListEqual(self.test_table._odmldict, backup_table._odmldict)

        expected = len(table2._odmldict) + 2  # only additional prop and
        # section will be counted; additional value is overwritten

        self.assertEqual(len(self.test_table._odmldict), expected)

    def test_strict_merge_error(self):
        doc1 = create_compare_test(sections=2, properties=2, levels=2)

        # add property with same name but different content
        old_name = doc1.sections[1].properties[0].name
        doc1.sections[1].remove(doc1.sections[1].properties[0])
        doc1.sections[1].append(odml.Property(name=old_name,
                                                       value='myval', dtype=odml.DType.string))

        self.test_table.load_from_odmldoc(doc1)

        doc2 = create_compare_test(sections=3, properties=3, levels=3)
        table2 = OdmlTable()
        table2.load_from_odmldoc(doc2)

        with self.assertRaises(ValueError):
            self.test_table.merge(doc2, mode='strict')

    def test_strict_merge(self):
        doc1 = create_compare_test(sections=0, properties=1, levels=2)
        doc1.sections[0].properties[0].value[0] = -1
        self.test_table.load_from_odmldoc(doc1)

        doc2 = create_compare_test(sections=0, properties=1, levels=2)
        table2 = OdmlTable()
        table2.load_from_odmldoc(doc2)
        self.test_table.merge(doc2, mode='strict')

        self.assertListEqual(table2._odmldict, self.test_table._odmldict)


class TestFilter(unittest.TestCase):
    """
    class to test the other functions of the OdmlTable-class
    """

    def setUp(self):
        self.test_table = OdmlTable()
        self.test_table.load_from_odmldoc(create_compare_test(levels=2))

    def test_filter_errors(self):
        """
        test filter function for exceptions
        """

        with self.assertRaises(ValueError):
            self.test_table.filter()

        with self.assertRaises(ValueError):
            self.test_table.filter(mode='wrongmode', Property='Property')

    def test_filter_mode_and(self):
        """
        testing mode='and' setting of filter function
        """

        self.test_table.filter(mode='and', invert=False, SectionName='Section2',
                               PropertyName='Property2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(4, num_props_new)

    def test_filter_mode_or(self):
        """
        testing mode='or' setting of filter function
        """

        self.test_table.filter(mode='or', invert=False, SectionName='Section2',
                               PropertyName='Property2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(17, num_props_new)

    def test_filter_invert(self):
        """
        testing invert setting of filter function
        """

        num_props_original = len(self.test_table._odmldict)
        self.test_table.filter(mode='or', invert=True, SectionName='Section2',
                               PropertyName='Property2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(num_props_original - 17, num_props_new)

    def test_filter_recursive(self):
        """
        testing recursive setting of filter function
        """

        # total_number of properties
        doc = self.test_table.convert2odml()
        tot_props = len(list(doc.iterproperties()))
        sec2s = list(doc.itersections(filter_func=lambda x: x.name == 'Section2'))
        sec2_props = sum([len(list(sec.properties)) for sec in sec2s])

        # removing all sections with name 'Section2' independent of location in odml tree
        self.test_table.filter(mode='and', recursive=True, invert=True, SectionName='Section2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(tot_props - sec2_props, num_props_new)

    def test_filter_comparison_func_false(self):
        """
        keeping/removing all properties by providing True/False as comparison function
        """

        num_props_original = len(self.test_table._odmldict)
        self.test_table.filter(comparison_func=lambda x, y: True, PropertyName='')
        self.assertEqual(len(self.test_table._odmldict), num_props_original)

        self.test_table.filter(comparison_func=lambda x, y: False, PropertyName='')
        self.assertEqual(len(self.test_table._odmldict), 0)


class TestOdmlDtypes(unittest.TestCase):
    """
    class to test the other functions of the OdmlDtype-class
    """

    def setUp(self):
        self.test_dtypes = OdmlDtypes()

    def test_defaults(self):
        expected_basedtypes = list(self.test_dtypes.default_basedtypes)
        self.assertListEqual(sorted(expected_basedtypes), sorted(self.test_dtypes.basedtypes))

        expected_synonyms = self.test_dtypes.default_synonyms
        self.assertEqual(expected_synonyms, self.test_dtypes.synonyms)

    def test_valid_dtypes(self):
        expected_dtypes = list(self.test_dtypes.default_basedtypes) + list(
            self.test_dtypes.default_synonyms)
        self.assertListEqual(sorted(expected_dtypes), sorted(self.test_dtypes.valid_dtypes))

    def test_default_values(self):
        basedefaults = self.test_dtypes.default_basedtypes
        syndefaults = dict([(syn, basedefaults[base]) for syn, base in
                            iteritems(self.test_dtypes.default_synonyms)])
        expected_defaults = basedefaults.copy()
        expected_defaults.update(syndefaults)

        self.assertEqual(expected_defaults, self.test_dtypes.default_values)

        for dtype, expected_default in iteritems(expected_defaults):
            self.assertEqual(expected_default, self.test_dtypes.default_value(dtype))

    def test_synonym_adder(self):
        basedtype, synonym = ('int', 'testsyn1')
        self.test_dtypes.add_synonym(basedtype, synonym)

        expected_synonyms = self.test_dtypes.default_synonyms.copy()
        expected_synonyms.update({synonym: basedtype})
        self.assertEqual(self.test_dtypes.synonyms, expected_synonyms)
        self.assertEqual(self.test_dtypes.default_value('testsyn1'),
                         self.test_dtypes.default_value('int'))

    def test_basedtype_adder(self):
        basedtype, default = 'testbasetype', 'testdefault'
        self.test_dtypes.add_basedtypes(basedtype, default)

        expected_basedtypes = self.test_dtypes.default_basedtypes.copy()
        expected_basedtypes.update({basedtype: default})
        self.assertListEqual(self.test_dtypes.basedtypes, list(expected_basedtypes))

    def test_default_value_setter(self):
        default_value = 1
        self.test_dtypes.set_default_value('int', default_value)

        self.test_dtypes.default_value('int')

        self.assertEqual(self.test_dtypes.default_value('int'), default_value)


if __name__ == '__main__':
    unittest.main()
