import jwt
from datetime import datetime, timedelta, timezone
import random
# Secret key for signing and verifying tokens
SECRET_KEY = "$ 9@^!Q#7Xp&v$%*+0q1z2m3n4L5K6J7H8G9F0E1D2C3B4A5a6b7c8d9e0f1g2h3i4j5k6l7M8N9O0P!@#$%^&*()"

# Function to create a JWT token


def create_token(user_id):
    try:
        # Set the expiration time for the token
        expiration = datetime.now(timezone.utc) + timedelta(days=365)

        # Create the payload containing the user ID and expiration time
        payload = {
            'user_id': user_id,
            'exp': expiration
        }

        # Generate the token using the payload and secret key
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return token

    except Exception as e:
        # Handle any exceptions that occur during token creation
        print(f"Error creating token: {e}")

# Function to verify a JWT token


def verify_token(token):
    try:
        # Verify and decode the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        expiration = payload['exp']

        # Check if the token has expired
        if datetime.now(timezone.utc) > datetime.fromtimestamp(expiration, timezone.utc):
            # Refresh the token
            refreshed_token = refresh_token(token)
            if refreshed_token:
                # Return the refreshed token
                return refreshed_token

            raise jwt.ExpiredSignatureError(
                "Token has expired and could not be refreshed")

        return user_id

    except jwt.ExpiredSignatureError:
        # Handle the case where the token has expired
        print("Token has expired")
    except jwt.InvalidTokenError:
        # Handle the case where the token is invalid
        print("Invalid token")
    except Exception as e:
        # Handle any other exceptions that occur during token verification
        print(f"Error verifying token: {e}")

# Function to refresh a JWT token


def refresh_token(token):
    try:
        # Verify and decode the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']

        # Create a new expiration time for the token
        expiration = datetime.now(timezone.utc) + timedelta(days=365)

        # Update the payload with the new expiration time
        payload['exp'] = expiration

        # Generate the refreshed token using the updated payload and secret key
        refreshed_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return refreshed_token

    except jwt.InvalidTokenError:
        # Handle the case where the token is invalid
        print("Invalid token")
    except Exception as e:
        # Handle any other exceptions that occur during token refreshing
        print(f"Error refreshing token: {e}")

print(str(random.randint(0, 99994)).zfill(4)+str(random.randint(0, 99994)).zfill(4))