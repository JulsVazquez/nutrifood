from cProfile import label
from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    weight = forms.IntegerField(label='Peso actual (kg)', min_value = 0)
    height = forms.IntegerField(label = 'Altura (cm)', min_value = 0)
    is_vegan = forms.BooleanField(label = 'Vegan')
    is_keto = forms.BooleanField(label = 'Keto')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.weight = self.cleaned_data['weight']
        user.height = self.cleaned_data['height']
        user.is_vegan = self.cleaned_data['is_vegan']
        user.is_keto = self.cleaned_data['is_keto']
        return user