from rest_framework.response import Response
from rest_framework import status

class UserGroupHelper:

  def verifyEqualsIdentifications(loggedId, requestId):
    if loggedId is not requestId:
      return Response({
        'message': "Can't assign to that user, with this level of authentication"
      }, status=status.HTTP_400_BAD_REQUEST)