from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from io import StringIO
import os
from zipfile import ZipFile
from PIL import Image
import math
from django.conf import settings
import datetime
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import *
def index(request):
    if request.method == "GET":
        # try :
        #     fileNum = int(request.GET['fileNum'])
        #     print('aa')
        # except :
        #     fileNum = 0
        args = {}
        try :
            fileNum = int(request.GET['fileNum'])
            addNum = fileNum + 1
            print(addNum)
        except :
            fileNum = 1
            addNum = 2


        args.update({"fileNum" : fileNum })
        args.update({"addNum": addNum})


        return render(request, 'index.html', args )

    elif request.method == 'POST':




        global outBody
        global allCont



        def wrapStringInHTMLWindows(outBody):

            filename = str(settings.BASE_DIR) + "/makelist/templates/list.html"
            f = open(filename, 'wb')
            f.write(outBody.encode())
            f.close()

            response = HttpResponse("", content_type='application/liquid;')
            response['Content-Length'] = len(outBody)

            # response['Content-Disposition'] = 'inline; filename=' + filename
            response.write(outBody.encode())
            return response

        thumbCnt = 0

        # 써머리 출력
        outBody = "<html><head><meta charset='UTF-8'><style>@import url('https://fonts.googleapis.com/css2?family=Overpass:wght@900&display=swap');             " \
                  "@font-face {     font-family: 'S-CoreDream-3Light';     src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');     font-weight: normal;     font-style: normal;}             .t_number { font-family: 'Saira Stencil One', cursive; font-family: 'Overpass', cursive; font-weight:900; font-size:48px;	color:#666;  text-align:center; } td .t_title { font-family: 'S-CoreDream-3Light'; font-size: 24px; height : 80px;  vertical-align:top;} .thumb-img { border-radius: 4%;}   td { text-align:center; } </style></head><body>{% load static %} <table align='center' style='border-collapse: collapse; border: 1px solid black;'><tr><td colspan='2'>"



        fileNum = request.POST['fileNum']

        for i in range(1,int(fileNum)+ 1) :
            thumbCnt += 1

            file_list = request.FILES.getlist('fileInput' + str(i))

            tempImage = TempImage.objects.create(
                image=file_list[0]
            )
            # image_name = tempImage.image.name.split('/')[1].split('.')[0]

            left = upper = 0
            bbox = (left, upper, 400, 400)
            img = Image.open(tempImage.image.path)
            working_slice = img.crop(bbox)

            path = os.path.join(
                str(settings.BASE_DIR) + "/makelist/temp_image/", str(file_list[0]))

            working_slice.save(path)

            outBody += '<table border=0 ><tr><td align="center">'
            outBody += '<img class="thumb-img" src="{% static "' + str(tempImage.image.name.split('/')[2]) + '" %}" >'
            outBody += '</td></tr><tr><td class="t_number" style="font-size:72px; font-weight:900; color:#666;  text-align:center;">'
            if ( i < 10 ):
                outBody += str(0)
            outBody += str(i)
            outBody += '</td></tr><tr><td align="center" class="t_title">'
            outBody += request.POST['productName'+ str(i) ]
            outBody += '</td></tr></table>'


            if (thumbCnt % 2 == 0):
                outBody += "</td></tr><tr><td colspan='2'>"
            else:
                outBody += "</td><td>"

        outBody += "</td></tr></table>"

        outBody += "</body></html>"

        wrapStringInHTMLWindows(outBody)

        return render(request, 'list.html' )



