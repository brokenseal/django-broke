import os, sys
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from south.migration import Migrations
from south.creator import freezer

from broke.registration import registered_models

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--tenant', action='store', dest='tenant', default=None,
            help='Which tenant should we get the views from.'),
    )

    help="Create a js file with all the registered models."
    args="[apps] --tenant=[tenant]"

    def handle(self, *args, **options):

        if not args:
            apps= registered_models
        else:
            apps = [ app for app in registered_models if app in args ]
        