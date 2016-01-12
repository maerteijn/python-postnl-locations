from datetime import datetime, timedelta
import suds
import time

from .settings import POSTNL_SETTINGS


class Locations(object):
    """Convenience class to communicate with the PostNL SOAP API"""
    def __init__(self):
        security = suds.wsse.Security()
        token = suds.wsse.UsernameToken(
            POSTNL_SETTINGS.get('username'), POSTNL_SETTINGS.get('password'))
        security.tokens.append(token)
        self.client = suds.client.Client(
            POSTNL_SETTINGS.get('wsdl'), autoblend=True, wsse=security)

    def create_message(self):
        # the PostNL API needs a message somehow
        message = self.client.factory.create("ns0:Message")
        message.MessageID = int(time.time() * 1000)
        message.MessageTimeStamp = time.strftime(
            "%d-%m-%Y %H:%M:%S", time.gmtime())
        return message

    def create_location(self, postalcode, deliverydate):
        location = self.client.factory.create("ns0:Location")
        location.Postalcode = postalcode
        location.DeliveryDate = deliverydate.strftime("%d-%m-%Y")
        location.AllowSundaySorting = True

        # TODO: add to settings and document it there
        delivery_options = self.client.factory.create("ns3:ArrayOfstring")
        delivery_options.string = ["PG"]
        location.DeliveryOptions = delivery_options

        # TODO: add to settings and document it there
        options = self.client.factory.create("ns3:ArrayOfstring")
        options.string = [
            "Daytime", "Evening", "Morning", "Noon", "Sunday", "Afternoon"]
        location.Options = options
        return location

    def nearest_locations(self, postalcode, deliverydate=None):
        """Returns the nearest locations based on postal code"""
        if not deliverydate:
            # then we want to see tomorrow
            tomorrow = datetime.now() + timedelta(days=1)

        location = self.create_location(postalcode, tomorrow)
        message = self.create_message()

        response = self.client.service.GetNearestLocations(
            POSTNL_SETTINGS.get('countrycode'),
            location,
            message
        )

        result = []
        for response_location in response.GetLocationsResult.ResponseLocation:
            result.append(response_location.Name.title())
        return result
