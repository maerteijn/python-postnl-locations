from datetime import datetime, timedelta
from suds import client, wsse
import time

from .utils import recursive_asdict


class Locations(object):
    """Convenience class to communicate with the PostNL SOAP API"""

    def __init__(self, settings):
        self.settings = settings
        security = wsse.Security()
        token = wsse.UsernameToken(
            self.settings.get('username'), self.settings.get('password'))
        security.tokens.append(token)
        # settings faults to False makes sure we can catch the server side
        # exception message as well
        self.client = client.Client(
            self.settings.get('wsdl'), autoblend=True,
            wsse=security, faults=False)

    def create_message(self):
        """Create a message with a timestamp and unique id for the request"""
        message = self.client.factory.create("ns0:Message")
        message.MessageID = int(time.time() * 1000)
        message.MessageTimeStamp = time.strftime(
            "%d-%m-%Y %H:%M:%S", time.gmtime())
        return message

    def create_location(self, postalcode, deliverydate):
        """Creates a location object with request parameters"""
        location = self.client.factory.create("ns0:Location")
        location.Postalcode = postalcode
        location.DeliveryDate = deliverydate.strftime("%d-%m-%Y")
        location.AllowSundaySorting = self.settings.get(
            'allow_sunday_sorting', True)

        delivery_options = self.client.factory.create("ns3:ArrayOfstring")
        delivery_options.string = self.settings.get('delivery_options', ["PG"])
        location.DeliveryOptions = delivery_options

        options = self.client.factory.create("ns3:ArrayOfstring")
        options.string = self.settings.get('options', ["Daytime"])

        location.Options = options
        return location

    def nearest_locations(self, postalcode, deliverydate=None):
        """Returns the nearest locations based on postal code"""
        if not deliverydate:
            # then we want to see tomorrow
            tomorrow = datetime.now() + timedelta(days=1)

        location = self.create_location(postalcode, tomorrow)
        message = self.create_message()

        status_code, result = self.client.service.GetNearestLocations(
            self.settings.get('countrycode'),
            location,
            message
        )

        if status_code > 400:
            # an error occured
            return status_code, recursive_asdict(result)

        data = recursive_asdict(result)
        # if there are any results, return them
        if "getlocationsresult" in data:
            return status_code, data['getlocationsresult']['responselocation']
        # otherwise, return a empty list
        return status_code, []
