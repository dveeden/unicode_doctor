#!/usr/bin/python3
from unicode_doctor import DecodeEncodeUnicodeDoctor, ForcedAsciiUnicodeDoctor
import unittest

class DecodeEncodeUnicodeDoctorTest(unittest.TestCase):
    def setUp(self):
        self.guess = DecodeEncodeUnicodeDoctor.make_guess

    def test_utf8_iso8859(self):
        for res in self.guess(str_good='Daniël',str_bad='DaniÃ«l'):
            self.assertRegex(res.issue, 'encoded with utf-8 and decoded with iso-8859-1')

    def test_iso8859_ibm850(self):
        for res in self.guess(str_good='Daniël',str_bad='DaniÙl'):
            self.assertRegex(res.issue, 'encoded with iso-8859-1 and decoded with ibm850')

class ForcedAsciiUnicodeDoctorTest(unittest.TestCase):
    def setUp(self):
        self.guess = ForcedAsciiUnicodeDoctor.make_guess

    def test_closest_ascii(self):
        for res in self.guess(str_good='Daniël',str_bad='Daniel'):
            self.assertRegex(res.issue, 'converted to the closest ASCII representation.')

    def test_non_ascii_stripped(self):
        for res in self.guess(str_good='Daniël',str_bad='Danil'):
            self.assertRegex(res.issue, 'stripped of non-ASCII characters')

    def test_non_ascii_replaced(self):
        for res in self.guess(str_good='Daniël',str_bad='Dani?l'):
            self.assertRegex(res.issue, 'non-ASCII characters replaced')
