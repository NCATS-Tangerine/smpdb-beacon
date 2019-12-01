import bmt

tk = None

from typing import List

DEFAULT_EDGE_LABEL = 'related_to'
DEFAULT_CATEGORY = 'named thing'

def toolkit_instance():
    global tk

    if tk is None:
        tk = bmt.Toolkit()

    return tk

def slot_uri(s:str) -> str:
    return f'https://biolink.github.io/biolink-model/docs/{s.replace(" ", "_")}.html'

def class_uri(c:str) -> str:
    camel_case = c.title().replace(' ', '')
    return f'https://biolink.github.io/biolink-model/docs/{camel_case}.html'

def is_class(c:str) -> bool:
    return toolkit_instance().is_category(c)

def is_slot(s:str) -> bool:
    return toolkit_instance().is_edgelabel(s)

def get_class(c:str):
    return toolkit_instance().get_element(c)

def get_slot(s:str):
    return toolkit_instance().get_element(s)

def ancestors(c:str) -> List[str]:
    x = get_class(c)

    if x is not None:
        if x.is_a is not None:
            return [c] + ancestors(x.is_a)
        else:
            return []
    else:
        return []
