from paintings import Painting
import helpers
import shutil
import os
import re
import torch
from torch import nn
from PIL import Image

SOURCE_IMG_PATH = 'source_img'
LOGS_PATH = 'logs'
TMP_PATH = 'tmp'
TMP_EMBEDDING_PATH = os.path.join(TMP_PATH, 'embedding.pt')
STAR_TOKEN = 1008
OUTPUTS_PATH = 'outputs/txt2img-samples'

def get_last_log_path(name='tmp'):
    cand = list(filter(lambda x: x.startswith(SOURCE_IMG_PATH) and x.endswith(f'_{name}'),
        sorted(os.listdir(LOGS_PATH))))
    if not cand:
        return None
    return os.path.join(LOGS_PATH, cand[-1])


def retrieve_last_embedding(name='tmp'):
    last_log_path = get_last_log_path(name)
    if last_log_path is None:
        return None
    embeddings_path = f'{last_log_path}/checkpoints'

    # embeddings_gs-999.pt -> 999
    key_func = lambda filename: int(re.findall(r'\d+', filename)[0]) if filename.startswith('embeddings_gs') else 0
    cand = sorted(os.listdir(embeddings_path), key = key_func)

    if not cand:
        return None

    last_embedding_path = os.path.join(embeddings_path, cand[-1])
    result = torch.load(last_embedding_path)
    return result['string_to_param']['*'].detach()


def delete_last_embedding():
    shutil.rmtree(get_last_log_path())


def invert(painting, name='tmp', silent=False):
    shutil.rmtree(SOURCE_IMG_PATH, ignore_errors=True)
    os.makedirs(SOURCE_IMG_PATH, exist_ok=True)
    painting.image.save(os.path.join(SOURCE_IMG_PATH, '1.jpg'))
    helpers.execute([
        'python',
        'main.py',
        '--base',
        'configs/latent-diffusion/txt2img-1p4B-finetune.yaml',
        '-t',
        '--actual_resume',
        'models/ldm/text2img-large/model.ckpt',
        '-n',
        f'{name}',
        '--gpus',
        '0,',
        '--data_root',
        f'{SOURCE_IMG_PATH}',
        '--init_word',
        'painting'
    ], silent=silent)
    result = retrieve_last_embedding(name)
    return result


def generate(embedding, prompt='A photo of *', silent=False):
    os.makedirs(TMP_PATH, exist_ok=True)
    parameterDict = torch.nn.ParameterDict({
        '*': nn.Parameter(embedding) })
    emb_to_save = {'string_to_param': parameterDict,
        'string_to_token': {'*': torch.tensor(STAR_TOKEN)}}
    torch.save(emb_to_save, TMP_EMBEDDING_PATH)
    helpers.execute([
        'python',
        'scripts/txt2img.py',
        '--ddim_eta',
        '0.0',
        '--n_samples',
        '8',
        '--n_iter',
        '2',
        '--scale',
        '10.0',
        '--ddim_steps',
        '50',
        '--embedding_path',
        f'{TMP_EMBEDDING_PATH}',
        '--ckpt_path',
        'models/ldm/text2img-large/model.ckpt',
        '--prompt',
        f'{prompt}'
    ], silent=silent)
    prompt_filename = prompt.replace(' ', '-')
    image = Image.open(os.path.join(OUTPUTS_PATH, f'{prompt_filename}.jpg'))
    image.load()
    return image


if __name__ == '__main__':
    emb = retrieve_last_embedding()
    generate(emb, silent=True)
