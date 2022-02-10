import logging
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from compute_anuga.models import Compute
from compute_anuga.serializers import ComputeSerializer

logger = logging.getLogger(__name__)


class ComputeViewSet(viewsets.ModelViewSet):
    serializer_class = ComputeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Compute.objects.all().order_by('-id')

    @action(detail=False, methods=['post'])
    def compute(self, request):
        logger.info(f'compute request: {request}')
        compute = self.get_object()
        compute.status = 'computing'
        compute.save()
        return Response(status=200)
