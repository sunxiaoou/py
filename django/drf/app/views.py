import uuid

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import Authentication
from .models import Book, User, UserToken
from .serializers import BookSerializer


# Create your views here.
class BooksView(APIView):
    # authentication_classes = [Authentication]
    @staticmethod
    def get(request: Request):
        books = Book.objects.order_by('pub_date')
        serializer = BookSerializer(books, many=True)
        return Response({'msg': 'ok', 'data': serializer.data})

    @staticmethod
    def post(request: Request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'ok', 'data': serializer.data})
        return Response({'msg': 'fail', 'data': serializer.errors})


class BookView(APIView):
    @staticmethod
    def get(request, pk):
        book = Book.objects.get(id=pk)
        return Response({'msg': 'ok', 'data': BookSerializer(book).data})

    @staticmethod
    def put(request, pk):
        book = Book.objects.get(id=pk)
        serializer = BookSerializer(book, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'ok', 'data': serializer.data})
        return Response({'msg': 'fail', 'data': serializer.errors})

    @staticmethod
    def delete(request, pk):
        Book.objects.filter(id=pk).delete()
        return Response({"msg": 'ok'})


class LoginView(APIView):
    authentication_classes = []

    @staticmethod
    def post(request):
        back_msg = {'status': 1001, 'msg': None}
        try:
            name = request.data.get('username')
            pwd = request.data.get('password')
            user = User.objects.filter(username=name, password=pwd).first()
            if user:
                token = uuid.uuid4()
                UserToken.objects.update_or_create(user=user, defaults={'token': token})
                back_msg['status'] = '1000'
                back_msg['msg'] = '登录成功'
                back_msg['token'] = token
            else:
                back_msg['msg'] = '用户名或密码错误'
        except Exception as e:
            back_msg['msg'] = str(e)
        return Response(back_msg)
