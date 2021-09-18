from django import forms
from .models import User
from django.core.validators import RegexValidator
from django.db.models import Q
import random


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username_or_email', 'password']

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        u_e = cleaned_data['username_or_email']
        if not User.objects.filter(Q(email=u_e) | Q(username=u_e)).exists():
            raise forms.ValidationError("User is not Exists!!!")
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    parent = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'parent')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if "email" in cleaned_data:
            if User.objects.filter(email=cleaned_data['email']).exists():
                raise forms.ValidationError("Email Already Exists !!!")
        if "username" in cleaned_data:
            if User.objects.filter(username=cleaned_data['username']).exists():
                raise forms.ValidationError("username Already Exists !!!")
        if 'parent' in cleaned_data and cleaned_data['parent']:
            if not User.objects.filter(user_id=cleaned_data['parent']).exists():
                raise forms.ValidationError("Parent Code not Exists !!!")
            else:
                cleaned_data['parent'] = User.objects.get(user_id=cleaned_data['parent']).id

        return cleaned_data


class UserProfileForm(forms.Form):
    name = forms.CharField(required=True)
    country = forms.CharField(required=True)
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)
    pincode = forms.IntegerField(required=True)
    document_type = forms.CharField(required=True)
    document1 = forms.ImageField(required=True)
    document2 = forms.ImageField(required=True)
    address_proof_type = forms.CharField(required=True)
    address_proof1 = forms.ImageField(required=True)
    address_proof2 = forms.ImageField(required=True)
    photo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ('name', 'country', 'city', 'address', 'pincode', 'document_type', 'document1', 'document2',
                  'address_proof_type', 'address_proof1', 'address_proof2', 'photo')

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        cleaned_data['profile'] = {
            'name': cleaned_data['name'],
        }
        cleaned_data['address'] = {
            'country': cleaned_data['country'],
            'city': cleaned_data['city'],
            'address': cleaned_data['address'],
            'pincode': cleaned_data['pincode'],
        }
        cleaned_data['document'] = {
            'document_type': cleaned_data['document_type'],
        }
        cleaned_data['address_proof'] = {
            'document_type': cleaned_data['address_proof_type'],
        }
        cleaned_data.pop("name")
        cleaned_data.pop("country")
        cleaned_data.pop("city")
        cleaned_data.pop("address")
        cleaned_data.pop("pincode")
        cleaned_data.pop("document_type")
        cleaned_data.pop("address_proof_type")
        return cleaned_data
