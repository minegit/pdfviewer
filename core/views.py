from django.http import HttpResponse
from django.template import loader
from .forms import PdfForm
from django.utils.crypto import get_random_string
import os
from django.conf import settings
from wand.image import Image

# Create your views here.


def index(request):
    template = loader.get_template('core/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def ajax_upload_pdf(request):
    try:
    	import pdb
    	pdb.set_trace()
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            uid = get_random_string()
            print request.FILES["file"].name
            destination_path = os.path.join(settings.PDF_LOCATION, str(uid))
            os.makedirs(destination_path)
            thumbnail_directory = os.path.join(destination_path, "thumbnail")
            os.makedirs(thumbnail_directory)
            destination_file = os.path.join(destination_path, request.FILES["file"].name)
            destination_thumbnail_file = os.path.join(thumbnail_directory, request.FILES["file"].name[:4])
            with open(destination_file, 'wb+') as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            with Image(filename=destination_file) as img:
                img.save(filename=destination_thumbnail_file+"_temp.jpg")
            if os.path.exists(destination_thumbnail_file+"_temp.jpg"):
	            with Image(filename=destination_thumbnail_file+"_temp.jpg") as img:
				    img.resize(200,150)
				    img.save(filename=destination_thumbnail_file+".jpg")
				    os.remove(destination_thumbnail_file+"_temp.jpg")
            else:
				all_files = os.listdir(thumbnail_directory)
				for file in all_files:
					if not file == request.FILES["file"].name[:4]+"_temp-0.jpg":
						os.remove(os.path.join(thumbnail_directory, file))
				with Image(filename=destination_thumbnail_file+"_temp-0.jpg") as img:
					img.resize(200,150)
					img.save(filename=destination_thumbnail_file+".jpg")
					os.remove(destination_thumbnail_file+"_temp-0.jpg")
            return_data = dict({'summary': str("Successfully Inserted")})
        else:
            return_data = dict({'summary': str("Something missing in form")})
    except Exception, e:
        print(e)
        return_data = dict({'summary': str(e)})
    import json
    return HttpResponse(json.dumps(return_data), content_type='application/json')
