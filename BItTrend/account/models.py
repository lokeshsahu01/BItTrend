from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


class User(AbstractUser):
    def document_path(self):
        return f"/document/{self.id}/"

    id = models.CharField(max_length=255, primary_key=True, default=get_random_string, editable=False)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=13, null=True, blank=True, unique=True)
    name = models.EmailField(max_length=255, null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    token = models.TextField(max_length=20000, null=True, blank=True)
    photo = models.FileField(upload_to=document_path, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "User"


class UserAddress(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_address")
    country = models.CharField(max_length=250)
    state = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250)
    address = models.TextField(max_length=65500)
    pincode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserDocument(models.Model):
    def document_path(self):
        return f"/document/{self.user.id}/"

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_document")
    document_type = models.CharField(max_length=250)
    document1 = models.FileField(upload_to=document_path)
    document2 = models.FileField(upload_to=document_path)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="user_document_approved_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserAddressProof(models.Model):
    def document_path(self):
        return f"/document/{self.user.id}/"

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_address_proof")
    document_type = models.CharField(max_length=250)
    address_proof1 = models.FileField(upload_to=document_path)
    address_proof2 = models.FileField(upload_to=document_path)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="user_address_proof_approved_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
