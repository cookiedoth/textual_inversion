import os

MODEL_PATH = 'models/ldm/text2img-large/model.ckpt'

print('Name: ', end='')
name = input()

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

prompts = ['The streets of Paris in the style of *',
    'Adorable corgi in the style of *',
    'Painting of a black hole in the style of *',
    'Times square in the style of *',
    'Painting of a mountain peak in the style of *',
    'Portrait in the style of *',
    'Painting of an ocean wave in the style of *',
    'A photo of *']

for prompt in prompts:
    os.system(f'python scripts/txt2img.py --ddim_eta 0.0  --n_samples 8 --n_iter 2 --scale 10.0 --ddim_steps 50 --embedding_path {path}  --ckpt_path {MODEL_PATH} --prompt "{prompt}"')

os.system(f'mv outputs saved_outputs/{name}')