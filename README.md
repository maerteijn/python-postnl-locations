================
PostNL Locations
================
A Python wrapper for using the PostNL locations SOAP API.


Usage
=====

To use this package follow these steps:

1. Install the `postnl-locations` python egg someway. (`pip install postnl-locations`)
3. In your project, patch the settings from the package with your settings 
(username and password are needed to communicate):

```python
MY_SETTINGS = {
    # this is the testservice wsdl, see the PostNL documentation for the production settings
    'wsdl': "https://testservice.postnl.com/CIF_SB/LocationWebService/2_0/?wsdl",
    'countrycode': 'NL',
    'username': "my-username",
     # the password is SHA1 hashed
    'password': "my-sha1-hashed-password"
}

import postnl.locations.settings
postnl.locations.settings.POSTNL_SETTINGS = MY_SETTINGS
```

3. Use the client as following

```python
from postnl.locations.client import Locations

locations = Locations()
my_locations = locations.nearest_locations(postcode="6821AD")
```