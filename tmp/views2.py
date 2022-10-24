import json

from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework.request import Request
from rest_framework.views import APIView

from oozie.models2 import _save_workflow
from .api2 import _get_document_helper
from .lib.django_util import JsonResponse
from .models import Document2


class DocsView(APIView):
  # authentication_classes = []
  # permission_classes = []

  @staticmethod
  def get(request):
    response = {'status': -1}

    # request.user = User.objects.get(username=request.META['LOGNAME'])   # workaround by using logname
    path = request.GET.get('path', '/')

    response['status'] = 0
    response['documents'] = _get_document_helper(request, None, False, False, path)['children']
    response['count'] = len(response['documents'])
    return JsonResponse(response)

  @staticmethod
  def post(request: Request):
    response = {'status': -1}

    workflow = request.data['workflow']
    workflow.pop('id')
    layout = request.data['layout']
    workflow_doc = _save_workflow(workflow, layout, request.user, fs=request.fs)

    response['status'] = 0
    response['id'] = workflow_doc.id
    response['doc_uuid'] = workflow_doc.uuid
    response['message'] = _('Added !')
    return JsonResponse(response)


class DocView(APIView):
  # authentication_classes = []
  # permission_classes = []

  @staticmethod
  def get(request):
    response = {'status': -1}

    workflow_id = request.GET.get('workflow')
    wid = {}
    if workflow_id.isdigit():
      wid['id'] = workflow_id
    else:
      wid['uuid'] = workflow_id
    doc = Document2.objects.get(type='oozie-workflow2', **wid)

    response['status'] = 0
    if doc.is_trashed:
      response['is_trashed'] = True
    else:
      response['data'] = json.loads(doc.data)
    return JsonResponse(response)

  @staticmethod
  def put(request: Request):
    response = {'status': -1}

    # request.user = User.objects.get(username=request.META['LOGNAME'])   # workaround by using logname
    workflow = request.data['workflow']
    layout = request.data['layout']
    workflow_doc = _save_workflow(workflow, layout, request.user, fs=request.fs)

    response['status'] = 0
    response['id'] = workflow_doc.id
    response['doc_uuid'] = workflow_doc.uuid
    response['message'] = _('Modified !')
    return JsonResponse(response)

  @staticmethod
  def delete(request: Request):
    response = {'status': -1}

    # request.user = User.objects.get(username=request.META['LOGNAME'])   # workaround by using logname
    workflow_id = request.GET.get('workflow')
    wid = {}
    if workflow_id.isdigit():
      wid['id'] = workflow_id
    else:
      wid['uuid'] = workflow_id
    doc = Document2.objects.get(type='oozie-workflow2', **wid)
    doc.trash()

    response['status'] = 0
    response['id'] = doc.id
    response['doc_uuid'] = doc.uuid
    response['message'] = _('Trashed !')
    return JsonResponse(response)
