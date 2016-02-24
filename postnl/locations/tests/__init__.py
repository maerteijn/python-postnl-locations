from unittest import TestCase
from suds.sudsobject import Object as SudsObject
import mock

from postnl.locations.client import Locations
from postnl.locations.settings import POSTNL_SETTINGS


mock_result = [{
    'partnername': u'Postnl', 'distance': u'409', 'name': u'Primera',
    'retailnetworkid': u'Pnpnl-01', 'terminaltype': u'Nrs',
    'deliveryoptions': {'string': ["DO", "PG", "UL"]},
    'longitude': u'5.91555826407064', 'phonenumber': u'026-4457665',
    'address': {
        'city': u'Arnhem',
        'remark': u'', 'countrycode': u'Nl',
        'housenr': u'17', 'zipcode': u'6828Ca', 'housenrext': u'A',
        'street': u'Steenstraat'},
    'latitude': u'51.9837221431004',
    'openinghours': {
        'monday': {'string': [u"11:00-18:00"]},
        'tuesday': {'string': [u"09:00-18:00"]},
        'friday': {'string': [u"09:00-18:00"]},
        'wednesday': {'string': [u"09:00-18:00"]},
        'thursday': {'string': [u"09:00-18:00"]},
        'saturday': {'string': [u"09:00-17:00"]}},
    'saleschannel': u'Pkt L', 'locationcode': u'163392'
}]

mock_error_result = {
    'faultcode': u'S:Cif Framework Message Interceptor',
    'faultstring': u'Check Cifexception In The Detail Section',
    'detail': {
        'cifexception': {
            'errors': {
                'exceptiondata': {
                    'errormsg': u'The Username/Password Is Incorrect.',
                    'errornumber': u'1',
                    'description': None
                }
            }
        }
    }
}


class TestLocations(TestCase):
    def setUp(self):
        self.locations = Locations(settings=POSTNL_SETTINGS)

    def test_nearest_locations(self):
        """Test nearest PostNL Pickup locations based on postal code"""
        # first create a mock for the soap result
        mock_object = SudsObject()
        mock_object.GetLocationsResult = SudsObject()
        mock_object.GetLocationsResult.ResponseLocation = mock_result

        # mock the function call and return a almost like soap object
        self.locations.client.service.GetNearestLocations = mock.MagicMock()
        # the first param is the http status code
        self.locations.client.service.GetNearestLocations.return_value = (200, mock_object)  # noqa

        # do the call
        result = self.locations.nearest_locations(postalcode="6821AD")
        self.assertEqual(result, (200, mock_result))

    def test_no_results(self):
        """Test when the soap service does not find any results"""
        # first create a mock for the soap result
        # empty result sets do not have the GetLocationsResult property, so
        # we just have this mick object
        mock_object = SudsObject()

        # mock the function call and return a almost like soap object
        self.locations.client.service.GetNearestLocations = mock.MagicMock()
        # the first param is the http status code
        self.locations.client.service.GetNearestLocations.return_value = (200, mock_object)  # noqa

        # do the call
        result = self.locations.nearest_locations(postalcode="6821 AD")
        self.assertEqual(result, (200, []))

    def test_error_handling(self):
        """See if our client returns the error properly"""
        # let's mock again
        self.locations.client.service.GetNearestLocations = mock.MagicMock()
        mock_error = SudsObject()
        mock_error.Fault = mock_error_result
        self.locations.client.service.GetNearestLocations.return_value = (500, mock_error)  # noqa

        # and call it
        result = self.locations.nearest_locations(postalcode="6821AD")
        self.assertEqual(result[0], 500)
