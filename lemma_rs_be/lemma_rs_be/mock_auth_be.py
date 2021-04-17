"""
Google OpenIdConnect:
    https://python-social-auth.readthedocs.io/en/latest/backends/google.html
"""
from social_core.backends.open_id_connect import OpenIdConnectAuth


class Mock(OpenIdConnectAuth):
    name = 'mock'
    OIDC_ENDPOINT = 'http://localhost:4011'
    ID_TOKEN_ISSUER = 'http://localhost:4011'


    def get_user_details(self, response):
        """Return user details from PixelPin account"""
        print(response)
        return {'email': response.get('email'),
                'fullname': response.get('name'),
                'username': response.get('sub')
                }

