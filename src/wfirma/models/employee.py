"""
Employee/User models for wFirma API.

This module provides user-related model classes used in wFirma API:
- User - Represents a user account in the wFirma system

In wFirma API, users are accessed through:
- /users/get endpoint - Get user information

Example:
    >>> from wfirma.models.employee import User
    >>> user = User(id=124233, login="jan@kowalski.com")
    >>> user.login
    'jan@kowalski.com'

Note:
    For user-company relationships, see `UserCompany` in the `company` module.
"""

from pydantic_xml import element

from wfirma.models.base import BaseXMLModel, OptionalDateTimeField


class User(BaseXMLModel, tag="user"):
    """
    User model representing a wFirma system user.

    This model matches the `user` structure returned by wFirma API
    from the /users/get endpoint. Users represent individual accounts
    that can access company data through the API.

    Attributes:
        id: User ID.
        login: User login email address.
        created: Account creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> user = User(id=124233, login="jan@kowalski.com")
        >>> user.login
        'jan@kowalski.com'

    Note:
        The created/modified fields may be "0000-00-00 00:00:00" in the API
        response, which is parsed as None.
    """

    id: int = element()
    login: str = element()
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


__all__ = [
    "User",
]
