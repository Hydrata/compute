import logging

import os
import shutil
from pathlib import Path
import urllib.request

import subprocess
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
        logger.error(f'compute request: {request}')
        print("compute:")
        print(request)
        print(request.data)
        download_link = request.data.get('download_link')
        run_id = request.data.get('run_id')
        filename = request.data.get('filename')
        package_subdirectory = os.path.join('/opt/anuga_data/', run_id)
        Path(package_subdirectory).mkdir(parents=True, exist_ok=True)
        url = urllib.request.urlopen(download_link)
        saved_zip_filepath = os.path.join(package_subdirectory, filename)
        with open(saved_zip_filepath, 'wb') as new_file:
            new_file.write(url.read())
        shutil.unpack_archive(saved_zip_filepath)
        anuga_runfile = os.path.join(package_subdirectory, 'code', 'run_anuga.py')
        subprocess.call(['mpirun', '-np', '1', '/opt/venv/compute/bin/python', anuga_runfile, os.getenv("ANUGA_ADMIN_USERNAME"), os.getenv("ANUGA_ADMIN_PASSWORD")])
        # mpirun -np 8 /opt/venv/hydrata/bin/python /opt/hydrata/gn_anuga/run_code/run_anuga.py "test"

        compute = self.get_object()
        compute.status = 'computing'
        compute.save()
        return Response(status=200)
