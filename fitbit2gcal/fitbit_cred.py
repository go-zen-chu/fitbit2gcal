#!/usr/bin/env python
from datetime import datetime

class FitbitCred:
    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None, expires_at=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def is_valid():
        """
        check whether access_token is not expired
        """
        if expires_at == None:
            # ignore validity if expires_at is None
            return True
        return datetime.now().timestamp() - self.expires_at > 0
