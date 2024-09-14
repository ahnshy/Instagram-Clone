from django.shortcuts import render
from rest_framework.views import APIView


class Main(APIView):
    def get(self, request):
        print("call get method.")
        return render(request, 'Instagram/index.html')
    def post(self, request):
        print("call post method.")
        return render(request, 'Instagram/index.html')


