from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from config.decorators import allowed_users
from costum.models import BaseModel, Company, Category, Brand, Model, Source, Status, Location, SubGabinete
from assets.models import RIR, RIRItem, Equipment
from distibuition.models import Distribution

#api distribuisaun Gab
class APIDistGab(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        label, obj = list(),list()
        muns = SubGabinete.active_objects.all()
        for m in muns:
            k = Distribution.objects.filter(sub_gabinete=m).count()
            label.append(m.name)
            obj.append(k)
        data = {'label':label, 'obj':obj}
        return Response(data)