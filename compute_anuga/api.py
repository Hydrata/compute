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
        print(download_link)
        run_id = request.data.get('run_id')
        print(run_id)
        filename = request.data.get('filename')
        print(filename)
        package_subdirectory = os.path.join('/opt/anuga_data/', run_id)
        print(package_subdirectory)
        Path(package_subdirectory).mkdir(parents=True, exist_ok=True)
        url = urllib.request.urlopen(download_link)
        print(url)
        saved_zip_filepath = os.path.join(package_subdirectory, filename)
        print(saved_zip_filepath)
        with open(saved_zip_filepath, 'wb') as new_file:
            new_file.write(url.read())
        print('open')
        shutil.unpack_archive(saved_zip_filepath, package_subdirectory)
        anuga_runfile = os.path.join(package_subdirectory, 'code', 'run_anuga.py')
        print(anuga_runfile)
        print(os.getenv("ANUGA_ADMIN_USERNAME"))
        print(os.getenv("ANUGA_ADMIN_PASSWORD"))
        subprocess.call(['whoami'])
        print(f'mpirun -np 8 /opt/venv/compute/bin/python {anuga_runfile} {os.getenv("ANUGA_ADMIN_USERNAME")} {os.getenv("ANUGA_ADMIN_PASSWORD")}')
        subprocess.Popen(['mpirun', '-np', '24', '/opt/venv/compute/bin/python', anuga_runfile, os.getenv("ANUGA_ADMIN_USERNAME"), os.getenv("ANUGA_ADMIN_PASSWORD")], cwd=os.path.join(package_subdirectory, 'code'))
        print('anuga_runfile done')
        # mpirun -np 8 /opt/venv/hydrata/bin/python /opt/hydrata/gn_anuga/run_code/run_anuga.py "test"

        compute = self.get_object()
        compute.status = 'computing'
        compute.save()
        return Response(status=200)
