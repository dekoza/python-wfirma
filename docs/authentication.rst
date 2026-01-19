Authentication
==============

wFirma API uses OAuth for authentication. This guide will help you set up authentication.

Getting API Credentials
------------------------

1. Log in to your wFirma account
2. Navigate to **Settings** → **API**
3. Generate a new application key and secret
4. Save these credentials securely

Configuration Methods
---------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The recommended method for production::

    export WFIRMA_APP_KEY=your_app_key
    export WFIRMA_SECRET=your_secret
    export WFIRMA_ENVIRONMENT=sandbox  # or production

Or create a ``.env`` file::

    WFIRMA_APP_KEY=your_app_key
    WFIRMA_SECRET=your_secret
    WFIRMA_ENVIRONMENT=sandbox

Direct Configuration
~~~~~~~~~~~~~~~~~~~~

Pass credentials directly when creating the client::

    from wfirma import WFirmaClient

    client = WFirmaClient(
        app_key="your_app_key",
        secret="your_secret",
        environment="sandbox"
    )

Environments
------------

Sandbox Environment
~~~~~~~~~~~~~~~~~~~

Use sandbox for testing::

    client = WFirmaClient(
        app_key="your_sandbox_key",
        secret="your_sandbox_secret",
        environment="sandbox"
    )

Production Environment
~~~~~~~~~~~~~~~~~~~~~~

Use production for live data::

    client = WFirmaClient(
        app_key="your_production_key",
        secret="your_production_secret",
        environment="production"
    )

.. warning::
   Always test your integration in the sandbox environment before using production credentials.

Token Management
----------------

The library handles token management automatically:

* Tokens are obtained on first API call
* Tokens are cached during the session
* Expired tokens are automatically renewed
* No manual token handling required

OAuth Token Store
-----------------

You can persist OAuth tokens using the built-in token stores:

* ``MemoryTokenStore`` – in-process, non-persistent (default for tests/quick scripts)
* ``FileTokenStore`` – JSON file-based store for persistence between runs

Example (file-based store)::


    from wfirma.auth.common import FileTokenStore

    store = FileTokenStore("~/.cache/wfirma/tokens.json")
    store.set("default", token)
    restored = store.get("default")


Tokens are stored as JSON objects keyed by a string you choose (e.g., ``default`` or per-company). Invalid JSON or non-mapping payloads raise ``ValidationError``; write failures raise ``ConfigurationError``. Keys must be strings.

All token store classes are shared between sync and async authentication modules.

.. note::
   When running tests locally, use pytest's built-in cache clearing flag
   (``--cache-clear``) at the start of the run.

OAuth 1.0a request signing helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to sign raw HTTP requests (for example, when building your own client),
you can build the OAuth1 ``Authorization`` header using ``wfirma.auth.common``::

    from wfirma.auth.common import OAuthToken, build_oauth1_authorization_header

    token = OAuthToken(access_token="oauth-token", refresh_token="oauth-token-secret")

    auth_header_value = build_oauth1_authorization_header(
        consumer_key="your_consumer_key",
        consumer_secret="your_consumer_secret",
        token=token,
        nonce="nonce",
        realm=None,
    )

    headers = {"Authorization": auth_header_value}

The helper uses the ``PLAINTEXT`` signature method and produces a header value starting
with ``OAuth ``. ``realm`` is optional. If you do not pass ``timestamp``, the current Unix
timestamp is used.

Multi-Company Support
---------------------

If you have access to multiple companies::

    client = WFirmaClient(
        app_key="your_app_key",
        secret="your_secret",
        company_id="specific_company_id"
    )

Security Best Practices
-----------------------

1. **Never commit credentials** to version control
2. **Use environment variables** in production
3. **Rotate credentials** regularly
4. **Use sandbox** for development and testing
5. **Limit API key permissions** to minimum required

Next Steps
----------

* :doc:`quickstart` - Make your first API call
* :doc:`guides/error_handling` - Handle authentication errors

OAuth Flows
-----------

OAuth 2.0 (Authorization Code)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use when you can open the user consent page. Minimal sync example::

    from wfirma.sync.auth import OAuth2Auth
    from wfirma.auth.common import FileTokenStore
    from wfirma.config import Environment

    auth = OAuth2Auth(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="https://your.app/callback",
        environment=Environment.PRODUCTION,
        token_store=FileTokenStore("~/.cache/wfirma/tokens.json"),
    )

    # Step 1: redirect user to wFirma consent page
    consent_url = auth.build_authorization_url(scope="invoices-read", state="csrf-state")

    # Step 2: exchange authorization code received on redirect
    token = auth.exchange_code("authorization-code-from-callback")

    # Step 3: reuse token for API calls (auto-refresh when expired)
    token = auth.get_token()

Async variants are available via ``wfirma.async_.auth.OAuth2Auth`` and ``wfirma.async_.auth.OAuth1Auth`` with identical APIs using ``httpx.AsyncClient`` under the hood.

OAuth 1.0a
~~~~~~~~~~

Use when the integration cannot open an OAuth2 consent page. Minimal sync example::

    from wfirma.sync.auth import OAuth1Auth
    from wfirma.auth.common import MemoryTokenStore

    auth = OAuth1Auth(
        consumer_key="your_consumer_key",
        consumer_secret="your_consumer_secret",
        scope="invoices-read",
        callback_url="https://your.app/callback",
        token_store=MemoryTokenStore(),
    )

    request_token = auth.fetch_request_token()
    authorization_url = auth.build_authorization_url(request_token)
    # Redirect the user to authorization_url, receive oauth_verifier
    access_token = auth.fetch_access_token(
        oauth_token=request_token.access_token,
        oauth_token_secret=request_token.refresh_token or "",
        oauth_verifier="oauth-verifier-from-callback",
    )

Async variants are available via ``wfirma.async_.auth.OAuth2Auth`` and ``wfirma.async_.auth.OAuth1Auth`` with identical APIs using ``httpx.AsyncClient`` under the hood.

OAuth 1.0a signature details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wFirma OAuth 1.0a implementation uses the ``PLAINTEXT`` signature method (per API documentation).
This library exposes two low-level helpers in ``wfirma.auth.common``:

* ``oauth_percent_encode(value: str) -> str`` - RFC3986 percent-encoding used by OAuth (spaces are encoded as ``%20``, not ``+``)
* ``sign_oauth1_plaintext(consumer_secret: str, token_secret: str | None) -> str`` - builds the ``PLAINTEXT`` signature value

These helpers are used internally, but they are also available if you need to debug request signing.

OAuth 1.0a
----------

OAuth 1.0a in wFirma uses the ``PLAINTEXT`` signature method.

The library provides ``OAuth1Auth`` helpers in both sync and async modules.

Generating request headers
~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have an access token stored in the token store, you can generate the
``Authorization`` header for authenticated requests:

.. code-block:: python

   from wfirma.sync.auth import OAuth1Auth, OAuthToken

   auth = OAuth1Auth(
       consumer_key="...",
       consumer_secret="...",
       scope="invoices-read",
       callback_url=None,
   )

   # The OAuth 1.0a token secret is stored in token.refresh_token.
   auth.token_store.set(
       "default",
       OAuthToken(access_token="oauth_token", refresh_token="oauth_token_secret"),
   )

   headers = auth.get_headers()
   # {'Authorization': 'OAuth oauth_consumer_key="...", ...'}

The async variant works the same way:

.. code-block:: python

   from wfirma.async_.auth import OAuth1Auth, OAuthToken

   auth = OAuth1Auth(
       consumer_key="...",
       consumer_secret="...",
       scope="invoices-read",
       callback_url=None,
   )

   auth.token_store.set(
       "default",
       OAuthToken(access_token="oauth_token", refresh_token="oauth_token_secret"),
   )

   headers = auth.get_headers()

For deterministic tests you can provide ``nonce`` and ``timestamp`` overrides.
