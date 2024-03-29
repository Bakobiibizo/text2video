from diffusers.pipelines.pipeline_utils import DiffusionPipeline
from PIL import Image
import torch
import random


def generate_image(
    input_prompt="a futuristic city scape, intergalatic civilization floating through a colorful universe, stars and colorful nebula, award winning illustration, highly detailed, bold line work, bright saturated colors, beautiful composition, artstation, 8k",
) -> Image.Image:
    negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry, lens flair, horrifying, ugly, deformed, grotesque"
    # load both base & refiner experts
    base = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True,
    )
    base.to("cuda")
    refiner = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )
    refiner.to("cuda")

    # Define how many steps and what % of steps to be run on each experts (80/20) here
    n_steps = 35
    high_noise_frac = 0.8

    prompt = (
        input_prompt
        or "a futuristic city scape, intergalatic civilization floating through a colorful universe, stars and colorful nebula, award winning illustration, highly detailed, bold line work, bright saturated colors, beautiful composition, artstation, 8k"
    )
    negative_prompt = "ugly, grotesque, deformed, horrifying, blury, smeared, burnt, weird hands, bad hands, too many limbs, detached limbs"

    # run both experts
    base_image = base(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,  # type: ignore
        output_type="latent",
    ).images  # type: ignore
    return refiner(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_start=high_noise_frac,  # type: ignore
        image=base_image,
    ).images[0]  # type: ignore
