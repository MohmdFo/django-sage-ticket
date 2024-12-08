from django import forms
from sage_ticket.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'message']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.issue = kwargs.pop('issue', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.user:
            instance.user = self.user

        if self.issue:
            instance.issue = self.issue

        instance.is_read = False

        if commit:
            instance.save()

        return instance
