from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import demo.utils.stable_diffusion as sd
import demo.utils.image_utils as image_utils
from .models import Celeb, Celeb_occupation, Occupation
import os.path
from PIL import Image
import demo.utils.validations as validations

default_antiprompt = ("naked, nude, cleavage, deformed text, deformed logos, bad text, deformed hands,(worst quality, "
                      "low quality, illustration, 3d, 2d, painting, cartoons, sketch), open mouth, deformed fingers, "
                      "extra fingers")


def get_occupations_by_celeb_id(celeb_id):
    celeb_occupations = Celeb_occupation.objects.filter(celeb_id=celeb_id)
    for occ in celeb_occupations:
        print(occ.get().name)


# Create your views here.
def landing(request):
    return render(request, "landing.html")


def app(request):
    password = request.POST.get('password')
    user = request.POST.get('user')

    if password != "ReplicaAdmittedToS24" and user != "YCombinator":
        return HttpResponse("Invalid username or password")

    return render(request, "app.html")


def generate(request):
    if request.method == 'POST':
        celeb_name = request.POST.get("celebrity", "")
        prompt = request.POST.get("prompt", "")
        facial_expression = request.POST.get("facial_exp", "")
        age = request.POST.get("age", "")
        background = request.POST.get("background", "")
        angle = request.POST.get("angle", "")
        print(f"{celeb_name} with prompt: {prompt}")
        celeb_data = Celeb.objects.filter(name__exact=celeb_name).get()
        full_prompt = (f"A {angle} of {celeb_data.description},with a {facial_expression} expression, {prompt}. The "
                       f"background is {background} (elaborate background:1.6)")

        if validations.validate_prompt(prompt) and validations.validate_celeb(celeb_name):
            try:
                image1 = sd.text_to_image_with_reactor(full_prompt, default_antiprompt,
                                                       face_model=celeb_data.model_name,
                                                       steps=8, cfg_scale=2.5, swap_weight=0.4)
                image2 = sd.text_to_image_with_reactor(full_prompt, default_antiprompt,
                                                       face_model=celeb_data.model_name,
                                                       steps=8, cfg_scale=2.5, swap_weight=0.4)
                image3 = sd.text_to_image_with_reactor(full_prompt, default_antiprompt,
                                                       face_model=celeb_data.model_name,
                                                       steps=8, cfg_scale=2.5, swap_weight=0.4)

            except Exception as e:
                print(f"An error ocurred: {e}")
                return HttpResponse(f"Error: {e}")

            image1.save(os.path.abspath(os.path.dirname(__file__)) + "/static/img/jpg/img1.jpg")
            image2.save(os.path.abspath(os.path.dirname(__file__)) + "/static/img/jpg/img2.jpg")
            image3.save(os.path.abspath(os.path.dirname(__file__)) + "/static/img/jpg/img3.jpg")

            return render(request, 'generated-images.html')

        else:
            return HttpResponse("Failed to validate form data.<br> Please refresh this window.")


def login(request):
    return render(request, "login.html")


def celeb_browser(request):
    celeb_list = Celeb.objects.all().order_by('name')
    return render(request, "celeb-browser.html", {"celeb_list": celeb_list})


def brush_tool(request):

    return render(request, "brush-tool.html")


def generate_inpaint(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        negative_prompt = request.POST.get("negative_prompt", "")
        mask = request.POST.get("mask-image")
        reference_index = int(request.POST.get("reference-image-index")) % 3
        variation = int(request.POST.get("variation","")) / 100
        mask_image = image_utils.base64_to_image(mask).resize((1024,1024))

        mask_image.save("mask.jpg")
        if validations.validate_inpaint_prompt(prompt):
            try:
                modified_image = sd.image_to_image_with_inpaint(prompt, negative_prompt, Image.open(os.path.abspath(os.path.dirname(__file__)) + f"/static/img/jpg/img{reference_index+1}.jpg"), mask_image, denoising_strength=variation)
            except Exception as err:
                print("Something went wrong when generating inpaint")
                return HttpResponse("Error")

            modified_image.save(os.path.abspath(os.path.dirname(__file__)) + "/static/img/jpg/inpaint.jpg")

            return render(request, template_name="inpaint_image.html")
        else:
            return HttpResponse("Failed to validate prompt")



def replace_inpaint(request):
    if request.method == "POST":
        reference_index = int(request.POST.get("reference-image-index")) % 3
        inpaint_image = Image.open(os.path.abspath(os.path.dirname(__file__)) + f"/static/img/jpg/inpaint.jpg")
        inpaint_image.save(os.path.abspath(os.path.dirname(__file__)) + f"/static/img/jpg/img{reference_index+1}.jpg")


        return HttpResponse("Change done succesfully")
    else:
        return HttpResponse("Method not allowed")