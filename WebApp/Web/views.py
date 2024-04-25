from django.shortcuts import render
from .models import KnowledgeBaseViewerModel
def index(request):
    return render(request, "pages/index.html")


def knowledge_base(request):
    kbobj = KnowledgeBaseViewerModel.objects.all().filter(status_active=True)
    context = {
        "knowledge_base": kbobj
    }
    return render(request,
                  "pages/knowledge-base.html", context=context)
