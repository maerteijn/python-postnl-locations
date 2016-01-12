from unittest import TestCase
import mock

from postnl.locations.client import Locations


class TestLocations(TestCase):
    def setUp(self):
        self.locations = Locations()

    def test_nearest_locations(self):
        """Test nearest PostNL Pickup locations based on postal code"""
        # first create a mock for the soap result
        result = mock.MagicMock()
        result.item.Name.title.return_value = u"My Location"
        result.GetLocationsResult.ResponseLocation = [result.item]

        # mock the result value
        self.locations.client.service.GetNearestLocations = mock.MagicMock()
        self.locations.client.service.GetNearestLocations.return_value = result

        # let's call it
        result = self.locations.nearest_locations(postalcode="6821AD")
        self.assertEqual(result, ["My Location"])
