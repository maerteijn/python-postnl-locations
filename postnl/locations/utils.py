from suds.sudsobject import asdict
from suds.sax.text import Text


def recursive_asdict(d):
    """
    Recursively convert Suds object into dict.
    We convert the keys to lowercase, and convert sax.Text
    instances to Unicode.

    Taken from:
    http://stackoverflow.com/a/15678861/202168

    Let's create a suds object from scratch with some lists and stuff
    >>> from suds.sudsobject import Object as SudsObject
    >>> sudsobject = SudsObject()
    >>> sudsobject.Title = "My title"
    >>> sudsobject.JustAList = [1, 2, 3]
    >>> sudsobject.Child = SudsObject()
    >>> sudsobject.Child.Title = "Child title"
    >>> sudsobject.Child.AnotherList = ["4", "5", "6"]
    >>> childobject = SudsObject()
    >>> childobject.Title = "Another child title"
    >>> sudsobject.Child.SudObjectList = [childobject]

    Now see if this works:
    >>> result = recursive_asdict(sudsobject)
    >>> result['title']
    'My title'
    >>> result['child']['anotherlist']
    ['4', '5', '6']
   """
    out = {}
    for k, v in asdict(d).items():
        k = k.lower()
        if hasattr(v, '__keylist__'):
            out[k] = recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(
                        item.title() if isinstance(item, Text) else item)
        else:
            out[k] = v.title() if isinstance(v, Text) else v
    return out
