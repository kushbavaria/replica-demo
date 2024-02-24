import requests
import json
from PIL import Image, ImageOps
import demo.utils.image_utils as image_utils
BASE_URL = "https://c4gwlbgfo255uv-3001.proxy.runpod.net"


def load_model(model=None):
    if model is None:
        model = 'RealVisXL3.safetensors'

    option_payload = {
        "sd_model_checkpoint": model,
    }

    response = requests.post(f"{BASE_URL}/sdapi/v1/options", json=option_payload)
    if response.status_code != 200:
        raise Exception("Failed to load model")
    print(response.text)
    return True


def text_to_image(prompt: str, negative_prompt: str,
                  model: str = None, save_images: bool = True,
                  steps: int = 20, cfg_scale: float = 7.0, enable_hr: bool = True,
                  sampler_name: str = "DPM++ 2M Karras", denoising_strength: float = 0.7) -> Image:
    load_model(model)

    body = {
        "prompt": prompt,
        "steps": steps,
        "width": 512,
        "negative_prompt": negative_prompt,
        "send_images": True,
        "save_images": save_images,
        "height": 512,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler_name,
        "enable_hr": enable_hr,
        "hr_scale": 2,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_checkpoint_name": "RealVisXL3.safetensors" if model is None else model,
        "hr_sampler_name": sampler_name,
        "denoising_strength": denoising_strength
    }
    image_to_image_payload = json.dumps(body)
    response = requests.post(f"{BASE_URL}/sdapi/v1/txt2img", data=image_to_image_payload)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception("Something went wrong in the image generation")

    encoded_result_image = response.json()["images"][0]
    result_image = image_utils.base64_to_image(encoded_result_image)

    return result_image


def text_to_image_with_reactor(prompt: str, negative_prompt: str,
                               model: str = None, save_images: bool = True,
                               steps: int = 20, cfg_scale: float = 7.0, enable_hr: bool = True,
                               sampler_name: str = "DPM++ SDE Karras", reference_image: Image = None,
                               face_model: str = None, swap_weight: float = 0.5,
                               denoising_strength: float = 0.7) -> Image:
    load_model(model)
    encoded_reference_image = image_utils.image_to_base64(reference_image) if reference_image is not None else None

    reactor_arguments = [
        encoded_reference_image,  # reference image
        True,
        '0',
        '0',
        'inswapper_128.onnx',
        'CodeFormer',
        1,
        False,
        'None',
        1,
        1,
        False,
        True,
        1,
        0,
        0,
        False,
        swap_weight,
        False,
        False,
        "CUDA",
        True,
        0 if reference_image is not None else 1,
        f"{face_model}.safetensors",
        ""
    ]

    print(reactor_arguments)

    body = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "send_images": True,
        "save_images": save_images,
        "steps": steps,
        "width": 512,
        "height": 512,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler_name,
        "enable_hr": enable_hr,
        "hr_scale": 2,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_checkpoint_name": "RealVisXL3.safetensors" if model is None else model,
        "hr_sampler_name": sampler_name,
        "alwayson_scripts": {"reactor": {"args": reactor_arguments}},
        "denoising_strength": denoising_strength
    }

    text_to_image_payload = json.dumps(body)
    response = requests.post(f"{BASE_URL}/sdapi/v1/txt2img", data=text_to_image_payload)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception("Something went wrong in the image generation")

    encoded_result_image = response.json()["images"][0]
    result_image = image_utils.base64_to_image(encoded_result_image)

    return result_image


def image_to_image_with_inpaint(prompt: str, negative_prompt: str,
                                reference_image: Image, mask_image: Image,
                                model: str = None, save_images: bool = True,
                                steps: int = 20, cfg_scale: float = 7.0, enable_hr: bool = True,
                                sampler_name: str = "DPM++ SDE Karras", denoising_strength: float = 0.5,
                                ) -> Image:
    load_model(model)
    encoded_reference_image = image_utils.image_to_base64(reference_image)
    encoded_mask_image = image_utils.image_to_base64(mask_image)

    body = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "send_images": True,
        "save_images": save_images,
        "steps": steps,
        "width": 512,
        "height": 512,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler_name,
        "enable_hr": enable_hr,
        "hr_scale": 2.5,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_checkpoint_name": "RealVisXL3.safetensors" if model is None else model,
        "hr_sampler_name": sampler_name,
        "init_images": [
            encoded_reference_image
        ],
        "denoising_strength": denoising_strength,
        "mask": encoded_mask_image,
        "mask_blur": 0,
        "inpainting_fill": 1,
        "inpaint_full_res": True,
        "inpaint_full_res_padding": 0,
        "inpainting_mask_invert": 0,
    }

    image_to_image_payload = json.dumps(body)
    response = requests.post(f"{BASE_URL}/sdapi/v1/img2img", data=image_to_image_payload)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception("Something went wrong while generating image")

    encoded_result_image = response.json()["images"][0]
    result_image = image_utils.base64_to_image(encoded_result_image)

    return result_image


def get_background_mask(reference_image: Image) -> Image:
    encoded_reference_image = image_utils.image_to_base64(reference_image)

    body = {
        "input_image": encoded_reference_image,
        "model": "u2net",
        "return_mask": True,
        "alpha_matting": False
    }

    rembg_payload = json.dumps(body)
    response = requests.post(f"{BASE_URL}/rembg", data=rembg_payload)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception("Something went wrong while generating mask")

    encoded_mask_image = response.json()["image"]
    mask_image = image_utils.base64_to_image(encoded_mask_image)

    fixed_mask_image = ImageOps.invert(mask_image)

    return fixed_mask_image


def upscale_image(image: Image):
    encoded_image = image_utils.image_to_base64(image)

    body = {
        "image": encoded_image,
        "upscaling_resize": 4,
        "codeformer_visibility": 1,
        "codeformer_weight": 0.058,
        "upscaler_1": "ESRGAN_4x",
        "extras_upscaler_2_visibility": 0,
    }

    upscale_payload = json.dumps(body)
    response = requests.post(f"{BASE_URL}/sdapi/v1/extra-single-image", data=upscale_payload)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception("Something went wrong while upscaling")

    encoded_upscaled_image = response.json()["image"]
    upscaled_image = image_utils.base64_to_image(encoded_upscaled_image)

    return upscaled_image


def image_to_image_control_net(prompt: str, negative_prompt: str,
                               reference_image: Image, mask_image: Image,
                               model: str = None, save_images: bool = True,
                               steps: int = 20, cfg_scale: float = 7.0, enable_hr: bool = True,
                               sampler_name: str = "DPM++ SDE Karras", denoising_strength: float = 0.5,
                               ) -> Image:
    load_model(model)
    encoded_reference_image = image_utils.image_to_base64(reference_image)
    encoded_mask_image = image_utils.image_to_base64(mask_image)

    body = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "send_images": True,
        "save_images": save_images,
        "steps": steps,
        "width": 512,
        "height": 512,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler_name,
        "enable_hr": enable_hr,
        "hr_scale": 2.5,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_checkpoint_name": "RealVisXL3.safetensors" if model is None else model,
        "hr_sampler_name": sampler_name,
        "init_images": [
            encoded_reference_image
        ],
        "denoising_strength": denoising_strength,
        "mask": encoded_mask_image,
        "mask_blur": 0,
        "inpainting_fill": 1,
        "inpaint_full_res": True,
        "inpaint_full_res_padding": 0,
        "inpainting_mask_invert": 0,

        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "input_image": encoded_reference_image,
                        "module": "depth",
                        "pixel_perfect": False,
                        "model": "sai_xl_depth_256lora [73ad23d1]"
                    }
                ]
            }
        }
    }

    image_to_image_payload = json.dumps(body)
    response = requests.post(f"{BASE_URL}/sdapi/v1/img2img", data=image_to_image_payload)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception("Something went wrong while generating image with controlnet")

    encoded_result_image = response.json()["images"][0]
    result_image = image_utils.base64_to_image(encoded_result_image)

    return result_image
