Python client for `Helix Swarm <https://www.perforce.com/manuals/swarm/>`_
==========================================================================

Status
------

|Build status|
|Docs status|
|Coverage status|
|Version status|
|Downloads status|

.. |Build status|
   image:: https://github.com/pbelskiy/helix-swarm/workflows/Tests/badge.svg
.. |Docs status|
   image:: https://readthedocs.org/projects/helix-swarm/badge/?version=latest
.. |Coverage status|
   image:: https://img.shields.io/coveralls/github/pbelskiy/helix-swarm?label=Coverage
.. |Version status|
   image:: https://img.shields.io/pypi/pyversions/helix-swarm?label=Python
.. |Downloads status|
   image:: https://img.shields.io/pypi/dm/helix-swarm?color=1&label=Downloads

Documentation
-------------

`Read the Docs <https://helix-swarm.readthedocs.io/en/latest/>`_

Installation
------------

::

    pip3 install -U helix-swarm

Examples
--------

Get review info:

.. code:: python

    from helixswarm import SwarmClient

    client = SwarmClient('http://server/api/v9', 'login', 'password')
    review = client.reviews.get_info(12345)
    print(review['review']['author'])

Add comment to review (async):

.. code:: python

    import asyncio
    from helixswarm import SwarmAsyncClient

    client = SwarmAsyncClient('http://server/api/v5', 'login', 'password')

    async def example():
        await client.comments.add('reviews/12345', 'my awesome comment')

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(example())
    finally:
        loop.run_until_complete(client.close())
        loop.close()

Testing
-------

Prerequisites: `tox`

Then just run tox, all dependencies and checks will run automatically

::

    tox

Contributing
------------

Feel free to any contributions

`Official REST API documentation <https://www.perforce.com/manuals/swarm/Content/Swarm/swarm-apidoc.html>`_
-----------------------------------------------------------------------------------------------------------

+------------+----------------+-----------------------------------------------------------------------------+
| API        | Date           | Notes                                                                       |
+============+================+=============================================================================+
| `v10`_     | October 2019   | Integration with CI tools                                                   |
+------------+----------------+-----------------------------------------------------------------------------+
| `v9`_      | April 2018     | Review append and replace changelist, 2fa, mark comment as read             |
+------------+----------------+-----------------------------------------------------------------------------+
| `v8`_      | December 2017  | Default reviewers                                                           |
+------------+----------------+-----------------------------------------------------------------------------+
| `v7`_      | October 2017   | Groups as review participants, groups as moderators of project              |
+------------+----------------+-----------------------------------------------------------------------------+
| `v6`_      | May 2017       | Activity dashboard, archiving reviews, cleaning reviews, for voting reviews |
+------------+----------------+-----------------------------------------------------------------------------+
| v5         | October 2016   | Limiting comments to a specific review version                              |
+------------+----------------+-----------------------------------------------------------------------------+
| `v4`_      | October 2016   | Private projects, file-level and line-level inline comments                 |
+------------+----------------+-----------------------------------------------------------------------------+
| v3         | September 2016 | Comments management                                                         |
+------------+----------------+-----------------------------------------------------------------------------+
| `v2`_      | May 2016       | Projects, groups                                                            |
+------------+----------------+-----------------------------------------------------------------------------+
| `v1.2`_    | October 2015   | Author filter to the list reviews endpoint                                  |
+------------+----------------+-----------------------------------------------------------------------------+
| `v1.1`_    | January 201    | Required reviewers                                                          |
+------------+----------------+-----------------------------------------------------------------------------+
| `v1`_      | July 2014      | Initial                                                                     |
+------------+----------------+-----------------------------------------------------------------------------+

.. _v10: https://www.perforce.com/manuals/swarm/Content/Swarm/swarm-apidoc_endpoints-v10.html
.. _v9: https://www.perforce.com/manuals/v19.1/swarm/Content/Swarm/swarm-apidoc.html
.. _v8: https://www.perforce.com/manuals/v17.4/swarm/#Swarm/swarm-apidoc.html
.. _v7: https://www.perforce.com/manuals/v17.3/swarm/index.html#Swarm/swarm-apidoc.html
.. _v6: https://www.perforce.com/manuals/v17.2/swarm/api.html
.. _v4: https://www.perforce.com/perforce/r16.2/manuals/swarm/api.html
.. _v2: https://www.perforce.com/perforce/r16.1/manuals/swarm/api.html
.. _v1.2: https://www.perforce.com/perforce/r15.3/manuals/swarm/api.html
.. _v1.1: https://www.perforce.com/perforce/r14.4/manuals/swarm/api.html
.. _v1: https://www.perforce.com/perforce/r14.3/manuals/swarm/api.html
