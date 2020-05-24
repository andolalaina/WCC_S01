from django.db.models import Q
from django.db import models

from datetime import datetime
from functools import reduce
import operator
import string
import csv
import io
import os

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings

from kopia.settings import MEDIA_ROOT

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def handle_uploaded_file(f, filename):
    path_to = os.path.join(MEDIA_ROOT, filename)
    with open(path_to, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)