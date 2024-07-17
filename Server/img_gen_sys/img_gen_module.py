from util import load_text_file, load_config, send_generation_request
from PIL import Image
import IPython.display
import os

class StableDiffusionImageGenerator:
    def __init__(self, args):
        self.args = args
        self.init_arguments()
        self.last_image = None

    @classmethod
    def set_initial_arguments(cls, args):
        generator = cls(args)
        generator.init_arguments()
        return generator

    def init_arguments(self):
        if not hasattr(self.args, "style_pre"):
            self.args.style_pre = "Create an illustration of"

        if not hasattr(self.args, "style_post"):
            self.args.style_post = "using watercolor for soft colors with vibrant, pastel colors and gentle, natural lighting with high resolution."
        
        if not hasattr(self.args, "postfix"):
            self.args.postfix = "This artwork should be suitable for sharing on art-sharing websites like DeviantArt."
        
        if not hasattr(self.args, "aspect_ratio"):
            self.args.aspect_ratio = "1:1"
        
        if not hasattr(self.args, "output_format"):
            self.args.output_format = "jpeg"
        
        if hasattr(self.args, "seed"):
            self.args.seed = int(self.args.seed)
        else:
            self.args.seed = 0

    def set_prompts(self, prompt):
        self.args.prompt = f"{self.args.style_pre} {prompt}, {self.args.style_post}, {self.args.postfix}"

    def get_img(self, prompt, display=False):
        self.set_prompts(prompt)
        response = send_generation_request(self.args)
        if response.headers.get("finish-reason") != 'CONTENT_FILTERED':
            self.last_image = response.content
        if display:
            self.display_image()
        return response

    def display_image(self):
        if self.last_image is None:
            return False
        else:
            # Save and display result
            img_path = f"./img/last_image.jpg"
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(self.last_image)
            print(f"Saved image {img_path}")
            print("Result image:")
            IPython.display.display(Image.open(img_path))
            return True

    def save_image(self, user_id, date):
        img_path = f"./img/{user_id}-{date}.jpg"
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        with open(img_path, "wb") as f:
            f.write(self.last_image)
        print(f"Saved image {img_path}")

    def get_args(self):
        return self.args
