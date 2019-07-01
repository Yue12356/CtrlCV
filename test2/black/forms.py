from django import forms

class PlayerForm(forms.Form):
    name = forms.CharField(max_length = '120')
    date_range = forms.IntegerField(max_value = 30, min_value = 1)