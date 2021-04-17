"""
Google OpenIdConnect:
    https://python-social-auth.readthedocs.io/en/latest/backends/google.html
"""
from social_core.backends.open_id_connect import OpenIdConnectAuth


class Muni(OpenIdConnectAuth):
    name = 'muni'
    OIDC_ENDPOINT = 'https://oidc.muni.cz/oidc'
    ID_TOKEN_ISSUER = 'https://oidc.muni.cz'


