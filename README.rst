Python client for `Helix Swarm <https://www.perforce.com/manuals/swarm/>`_
==========================================================================

|Build status|
|Docs status|
|Coverage status|
|Version status|
|Downloads status 1|
|Downloads status 2|

.. |Build status|
   image:: https://github.com/pbelskiy/helix-swarm/workflows/Tests/badge.svg
.. |Docs status|
   image:: https://readthedocs.org/projects/helix-swarm/badge/?version=latest
.. |Coverage status|
   image:: https://img.shields.io/coveralls/github/pbelskiy/helix-swarm?label=Coverage
.. |Version status|
   image:: https://img.shields.io/pypi/pyversions/helix-swarm?label=Python
.. |Downloads status 1|
    image:: https://img.shields.io/pypi/dm/helix-swarm?color=1&label=Downloads
.. |Downloads status 2|
    image:: https://img.shields.io/pypi/dm/helixswarm?color=1&label=Downloads

----

Package supports sync and async syntax with same code base.

.. code:: python

    from helixswarm import SwarmAsyncClient, SwarmClient

Documentation
-------------

`Read the Docs <https://helix-swarm.readthedocs.io/en/latest/>`_

`Official REST API PDF <https://github.com/pbelskiy/helix-swarm/blob/master/docs/swarm.pdf>`_

Installation
------------

There are two identical packages: ``helix-swarm`` and alias ``helixswarm``, alias
was created one year later due name confusion, to be import name and package name will the same.

::

    pip3 install helixswarm

Examples
--------

Get review info:

.. code:: python

    from helixswarm import SwarmClient

    client = SwarmClient('http://server/api/v9', 'user', 'password')
    review = client.reviews.get_info(12345)
    print(review['review']['author'])

Add comment to review in async way (be careful ``SwarmAsyncClient`` must be called inside async function):

.. code:: python

    import asyncio
    from helixswarm import SwarmAsyncClient

    async def example():
        client = SwarmAsyncClient('http://server/api/v5', 'user', 'password')
        await client.comments.add('reviews/12345', 'my awesome comment')

    asyncio.run(example())


Update credentials handler:

.. code:: python

    import requests
    from helixswarm import SwarmClient

    def get_credentials():
        response = requests.get(...).json()
        return response['user'], response['password']

    client = SwarmClient(
        'http://server/api/v9',
        'user',
        'password',
        auth_update_callback=get_credentials
    )

    # let's suppose credentials are valid now
    review = client.reviews.get_info(12345)
    print(review['review']['author'])

    # now, after some time, password of user somehow changed, so our callback
    # will be called, new credentials will be using for retry and future
    # here we get also correct review data instead of SwarmUnauthorizedError
    # exception
    review = client.reviews.get_info(12345)
    print(review['review']['author'])

Testing
-------

Prerequisites: `tox`

Then just run tox, all dependencies and checks will run automatically

::

    tox

Contributing
------------

Feel free to any contributions.

Mirror repositories of review board source code:
  - `2022.1 <https://github.com/dfrees/swarm>`_
  - `2016.1 <https://github.com/stewartlord/swarm>`_

Latest version of code can be download from official page:
https://www.perforce.com/downloads/helix-swarm

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
