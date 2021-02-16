"""
Google OpenIdConnect:
    https://python-social-auth.readthedocs.io/en/latest/backends/google.html
"""
from social_core.backends.open_id_connect import OpenIdConnectAuth


class Muni(OpenIdConnectAuth):
    name = 'muni'
    OIDC_ENDPOINT = 'https://localhost:8443/connect/authorize'
    # differs from value in discovery document
    # http://openid.net/specs/openid-connect-core-1_0.html#rfc.section.15.6.2
    ID_TOKEN_ISSUER = 'https://localhost:8443'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        print(access_token)
        result = self.get_json(
            'https://localhost:8443/connect/userinfo',
            headers={
                'Authorization': 'Bearer {0}'.format(access_token)
            },
            verify=False
        )
        print(result)
        return result
