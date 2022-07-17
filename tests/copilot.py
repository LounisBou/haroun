import torch
from dalle_pytorch import DiscreteVAE, DALLE

def generateImage(text):
    """
        use OpenAI's Pretrained VAE to generate an image from a text.
        text: string of text to generate an image from.
        return: image.
    """

    # load the pretrained DiscreteVAE
    vae = DiscreteVAE(
        image_size = 256,
        num_layers = 3,
        num_tokens = 8192,
        codebook_dim = 1024,
        hidden_dim = 64,
        num_resnet_blocks = 1,
        temperature = 0.9
    )

    # Load the pretrained VAE
    vae = DALLE(
        dim = 1024,
        vae = vae,                  # automatically infer (1) image sequence length and (2) number of image tokens
        num_text_tokens = 10000,    # vocab size for text
        text_seq_len = 256,         # text sequence length
        depth = 12,                 # should aim to be 64
        heads = 16,                 # attention heads
        dim_head = 64,              # attention head dimension
        attn_dropout = 0.1,         # attention dropout
        ff_dropout = 0.1            # feedforward dropout
    )
    # Load the text
    text = torch.tensor(text, dtype=torch.long)
    # Generate an image
    image = vae.generate(text)
    # Return the image
    return image

generateImage("Hello World")

