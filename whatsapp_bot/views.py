import requests
from django.shortcuts import render, HttpResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from Article_Summarization.link_to_text import link_to_text
from Article_Summarization.pdf_to_text import pdf_to_text
from Article_Summarization.summarizer import textSummarizer
from .divider import divider
from .models import TextSummary, LinkSummary
import time
import os



#twilio ac details
account_sid = 'ACe30a58028273006bd38eb8d1eec820aa'
auth_token = '0ab3a09d472da28d413f54536fe7c5d1'
client = Client(account_sid,auth_token)

# Create your views here.

@csrf_exempt
def bot(request):
    try:
        sender_number = request.POST["From"]
        #print(request.POST["From"])
        status = 1
        if "MediaContentType0" in request.POST:
            if 'application/pdf' == request.POST["MediaContentType0"]:
                try:
                    response = requests.get(request.POST["MediaUrl0"])
                    with open('Article_Summarization/pdftemp/'+request.POST["Body"], 'wb') as f:
                        f.write(response.content)
                    status, body = pdf_to_text(request.POST["Body"])
                except Exception as e:
                    body = str(e)
                    status = 1
                try:
                    os.remove('Article_Summarization/pdftemp/'+request.POST["Body"])
                    pass
                except:
                    pass   
            else:
                body = 'Plz send valid pdf/text/links'
        elif 'http' in request.POST["Body"]:
            result = LinkSummary.objects.filter(link__iexact=request.POST["Body"]).values_list('summary', flat=True).first()
            if result is not None:
                status = 2
            else:
                status, body = link_to_text(request.POST["Body"])     
        else:
            body = str(request.POST["Body"])
            result = TextSummary.objects.filter(text__iexact=body).values_list('summary', flat=True).first()
            if result is not None:
                status = 2
            else:
                status = 0
    except:
        pass
    if status == 0:
        status, body = textSummarizer(body)
        if status == 0:
            if 'http' in request.POST["Body"]:
                ins = LinkSummary(link=request.POST["Body"], summary=body)
                ins.save()
            elif "MediaContentType0" not in request.POST:
                ins = TextSummary(text=body, summary=body)
                ins.save()
        else:    
            body = 'Error Occcurred errorcode: '+body 
    if status == 1:
        body = 'Error Occcurred errorcode: '+body  
    if status == 2:
            body = result
    lst = divider(body, 1200)
    for msg in lst:
        try:
            client.messages.create(
                from_='whatsapp:+14155238886',
                body=msg,
                to=sender_number,
            )
            time.sleep(2)
        except:
            time.sleep(3)
            client.messages.create(
                from_='whatsapp:+14155238886',
                body='Some Error Occured Please Try Later',
                to=sender_number,
            )
    return HttpResponse('ok')

