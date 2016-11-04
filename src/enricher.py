#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmltodict
import collections
from transliterate import translit
from typing import Dict, Any, Text, List


def xmlToKV(xml: Text) -> Dict[Text, Any]:
    """
    Create key value storage from dict and store there xml elemes.
    """
    xmlelems = xmltodict.parse(xml)

    register = dict()

    for _, element in xmlelems[list(xmlelems.keys())[0]].items():
        if isinstance(element, dict):
            register[element.get(translit("ID", "ru"), -1)] = element
        elif isinstance(element, list):
            for el in element:
                register[el.get(translit("ID", "ru"), -1)] = el

    return register


def enrich(kv: Dict[Text, Any]) -> List[Dict[Any, Any]]:
    """
    Enrich elements from kv with possible elements from kv.
    """

    def _enrich(_id, _body):
        if isinstance(_body, collections.OrderedDict):
            return {k: _enrich(_id, v) for k, v in _body.items()}
        elif isinstance(_body, list):
            return [_enrich(_id, el) for el in _body]
        else:
            if _body in kv:
                if _body != _id:
                    if _body not in used:
                        used.add(_body)
                        return _enrich(_body, kv[_body])
                    else:
                        return kv[_body]
            return _body

    res = []
    used = set()

    for _id, body in kv.items():
        res.append((_id, _enrich(_id, body)))

    return [el[1] for el in res if el[0] not in used]


def flatten(values: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
    """
    Flatten list of dict. For every dict from list when dict has list
    we extract values from it and create new dict.
    Example:

    flatten([{'a': 1, 'b': [1,2]}]) = [{'a':1, 'b':1},{'a':1, 'b':2}]

    Warning! We don't have here task for flatten dict. Our problem is next
    we have record where someone collect values and we want unfold this record
    ex:
    flatten({'a': [1,2,3], 'b': [4]}) = [{'a': 1}, {'a': 2}, {'b': 4}, {'a':3}]
    """
    res = []
    for value in values:
        for el in _flatten(value):
            res.append(el)
    return res


def _flatten(value: Dict[Any, Any]) -> List[Dict[Any, Any]]:
    """
    Helper function for flatten.
    """
    res = []
    list_keys = []
    list_values = []
    for k, v in value.items():
        if isinstance(v, list):
            for i in v:
                list_keys.append(k)
                list_values.append(i)
        if isinstance(v, dict):
            _v = _flatten(v)
            if len(_v) > 1:
                for _i in _v:
                    list_keys.append(k)
                    list_values.append(_i)

    for k, v in zip(list_keys, list_values):
        dres = value.copy()
        dres[k] = v
        for i in set(list_keys):
            if i != k:
                dres.pop(i)
        res.append(dres)
    return res
