from django.db.models import QuerySet


class TicketQueryAccess(QuerySet):
    def get_actives(self):
        return self.filter(is_read=True)

    def get_archive(self):
        return self.filter(is_read=True)
