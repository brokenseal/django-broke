from django.db.models import manager

class BrokeManager(manager.Manager):
    def filter_based_on_request(self, request):
        raise NotImplementedError("You must implement this method on sub classes.")