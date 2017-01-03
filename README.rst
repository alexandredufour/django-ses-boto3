================
django-ses-boto3
================
Custom Django email backend for `Amazon Simple Email Service (SES) <https://aws.amazon.com/ses/>`_
using `Boto 3 <https://github.com/boto/boto3>`_ and Python 3.

If you don't need boto3, use `django-ses <https://github.com/django-ses/django-ses>`_ instead.

Installation
------------

``$ pip install django-ses-boto3``


Quick start
-----------

1. Add ``django_ses_boto3`` to ``INSTALLED_APPS`` in ``settings.py``: ::

    INSTALLED_APPS = [
        ...
       'django_ses_boto3',
    ]

2. Update ``EMAIL_BACKEND`` in ``settings.py``::

    EMAIL_BACKEND = 'django_ses_boto3.ses_email_backend.SESEmailBackend'

3. Set ``AWS_SES_REGION_NAME`` in ``settings.py``::

    AWS_SES_REGION_NAME = 'us-west-2' # or your AWS region


Authentication
--------------
This library uses preconfigured AWS credentials. Configuration instructions: https://boto3.readthedocs.io/en/latest/guide/configuration.html#guide-configuration

Passing credentials as `method parameters <https://boto3.readthedocs.io/en/latest/guide/configuration.html#method-parameters>`_ is NOT supported (or recommended).


TODO
----
* Tests
