from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.task.permissions import IsProjectOwner
from apps.accounts.models import Role


from .serializers import RegisterSerializer, UserSerializer, AssignRoleSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "Logged out"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserMeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class AssignRoleAPIView(APIView):
    permission_classes = [IsProjectOwner]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": _("User not found")}, status=404)
        
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.validated_data["role"]
        
        if role not in Role.values:
            return Response({"error": _("Invalid role")}, status=400)

        user.role = role
        user.save()

        return Response({"success": _(f"{user.username} assigned as {user.get_role_display()}")})