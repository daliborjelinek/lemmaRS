"""
Google OpenIdConnect:
    https://python-social-auth.readthedocs.io/en/latest/backends/google.html
"""
from social_core.backends.open_id_connect import OpenIdConnectAuth


class Muni(OpenIdConnectAuth):
    name = 'muni'
    OIDC_ENDPOINT = 'https://oidc.muni.cz/oidc/authorize'
    # differs from value in discovery document
    # http://openid.net/specs/openid-connect-core-1_0.html#rfc.section.15.6.2
    ID_TOKEN_ISSUER = 'https://oidc.muni.cz'
    USER_FIELDS = ['username', 'email', 'fullname']

    # def get_user_details(self, response):
    #     """Return user details from PixelPin account"""
    #     print(response)
    #     return {'email': 'bla@bla.cz',
    #             'username': 'jarda',
    #             'fullname': 'fulnamejarda'
    #             }

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        print(access_token)
        result = self.get_json(
            'https://oidc.muni.cz/oidc/userinfo',
            headers={
                'Authorization': 'Bearer {0}'.format(access_token)
            },
        )
        print(result)
        return result
