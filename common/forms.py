from django import forms


class BaseModelForm(forms.Form):
    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance
