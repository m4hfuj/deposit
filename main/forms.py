from django.shortcuts import get_object_or_404
from django import forms
from .models import Visitation, Client, Box


class AddVisitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # get the client object through pk
        client_pk = kwargs.get('initial', {}).get('client_pk')
        if client_pk:
            self.fields['client'].initial = get_object_or_404(Client, pk=client_pk)
            self.client = Client.objects.get(pk = client_pk)

    class Meta:
        model = Visitation
        fields = ['client', 'box', 'visit_date', 'check_in', 'check_out']

        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'box': forms.Select(attrs={'class': 'form-select'}),
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'check_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['client'].queryset = Client.objects.filter(client = self.client)
            self.fields['box'].queryset = Box.objects.filter(transaction__client = self.client)

