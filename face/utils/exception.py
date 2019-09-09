from face.utils.constants import required, invalid, expired


class AuthRequired(Exception):
    """Handles required Authorization header"""

    status_code = 403

    def __init__(self):
        Exception.__init__(self)
        self.error = required.format("Authorization")

    def to_dict(self):
        rv = dict()
        rv["error"] = self.error
        return rv


class DecodeError(Exception):
    """Handles invalid Authorization header"""

    status_code = 403

    def __init__(self):
        Exception.__init__(self)
        self.error = invalid.format("Authorization")

    def to_dict(self):
        rv = dict()
        rv["error"] = self.error
        return rv


class ExpiredSignatureError(Exception):
    """Handles expired Authorization header"""

    status_code = 403

    def __init__(self):
        Exception.__init__(self)
        self.error = expired.format("Authorization")

    def to_dict(self):
        rv = dict()
        rv["error"] = self.error
        return rv


class BaseJWTError(Exception):
    """Handles base Authorization header"""

    status_code = 403

    def __init__(self):
        Exception.__init__(self)
        self.error = expired.format("Authorization")

    def to_dict(self):
        rv = dict()
        rv["error"] = self.error
        return rv
