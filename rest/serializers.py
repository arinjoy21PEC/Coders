from rest_framework import serializers
from rest.models import Company
class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Company
        fields = "__all__"
