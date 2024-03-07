from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializer import TaskSerializer
from .models import *

from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        _, token = AuthToken.objects.create(user)
        
        token_instance = AuthToken.objects.get(token_key=token[:8])

        data = {
            'token': token,
            'expiry': token_instance.expiry,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return Response(data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    serializer_class = TaskSerializer


    def create(self, request, *args, **kwargs):
        if 'prueba' in request.data.get('title').lower():
            return Response({'error': 'No se puede crear una tarea con la palabra prueba en el titulo'}, status=400)
        if 'prueba' in request.data.get('description').lower():
            return Response({'error': 'No se puede crear una tarea con la palabra prueba en la descripcion'}, status=400)

        return super(TaskViewSet, self).create(request, *args, **kwargs)
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'prueba' in instance.title.lower():
            return Response({'error': 'No se puede mostrar una tarea con la palabra prueba en el titulo'}, status=400)
        if 'prueba' in instance.description.lower():
            return Response({'error': 'No se puede mostrar una tarea con la palabra prueba en la descripcion'}, status=400)

        return super(TaskViewSet, self).retrieve(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'title' in request.data:
            if 'prueba' in request.data.get('title').lower():
                return Response({'error': 'No se puede actualizar una tarea con prueba en el titulo'}, status=400)
        if 'description' in request.data:
            if 'prueba' in request.data.get('description').lower():
                return Response({'error': 'No se puede actualizar una tarea con prueba en la descripcion'}, status=400)
        if instance.completed:
            return Response({'error': 'No se puede actualizar una tarea completada'}, status=400)

        return super(TaskViewSet, self).update(request, *args, **kwargs)
    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'title' in request.data:
            if 'prueba' in request.data.get('title').lower():
                return Response({'error': 'No se puede actualizar una tarea con prueba en el titulo'}, status=400)
        if 'description' in request.data:
            if 'prueba' in request.data.get('description').lower():
                return Response({'error': 'No se puede actualizar una tarea con prueba en la descripcion'}, status=400)
        if instance.completed:
            return Response({'error': 'No se puede actualizar una tarea completada'}, status=400)

        return super(TaskViewSet, self).partial_update(request, *args, **kwargs)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.completed:
            return Response({'error': 'No se puede eliminar una tarea completada'}, status=400)

        return super(TaskViewSet, self).destroy(request, *args, **kwargs)
    

    def get_queryset(self):
        if self.request.user.has_perm('tasks.view_task') or self.request.user.is_anonymous:
            queryset = Task.objects.all()
            completed = self.request.query_params.get('completed')

            if completed is not None:
                if completed.lower() == 'true' or completed == '1':
                    queryset = queryset.filter(completed=True)

            return queryset
        
        return Task.objects.none()
    