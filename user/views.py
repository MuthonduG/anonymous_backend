from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.shortcuts import get_object_or_404

# Get all users
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Get single user
@api_view(['GET'])
def getUser(request, pk):
    user = get_object_or_404(User, id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# Register new user
@api_view(['POST'])
def registerUser(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# Update user data
@api_view(['PUT'])
def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# Delete user
@api_view(['DELETE'])
def deleteUser(request, pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    return Response(
        {"message": "User account successfully deleted!"},
        status=status.HTTP_204_NO_CONTENT
    )
