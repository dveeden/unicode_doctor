from abc import ABCMeta, abstractmethod
from encodings.aliases import aliases
from unicodedata import normalize
from typing import Generator


class UnicodeIssue:
    def __init__(self, issue: str) -> None:
        self.issue = issue
        self.acceptable = None  # type: bool

    def __str__(self) -> str:
        return self.issue


class BaseUnicodeDoctor(metaclass=ABCMeta):

    @abstractmethod
    def make_guess(str_good: str, str_bad: str, **kwargs) -> Generator[UnicodeIssue, None, None]:
        raise NotImplementedError


class DecodeEncodeUnicodeDoctor(BaseUnicodeDoctor):
    def make_guess(str_good: str, str_bad: str, **kwargs) -> Generator[UnicodeIssue, None, None]:

        if 'test_all' in kwargs and kwargs['test_all'] is True:
            charsets = [x for x in aliases]
        else:
            charsets = ['utf-8', 'iso-8859-1', 'utf-16', 'ibm850']

        for enc_cs in charsets:
            for dec_cs in charsets:
                try:
                    str_reencoded = str_good.encode(enc_cs, errors='ignore').decode(dec_cs, errors='ignore')
                except LookupError:
                    continue  # Not an text encoding. e.g. base64
                if str_reencoded == str_bad:
                    issue = UnicodeIssue("{good} was encoded with {enc} and decoded with {dec}. result: {bad}".format(
                                  good=str_good, enc=enc_cs, dec=dec_cs, bad=str_reencoded))
                    issue.acceptable = False
                    yield issue


class ForcedAsciiUnicodeDoctor(BaseUnicodeDoctor):
    def make_guess(str_good: str, str_bad: str, **kwargs) -> Generator[UnicodeIssue, None, None]:
        forced_str = normalize('NFKD', str_good).encode('ascii', errors='ignore').decode('utf8')
        if forced_str == str_bad:
            issue = UnicodeIssue("{good} was converted to the closest ASCII representation. result: {bad}".format(good=str_good, bad=str_bad))
            issue.acceptable = True
            yield issue

        forced_str = str_good.encode('ascii', errors='ignore').decode('utf8')
        if forced_str == str_bad:
            issue = UnicodeIssue("{good} was stripped of non-ASCII characters. result: {bad}".format(good=str_good, bad=str_bad))
            issue.acceptable = False
            yield issue

        forced_str = str_good.encode('ascii', errors='replace').decode('utf8')
        if forced_str == str_bad:
            issue = UnicodeIssue("{good} had non-ASCII characters replaced. result: {bad}".format(good=str_good, bad=str_bad))
            issue.acceptable = True
            yield issue
