from django.db.models import Q
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from django.http import JsonResponse
from .middleware import *
from .serializer import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from datetime import datetime
from django.core.files.storage import FileSystemStorage


@api_view(['POST'])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form):
    username_or_email = form.cleaned_data['username_or_email']
    password = form.cleaned_data['password']
    user_obj = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
    if user_obj.check_password(password):
        serializer = TokenObtainPairSerializer(data={'username': user_obj.username, 'password': password})
        token = serializer.validate({'username': user_obj.username, 'password': password})['access']
        user_obj.last_login = datetime.now()
        user_obj.save()
        serializer = AuthUserSerializer(instance=user_obj, many=False).data
        serializer["token"] = token
        data = {'data': serializer, "message": "Successfully Login",  "isSuccess": True, "status": 200}
        return Response(data, status=200)
    else:
        return Response({"data": None, "message": "Password Incorrect", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(RegisterMiddleware)
def register_view(request, form):
    serializer = AuthUserSerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        input_data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password']}
        token_serializer = TokenObtainPairSerializer(data=input_data)
        token = token_serializer.validate(input_data)
        update_serializer = AuthUserSerializer(
            instance=User.objects.get(username=form.cleaned_data['username']),
            data={"last_login": datetime.now()},
            partial=True
        )
        if update_serializer.is_valid():
            update_serializer.save()
            data = update_serializer.data
            data['token'] = token['access']
            return Response({"data": data, "isSuccess": True, "status": 200}, status=200)
        else:
            error = serializer.errors
            if "__all__" in error:
                error = error["__all__"][0]
            else:
                error = "".join(key + f" {error[key][0]}\n" for key in error)
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    else:
        error = serializer.errors
        if "__all__" in error:
            error = error["__all__"][0]
        else:
            error = "".join(key + f" {error[key][0]}\n" for key in error)
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(UserProfileMiddleware)
def user_profile_view(request, form):
    error = []
    form.cleaned_data['profile']['photo'] = request.FILES['photo']
    form.cleaned_data['address']['user'] = request.user.id
    form.cleaned_data['document']['user'] = request.user.id
    form.cleaned_data['document']['document1'] = request.FILES['document1']
    form.cleaned_data['document']['document2'] = request.FILES['document2']
    form.cleaned_data['address_proof']['user'] = request.user.id
    form.cleaned_data['address_proof']['address_proof1'] = request.FILES['address_proof1']
    form.cleaned_data['address_proof']['address_proof2'] = request.FILES['address_proof2']
    profile = AuthUserSerializer(data=form.cleaned_data['profile'], instance=request.user)
    if profile.is_valid():
        profile.save()
    else:
        err = profile.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    address = UserAddressSerializer(data=form.cleaned_data['address'])
    if address.is_valid():
        address.save()
    else:
        err = address.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    document = UserDocumentSerializer(data=form.cleaned_data['document'])
    if document.is_valid():
        document.save()
    else:
        err = address.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    address_proof = UserAddressProofSerializer(data=form.cleaned_data['address_proof'])
    if address_proof.is_valid():
        address_proof.save()
    else:
        err = address.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    if any(error):
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    else:
        return Response({"data": None, "message": "User Profile Updated Successfully",
                         "isSuccess": False, "status": 200}, status=200)
