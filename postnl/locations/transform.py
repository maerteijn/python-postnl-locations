import re


class TransformPostNLResults(object):
    def __init__(self, data=[]):
        """
        Transform the results from the PostNL webservice to a more sane result.

        The only thing you need to define is a transform_<key> method to
        transform the data, see examples below.

        >>> from postnl.locations.tests import another_mock_result
        >>> transformer = TransformPostNLResults(data=another_mock_result)
        >>> print(transformer.data[0]['openinghours']['monday'])
        11:00-18:00
        >>> print(transformer.data[0]['address']['remark'])
        This is a remark
        """
        for location in data:
            for key in location:
                transform_function = "transform_%s" % key
                if hasattr(self, transform_function):
                    location[key] = getattr(
                        self, transform_function)(location[key])
        self.data = data

    def transform_openinghours(self, value):
        """Remove the 'string' key from the value"""
        for day in value:
            value[day] = value[day]['string'][0]
        return value

    def transform_address(self, value):
        """Make sure the remarks field is sanely upper/lowecase"""

        def uppercase(matchobj):
            return matchobj.group(0).upper()

        def capitalize(s):
            return re.sub(
                '^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)', uppercase, s)

        value['remark'] = capitalize(value['remark'].lower())
        return value
