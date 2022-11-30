import os

MODEL_PATH = 'models/ldm/text2img-large/model.ckpt'

def append_path_prompt(path):
    variants = os.listdir(path)
    for i, x in enumerate(variants):
        print(i, x, sep='\t')
    pos = int(input())
    assert(pos >= 0 and pos < len(variants))
    return os.path.join(path, variants[pos])

path = append_path_prompt('best_artworks/logs')
path = os.path.join(path, 'checkpoints')
path = append_path_prompt(path)
print('Path:', path)

print('Prompt: ', end='')
prompt = input()

os.system(f'python scripts/txt2img.py --ddim_eta 0.0  --n_samples 8 --n_iter 2 --scale 10.0 --ddim_steps 50 --embedding_path {path}  --ckpt_path {MODEL_PATH} --prompt "{prompt}"')
