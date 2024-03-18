from diffusers import DiffusionPipeline
import torch
import os
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

def generate_image_with_diffusers(prompt, output_path="generated_image.png", num_inference_steps=8, guidance_scale=7.5):
    # Initialize the pipeline with torch.float32 for broader compatibility
    pipeline = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
    
    # Attempt to use M1 GPU acceleration if available, otherwise fall back to CPU
    device = "cpu"
    pipeline = pipeline.to(device)

    # Generate the image with reduced number of inference steps and potentially adjusted guidance scale
    # Lowering the guidance scale can also speed up the process slightly at the cost of adherence to the prompt
    image = pipeline(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage with reduced inference steps and guidance scale for quicker generation
prompt = "A futuristic city skyline at sunset"
generate_image_with_diffusers(prompt)
