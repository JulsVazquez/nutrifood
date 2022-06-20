from cProfile import label
from allauth.account.forms import SignupForm
from django import forms
from pkg_resources import require


class CustomSignupForm(SignupForm):
    weight = forms.IntegerField(label='Weight (kg)', min_value=0)
    height = forms.IntegerField(label='Height (cm)', min_value=0)
    is_vegan = forms.BooleanField(label='Vegan', required=False)
    is_keto = forms.BooleanField(label='Keto', required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.weight = self.cleaned_data['weight']
        user.height = self.cleaned_data['height']
        user.is_vegan = self.cleaned_data['is_vegan']
        user.is_keto = self.cleaned_data['is_keto']
        user.save()
        print(user)
        return user
