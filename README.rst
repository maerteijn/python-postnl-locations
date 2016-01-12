================
PostNL Locations
================
A Python wrapper for using the PostNL locations SOAP API. You can find the source code
here: `python-postnl-locations`_.

.. _`python-postnl-locations`: https://github.com/maerteijn/python-postnl-locations

.. image:: https://travis-ci.org/maerteijn/python-postnl-locations.svg?branch=master
    :target: https://travis-ci.org/maerteijn/python-postnl-locations

.. image:: http://codecov.io/github/maerteijn/python-postnl-locations/coverage.svg?branch=master
    :alt: Coverage
    :target: http://codecov.io/github/maerteijn/python-postnl-locations/


Compatibility
=============

This package is depending on ``suds-jurko`` , a fully compatible version of the original 
package with some bug fixes and speed improvements, and has support for python3 as well. 
So this package depends on it (``suds-py3`` still has some compatibility issues).


Usage
=====

To use this package follow these steps:

1. Install this python package someway. (``pip install postnl-locations``)

2. In your project, create a settings dictionary with at least the following parameters:

.. code-block:: python

  MY_SETTINGS = {
      # this is the testservice wsdl, see the PostNL documentation for the production settings
      'wsdl': "https://testservice.postnl.com/CIF_SB/LocationWebService/2_0/?wsdl",
      'countrycode': 'NL',
      'username': "my-username",
       # the password is SHA1 hashed
      'password': "my-sha1-hashed-password"
  }

3. Use the client as following:

.. code-block:: python

  from postnl.locations.client import Locations
  
  locations = Locations(settings=MY_SETTINGS)
  my_locations = locations.nearest_locations(postalcode="6821AD")


Take a look at the `settings.py`_ for more options.

.. _`settings.py`: https://github.com/maerteijn/python-postnl-locations/blob/master/postnl/locations/settings.py

