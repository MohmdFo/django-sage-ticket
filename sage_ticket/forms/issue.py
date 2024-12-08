from django import forms
from sage_ticket.models import Issue
from sage_ticket.helper.choice import TicketStateEnum


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'message', 'severity', 'department']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.user:
            instance.raised_by = self.user

        instance.state = TicketStateEnum.NEW
        instance.is_unread = True

        if commit:
            instance.save()

        return instance
