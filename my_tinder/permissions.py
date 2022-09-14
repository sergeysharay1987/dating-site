from rest_framework.permissions import BasePermission
from PIL import Image

class IsUserPkInUrl(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id and view.action == 'update':
            # print(f'request.data: {dir(request.data["avatar"])}')
            # print(f'request.data["avatar"].file: {request.data["avatar"].file}')
            # byte_io = request.data["avatar"].file
            # im = Image.open(byte_io)
            #im.show()
            #print(f'image: {im}')
            return True
        return False