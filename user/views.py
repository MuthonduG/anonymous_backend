from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, OtpToken
from .serializer import UserSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from .signals import create_token
import logging


logger = logging.getLogger(__name__)

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

# sign up new user
@api_view(['POST'])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.error(f"Registration errors: {serializer.errors}")
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

# activate account using OTP
@api_view(['POST'])
def verifyEmail(request):
    # Extract email and OTP from request data
    email = request.data.get("email")
    otp_code = request.data.get("otp_code")
    
    if not email or not otp_code:
        return Response(
            {"message": "Email and OTP code are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Fetch the user by email
    user = get_object_or_404(User, email=email)

    # Fetch the most recent OTP for the user
    user_otp = OtpToken.objects.filter(user=user).last()

    if not user_otp:
        return Response(
            {"message": "No OTP found for this user."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if OTP has expired
    if timezone.now() > user_otp.otp_expires_at:
        return Response(
            {"message": "The OTP has expired. Please request a new one."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate the provided OTP code (case insensitive)
    if user_otp.otp_code.lower() != otp_code.lower():
        return Response(
            {"message": "Invalid OTP. Please try again."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Activate the user's account
    user.is_active = True
    user.save()
    logger.info(f"User {user.email} activated their account using OTP.")

    # Send confirmation email
    try:
        send_mail(
            subject="Account Activated",
            message="Your account has been successfully activated!",
            from_email="muthondugithinji@gmail.com",  
            recipient_list=[user.email],
            fail_silently=False, 
        )
    except Exception as e:
        logger.error(f"Failed to send activation email to {user.email}: {e}")

    # Invalidate the OTP
    user_otp.delete()

    return Response(
        {"message": "Account has been activated successfully!"},
        status=status.HTTP_200_OK,
    )


# resend otp 
@api_view(['POST']) 
def resendOtp(request, email): 
    # Fetch the user by email 
    user = get_object_or_404(User, email=email) 

    # Invalidate any existing OTPs that are not expired 
    OtpToken.objects.filter(user=user, otp_expires_at=timezone.now()).delete()

    # Generate and send new OTP 
    try: 
        create_token(user) 
        logger.info(f"Generated and sent new OTP for user {user.email}") 
    except Exception as e: 
        logger.error(f"Failed to generate/send OTP for {user.email}: {e}") 
        return Response( 
            {"message": "Failed to send OTP. Please try again later."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, ) 
    
    return Response( {"message": "A new OTP has been sent to your email address."}, status=status.HTTP_200_OK, )