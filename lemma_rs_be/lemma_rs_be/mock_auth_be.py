"""
Google OpenIdConnect:
    https://python-social-auth.readthedocs.io/en/latest/backends/google.html
"""
from calendar import timegm
from datetime import datetime

from social_core.backends.open_id_connect import OpenIdConnectAuth
from social_core.exceptions import AuthTokenError


class Mock(OpenIdConnectAuth):
    name = 'mock'
    OIDC_ENDPOINT = 'http://localhost:4011'
    ID_TOKEN_ISSUER = 'http://localhost:4011'


    def get_user_details(self, response):
        """Return user details from PixelPin account"""
        return {'email': response.get('email'),
                'fullname': response.get('name'),
                'username': response.get('sub')
                }

    def validate_claims(self, id_token):
        utc_timestamp = timegm(datetime.utcnow().utctimetuple())

        if 'nbf' in id_token and utc_timestamp < id_token['nbf']:
            raise AuthTokenError(self, 'Incorrect id_token: nbf')

        # Verify the token was issued in the last 10 minutes
        iat_leeway = self.setting('ID_TOKEN_MAX_AGE', self.ID_TOKEN_MAX_AGE)
        if utc_timestamp > id_token['iat'] + iat_leeway:
            raise AuthTokenError(self, 'Incorrect id_token: iat')

        # # Validate the nonce to ensure the request was not modified
        # nonce = id_token.get('nonce')
        # if not nonce:
        #     raise AuthTokenError(self, 'Incorrect id_token: nonce')
        #
        # nonce_obj = self.get_nonce(nonce)
        # if nonce_obj:
        #     self.remove_nonce(nonce_obj.id)
        # else:
        #     raise AuthTokenError(self, 'Incorrect id_token: nonce')
