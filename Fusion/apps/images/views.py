from rest_framework.views import APIView
from rest_framework import status
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.response import Response


class UploadFileViews(APIView):
    def post(self, request):
        upload_files = request.FILES.getlist('file', None)
        task_id = request.data.get("task_id")
        chuck = request.data.get("chuck", 0)
        for item in upload_files:
            file_name = "{task_id}{chuck}{name}".format(task_id=task_id,
                                                        chuck=chuck,
                                                        name = item.name,)
            file = item.file
            default_storage.save("./upload/iso/{file_name}".format(file_name=file_name),
                                 ContentFile(file.read())
                                 )

        return Response({"message":"文件分片", "status":200})


class MergeViews(APIView):

    def get(self, request):
        task_id = request.query_params.get("task_id")
        filename = request.query_params.get('filename', '')



