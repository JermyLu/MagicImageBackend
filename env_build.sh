# 默认环境为linux,  安装conda & 构建项目运行conda虚拟环境
wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
bash Anaconda3-2020.07-Linux-x86_64.sh
source ~/.bashrc
# 检查是否安装成功
conda -V
# 构建项目运行conda虚拟环境
env_name="magicImage"
conda create --name $env_name python=3.10
conda activate $env_name

# conda安装pyTorch
# 注意: 当前环境cuda最高支持11.0, 可在https://pytorch.org/get-started/previous-versions/查询你的cuda对应的pyTorch版本
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c pytorch
packages=(tensorflow==2.11.0 diffusion transformers accelerate diffusers modelscope fastapi uvicorn numba easydict gradio opencv-python CMake face_recognition)
for package in ${packages[*]}
do
    pip install $package -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
done

echo "run-env build successfully!"
