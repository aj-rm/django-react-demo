from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializer import TaskSerializer
from .models import *


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
        queryset = Task.objects.all()
        completed = self.request.query_params.get('completed')

        if completed is not None:
            if completed.lower() == 'true' or completed == '1':
                queryset = queryset.filter(completed=True)

        return queryset
    