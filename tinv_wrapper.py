from paintings import Painting
import shutil
import os

SOURCE_IMG_PATH = 'source_img'

def invert(painting):
    # shutil.rmtree(SOURCE_IMG_PATH, ignore_errors=True)
    # os.makedirs(SOURCE_IMG_PATH, exist_ok=True)
    # painting.image.save(os.path.join(SOURCE_IMG_PATH, '1.jpg'))
    os.system('echo "loh"')
    # os.system(f'python main.py --base configs/latent-diffusion/txt2img-1p4B-finetune.yaml -t --actual_resume models/ldm/text2img-large/model.ckpt -n tmp --gpus 0, --data_root {SOURCE_IMG_PATH} --init_word "painting"')

if __name__ == '__main__':
    # import wikiart
    # oscar = wikiart.load_artist('vincent-van-gogh')
    # invert(oscar[0])
    invert(5)
