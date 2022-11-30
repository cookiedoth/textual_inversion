import torch
import os
import random
import shutil

random.seed(42)

PICS_PATH = 'resized/resized'
CONFIG_PATH = '../configs/latent-diffusion/txt2img-1p4B-finetune.yaml'
MODEL_PATH = '../models/ldm/text2img-large/model.ckpt'
DATA_ROOT = 'imgs'
INIT_WORD = 'style'

def extract_styles(artist_name, bucket_count, bucket_size):
    filenames = list(filter(lambda s: s.startswith(artist_name), os.listdir(PICS_PATH)))
    if len(filenames) < bucket_count * bucket_size:
        print('Not enough paintings')
        return
    random.shuffle(filenames)
    if not os.path.exists('imgs'):
        os.makedirs('imgs')
    for i in range(bucket_count):
        os.system('rm imgs/*')
        cur_pics = filenames[bucket_size * i: bucket_size * (i + 1)]
        for pic in cur_pics:
            shutil.copyfile(f'{PICS_PATH}/{pic}', f'imgs/{pic}')
        try:
            os.system(f'python ../main.py --base {CONFIG_PATH} -t --actual_resume {MODEL_PATH} -n {artist_name}{i} --gpus 0, --data_root {DATA_ROOT} --init_word {INIT_WORD}')
        except:
            pass

extract_styles('Alfred_Sisley', 5, 5)
