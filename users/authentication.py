"""Authentication backends"""
from rest_framework import authentication


class GXTokenAuthentication(authentication.TokenAuthentication):
    """
    API Authentication based on Token.

    All signed requests should have HTTP header like:
    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    """
    pass
