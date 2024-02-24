from demo.models import Celeb


def validate_prompt(prompt: str):
    result = 0 < len(prompt) < 150 and prompt.strip(" ") != ""
    return result


def validate_celeb(celeb_name: str):
    result = Celeb.objects.filter(name=celeb_name).exists()
    return result


def validate_expression(prompt: str):
    result = 0 < len(prompt) < 80 and prompt.strip(" ") != ""
    return result


def validate_age(prompt: str):
    result = 0 < len(prompt) < 80 and prompt.strip(" ") != ""
    return result


def validate_background(prompt: str):
    result = 0 < len(prompt) < 80 and prompt.strip(" ") != ""
    return result

def validate_inpaint_prompt(prompt: str):
    result = 0 < len(prompt) < 80 and prompt.strip(" ") != ""
    return result