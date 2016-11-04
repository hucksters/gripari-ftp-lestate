#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from transliterate import translit
import gripari_ftp_lestate.enricher as lest


@pytest.fixture(scope="module")
def xml(request):
    _xml = b""

    with open(
            "/Users/dpetrov/Projects/Hucksters/data/ReportRetail_LEST-000204_2016.xml",
            "rb") as src:
        _xml = src.read()

    return _xml


def test_xmlToKV(xml):
    assert "d74a47f8-9df8-11e6-9844-448a5b8e765b" in lest.xmlToKV(xml).keys()


def test_enrich(xml):
    enriched = lest.enrich(lest.xmlToKV(xml))
    assert len(enriched) > 0
    assert "d74a47f8-9df8-11e6-9844-448a5b8e765b" in set([x.get(translit(
        "ID", "ru")) for x in enriched])


def test_flatten():
    assert lest.flatten([{'a': 1,
                          'b': [1, 2]}]) == [{'a': 1,
                                              'b': 1}, {'a': 1,
                                                        'b': 2}]
    assert lest.flatten([{'a': {'b': [1, 2]}}]) == [{'a': {'b': 1}},
                                                    {'a': {'b': 2}}]
    assert lest.flatten([{'a': 1,
                          'b': {'c': [1, 2]}}]) == [{'a': 1,
                                                     'b': {'c': 1}},
                                                    {'a': 1,
                                                     'b': {'c': 2}}]

    assert lest.flatten([{'a': 1,
                          'b': [{'c': 1}]}]) == [{'a': 1,
                                                  'b': {'c': 1}}]
    assert lest.flatten([{'a': 1,
                          'b': {'c': [1, 2],
                                'e': [3]}}]) == [{'a': 1,
                                                  'b': {
                                                      'c': 1
                                                  }}, {'a': 1,
                                                       'b': {'c': 2}},
                                                 {'a': 1,
                                                  'b': {'e': 3}}]
