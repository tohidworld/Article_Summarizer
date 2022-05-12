from Article_Summarization.summarizer import textSummarizer
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Article_Summarization.pdf_to_text import pdf_to_text
from Article_Summarization.link_to_text import link_to_text
import os
from whatsapp_bot.models import LinkSummary, TextSummary

# Create your views here.

def home(request):
    return render(request, 'home.html')

def summary(request):
    context = {}
    if request.method == "POST":
        status = 1
        #print(request.POST.keys())
        if 'link' in request.POST.keys():
            if 'http' in request.POST["link"]:
                result = LinkSummary.objects.filter(link__iexact=request.POST["link"]).values_list('summary', flat=True).first()
                if result is not None:
                    status = 2
                else:
                    status, body = link_to_text(request.POST["link"])
            else:
                body = 'Please Enter A Valid Link'
        if 'text' in request.POST.keys():
            body = str(request.POST["text"])
            result = TextSummary.objects.filter(text__iexact=body).values_list('summary', flat=True).first()
            if result is not None:
                status = 2
            else:
                status = 0
        if 'pdf' in request.POST.keys():
            uploadedPdf = request.FILES["uploadedPdf"]
            if '.pdf' in uploadedPdf.name: 
                fs = FileSystemStorage()
                filename = fs.save(uploadedPdf.name, uploadedPdf)
                status, body = pdf_to_text(filename)
                try:
                    os.remove('Article_Summarization/pdftemp/'+filename)
                except:
                    pass
            else:
                body = 'Please Enter A PDF File'
        if status == 0:
            status, body = textSummarizer(body)
            if status == 0:
                if 'link' in request.POST.keys():
                    ins = LinkSummary(link=request.POST["link"], summary=body)
                    ins.save()
                elif 'text' in request.POST.keys():
                    ins = TextSummary(text=body, summary=body)
                    ins.save()
            else:    
                body = 'Error Occcurred errorcode: '+body 
        if status == 1:
            body = 'Error Occcurred errorcode: '+body
        if status == 2:
            body = result
        context['body'] = body
    else:
        context['body'] = 'Please Enter Link, Text or Pdf To Get The Summary'
    return render(request, 'summary.html', context)

def connectivity(request):
    return render(request, 'connectivity.html')

def about(request):
    return render(request, 'about.html')
