import helpers
import os

lst = ['python', 'main.py', '--base', 'configs/latent-diffusion/txt2img-1p4B-finetune.yaml', '-t', '--actual_resume', 'models/ldm/text2img-large/model.ckpt', '-n', 'tmp', '--gpus', '0,', '--data_root', 'source_img', '--init_word', 'style']
helpers.execute(lst)
# os.system(' '.join(lst))
