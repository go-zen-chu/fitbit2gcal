#!/usr/bin/env python
from datetime import datetime

class FitbitCred:;
    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None, expired_at=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expired_at = expired_at

    def is_valid():
        """
        check whether access_token is not expired
        """
        return datetime.now() - self.expired_at > 0
