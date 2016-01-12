POSTNL_SETTINGS = {
    'wsdl': "https://testservice.postnl.com/CIF_SB/LocationWebService/2_0/?wsdl",  # noqa
    'countrycode': 'NL',
    'username': "",
    # this should be a SHA1 hash
    'password': "",
    # see the PostNL CIF - Location WebService, version 2_0 for documentation
    # on the following settings
    'delivery_options': ["PG"],
    'options': [
        "Daytime", "Evening", "Morning", "Noon", "Sunday", "Afternoon"],
    'allow_sunday_sorting': True
}
