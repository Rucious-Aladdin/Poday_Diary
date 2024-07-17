# -*- coding: utf-8
from util import *
from img_gen_module import StableDiffusionImageGenerator


if __name__ == "__main__":
    path_to_config = "./config/"
    config_filename = "config.txt"

    config_text = load_text_file(path_to_config, config_filename)
    config = load_config(config_text)

    img_generator = StableDiffusionImageGenerator.set_initial_file(config)
    response = img_generator.get_img(input(), display=True)
    output_image = response.content
