# coding=utf-8
""""
    Command to fill the map client Credits with the Kartoza default.
.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the Mozilla Public License 2.0.

"""

from django.core.management.base import BaseCommand
from core.models import GeneralSuiteData

DEFAULT_CREDITS = """<div style="text-align: center;">
<p>Hosted by</p>
<p><a href="https://kartoza.com" target="_blank" title="Kartoza"><img src="/static/kartoza/kartoza-logo.png" alt="Kartoza" height="60"></a></p>
<p><a href="https://kartoza.com" target="_blank">GeoSpatialHosting by Kartoza</a></p>
</div>"""

# What core/fixtures/G3WGeneralDataSuite.json puts in, counts as not set.
FIXTURE_CREDITS = '<p>test custom credits<br></p>'


class Command(BaseCommand):
    """
    Fill GeneralSuiteData.credits with DEFAULT_CREDITS when it is empty or
    still the fixture placeholder. Credits edited in the admin are kept.
    """

    help = 'Set the default Kartoza Credits if none have been set.'

    def handle(self, *args, **options):

        general_data = GeneralSuiteData.objects.first()
        if not general_data:
            self.stdout.write('No general suite data, skipping default credits.')
            return

        credits = (general_data.credits or '').strip()
        if credits and credits != FIXTURE_CREDITS:
            self.stdout.write('Credits already set, keeping them.')
            return

        general_data.credits = DEFAULT_CREDITS
        general_data.save()
        self.stdout.write(self.style.SUCCESS('Default credits set.'))
