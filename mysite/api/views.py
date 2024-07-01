import cProfile
import io
import pstats
import time
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from .serializers import ProductSerializer, OrderDetailSerializer, ProfileSerializer
from cart.models import OrderDetail
from users.models import Profile
from myapp.models import Product
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.versioning import URLPathVersioning
from rest_framework.throttling import UserRateThrottle
import asyncio
import cProfile
import pstats
import io
import schedule

# Кастомный класс пагинации
class CustomPagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_query_param = 'page_size'  # Параметр запроса для значения количества элементов на странице
    max_page_size = 100  # Максимально разрешенное количество элементов на странице

class CustomThrottle(UserRateThrottle):
    rate = '228/day'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]  # Добавляем фильтрацию
    search_fields = ['name', 'price', 'description']  # Замените "your_searchable_fields_here" на реальные поля, по которым вы хотите фильтровать
    pagination_class = CustomPagination  # Добавляем кастомную пагинацию
    permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated]
    versioning_class = URLPathVersioning
    throttle_classes = [CustomThrottle]
    async def perform_async_task(self, task_id):
        # Асинхронная операция, которая может быть выполнена в фоновом режиме
        await asyncio.sleep(1)
        print(f"Выполнено асинхронной задачи {task_id}")

    def async_operation(self):
        # Создание сопрограммы для выполнения асинхронной задачи
        async_tasks = [self.perform_async_task(i) for i in range(5)]

        # Запуск всех сопрограмм
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*async_tasks))
        loop.close()    

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]  # Добавляем фильтрацию
    search_fields = ['user_username', 'contact_number']  # Замените "your_searchable_fields_here" на реальные поля, по которым вы хотите фильтровать
    pagination_class = CustomPagination  # Добавляем кастомную пагинацию
    permission_classes = [IsAdminUser]
    versioning_class = URLPathVersioning
    throttle_classes = [CustomThrottle]
    async def perform_async_task(self, task_id):
        # Асинхронная операция, которая может быть выполнена в фоновом режиме
        await asyncio.sleep(1)

    def async_operation(self):
        # Создание сопрограммы для выполнения асинхронной задачи
        async_tasks = [self.perform_async_task(i) for i in range(5)]

        # Запуск всех сопрограмм
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*async_tasks))
        loop.close()

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    filter_backends = [filters.SearchFilter]  # Добавляем фильтрацию
    search_fields = ['customer_username', 'amount']  # Замените "your_searchable_fields_here" на реальные поля, по которым вы хотите фильтровать
    pagination_class = CustomPagination  # Добавляем кастомную пагинацию
    permission_classes = [IsAdminUser]
    versioning_class = URLPathVersioning
    async def perform_async_task(self, task_id):
        # Асинхронная операция, которая может быть выполнена в фоновом режиме
        await asyncio.sleep(1)
        print(f"Выполнено асинхронной задачи {task_id}")

    def async_operation(self):
        # Создание сопрограммы для выполнения асинхронной задачи
        async_tasks = [self.perform_async_task(i) for i in range(5)]

        # Запуск всех сопрограмм
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*async_tasks))
        loop.close()   