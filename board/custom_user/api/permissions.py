from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    См.название класса
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.id == request.user.id or request.user.is_staff)
        )


class IsAuthenticateAndIsOwner(BasePermission):
    """
    GET запросы запрещены
    POST запросы принимаются только от пользователей,
    при условии, что они игнорируют пользователей для себя.
    Принимает по одному объекту!

    PUT,PATCH только для владельцев
    """

    def has_permission(self, request,view) -> bool:
        return True if request.data.get('user', None) == request.user.id else False

    def has_object_permission(self, request, view, obj) -> bool:
        return True if request.user.is_authenticated and obj.user == request.user else False
