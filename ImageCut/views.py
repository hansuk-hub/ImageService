from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from io import StringIO
import os
from zipfile import ZipFile
from PIL import Image
import math
from django.conf import settings
import datetime

from .models import  *


# Create your views here.
def test(request):
    if request.method == "GET" :
        return render(request, './test.html')

    elif request.method =='POST' :
        file_list = request.FILES.getlist('fileToUpload')

    tempImage = TempImage.objects.create(
        image = file_list[0]
    )

    image_name = tempImage.image.name.split('/')[1].split('.')[0]

    img = Image.open(tempImage.image.path)
    width, height = img.size
    upper = 0
    left = 0
    slice_size = 2500

    slices = int(math.ceil(height / slice_size))
    count = 1

    sliced_image_path_list = []

    for slice in range(slices) :
        if count == slices :
            lower = height
        else:
            lower = int(count * slice_size)

        bbox = (left, upper, width, lower)
        working_slice = img.crop(bbox)

        #working_slice = add_margin(
            # working_slice, 100, 0, 100, 0 , (255,255,255))
        upper += slice_size
        path = os.path.join(
            settings.BASE_DIR + "/sliced_image/", image_name + str(count) + ".jpg")
        working_slice.save(path)
        sliced_image_path_list.append(path)
        count += 1

    response  = HttpResponse(content_type = 'application/zip')

    zf = ZipFile(response, 'w')

    zip_subdir = str(datetime.datetime.now())
    zip_filename = "%s.zip" % zip_subdir

    for fpath in sliced_image_path_list :
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

    zf.close()



    os.remove(tempImage.image.path)
    tempImage.delete()

    for path in sliced_image_path_list:
        os.remove(path)

    response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return response