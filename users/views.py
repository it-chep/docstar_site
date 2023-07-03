from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import *

from .models import *


def init_email(request):
    pass


# class SignUpView(DataMixin, CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('success')
#     template_name = 'users/signup.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Регистрация")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_params(self, request):
#         email = self.request.GET.get('email')
#         return email
#
#     def post(self, request, *args, **kwargs):
#
#         form = CustomUserCreationForm(request.POST)
#         # form.fields["email"].initial = SignUpView.get_params(self, request)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#
#             logout(request)
#
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#
#             return redirect('success')
#         else:
#             return render(request, self.template_name, {'form': form})


class SignUp(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    template_name = 'users/signup.html'

    @staticmethod
    def get(request):
        if not request.user.is_anonymous:
            return redirect('logout')
        return render(request, SignUp.template_name)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            login(request, user)
            return Response({'status': 200}, status=status.HTTP_200_OK)

        else:
            print('goodbye')
            errors = serializer.errors
            if 'email' in errors:
                email_errors = errors['email']

                if 'not_unique' in email_errors:
                    return redirect('login')

                elif 'invalid' in email_errors:
                    # return redirect('phone_not_found')
                    return Response({'status': 'error', },
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'fatal_error', },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    template_name = 'users/login.html'

    def get(self, request):
        if not request.user.is_anonymous:
            return redirect('logout')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data['user']
            login(request, user)
            return redirect('homepage')
        else:
            errors = serializer.errors
            if 'user' in errors:
                user_errors = errors['user']

                if 'non_phone' in user_errors:
                    return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                if 'invalid_data' in user_errors:
                    return Response({'status': 'invalid_data'}, status=status.HTTP_400_BAD_REQUEST)
            if 'phone_number' in errors:
                return Response({'status': 'not_phone'}, status=status.HTTP_400_BAD_REQUEST)

            return redirect('signup')


class LogoutView(APIView):
    # Работает без JS
    permission_classes = (IsAuthenticated,)
    template_name = 'users/logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect('homepage')


class Forgot_pass(APIView):

    def get(self, request):
        pass


def success_signup(request):
    return render(request, 'users/success.html')

class VerificationEmail(APIView):

    def get(self):
        pass

    def post(self):
        pass


class GetToken(APIView):

    def get(self, request):
        token = request.GET.get('token')

        user = CustomUser.objects.filter(email_verification_token=token).get()

        if user:
            user.verified_email = True
            user.save()
            return redirect('homepage')
        else:
            return redirect('invalid_token')


class ForgotPassword(APIView):
    template_name = 'users/forgot_password.html'
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def get(self, request):
        if not request.user.is_anonymous:
            return redirect('logout')
        return render(request, self.template_name)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response({'status': 200}, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            if 'email' in errors:
                user_errors = errors['email']
                if 'not_exist' in user_errors:
                    return Response({'status': 'error', 'message': 'Плохой email'},
                                    status=status.HTTP_400_BAD_REQUEST)

            return redirect('signup')


class ValidateToken(APIView):
    template_name = 'users/validate_token.html'

    def get(self, request, ):
        token = request.GET.get('token')

        user = CustomUser.objects.filter(email_verification_token=token).first()

        if user:
            return redirect(reverse_lazy('change_password') + f'?token={token}')
        else:
            return redirect('invalid_token')


class ChangePassword(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer
    template_name = 'users/change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        if serializer.is_valid():
            user = CustomUser.objects.filter(email_verification_token=request.GET.get('token')).get()
            print(user, user.password, )
            login(request, user)
            return redirect('homepage')

        else:
            print('post error')
            errors = serializer.errors
            return redirect('homepage')


class InvalidToken(APIView):
    template_name = 'users/invalid_token.html'

    def get(self, request):
        return render(request, self.template_name)
