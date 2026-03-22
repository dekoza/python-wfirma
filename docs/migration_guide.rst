Migration Guide
===============

This guide summarizes the user-visible changes across the beta line and what stays fixed as the project moves toward ``1.0rc1``.

From 1.0b1 to 1.0b2
-------------------

The project hardened its release process and manual verification story.

- the packaged CLI is now part of the supported manual verification workflow
- release steps now live in ``RELEASING.md`` instead of tribal knowledge
- the README now leads with read-only usage before mutating examples

Important changes already made during the beta line
---------------------------------------------------

These changes landed during the beta cycle and are worth calling out for anyone coming from early development snapshots:

- the library now uses a production-only environment model
- ``OAuth1Auth`` is supported as a first-class mode in ``WFirmaClient``
- the packaged CLI provides read-only commands such as ``wfirma company show``

Recommended verification after upgrade
--------------------------------------

Use least-privilege credentials and re-check the safe read-only flows:

.. code-block:: bash

   wfirma company show
   wfirma tags list
   wfirma terms list
   wfirma warehouses list

What freezes for 1.0rc1
-----------------------

The release candidate is expected to freeze these public surfaces:

- import paths under ``wfirma``
- auth constructors and expected arguments
- exception classes and their semantics
- the production-only environment model
- CLI command names and flags
