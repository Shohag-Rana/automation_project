from django import forms
from .models import Executor


class ExecutorForm(forms.ModelForm):
    class Meta:
        model = Executor
        fields = '__all__'
    def clean(self):
        data = self.cleaned_data['app_name']
        if data == "hello":
            raise forms.ValidationError("Not a proper titlecased string")



