conda env create -f environment.yaml
conda activate ldm

mkdir -p models/ldm/text2img-large/
wget -O models/ldm/text2img-large/model.ckpt https://ommer-lab.com/files/latent-diffusion/nitro/txt2img-f8-large/model.ckpt

conda install -c conda-forge kaggle
touch ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

mkdir datasets
gsutil cp gs://wikiart_op/wikiart.tar datasets
tar xvf datasets/wikiart.tar datasets
rm datasets/wikiart.tar
