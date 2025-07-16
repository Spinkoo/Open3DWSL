# Open3D GPU Build on Windows (WSL) – Install Guide

Do you need to build Open3D from source with GPU support on Windows? I suppose you have your reasons the same way I did when I was navigating through forums to solve the issue.

Ideally, you would install it on WSL (Ubuntu) for maximum support, which you could use later on for your Python virtual environment to run your codes.

# Let's get started! :D

---

## 1. Update and Upgrade

```bash
sudo apt update
sudo apt upgrade
```

---

## 2. Install Python

```bash
sudo apt install python3
sudo apt install --reinstall python3-pip
sudo apt install python3-env
```
---


## 3. Install C Compilers

```bash
sudo apt install g++-11
sudo apt install clang-15 libc++-15-dev libc++abi-15-dev
sudo apt install gcc
```

---

## 4. Install CUDA 12.4 (with toolkit option checked)

```bash
mkdir cuda && cd cuda
wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux.run
sudo sh cuda_12.4.1_550.54.15_linux.run
```

Add CUDA to your path:

```bash
export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

---

## 5. Check CUDA Tools

```bash
which cicc
# if cicc is not found:
sudo ln -s /usr/local/cuda-12.4/nvvm/bin/cicc /usr/bin/cicc

nvcc --version
# Should report 12.4 or similar

which ptxas
ptxas --version
# Should also be 12.x
# if it fails:
sudo ln -s /usr/local/cuda-12.4/bin/ptxas /usr/bin/ptxas
```

---

## 6. Install CMake

You could either install a recent version of CMake or download the already tested v3.29.3 (stable on WSL).

To use CMake locally:

```bash
mkdir cmake_build && cd cmake_build
wget https://github.com/Kitware/CMake/releases/download/v3.29.3/cmake-3.29.3-linux-x86_64.tar.gz
mkdir -p ~/opt && tar -xzf cmake-3.29.3-linux-x86_64.tar.gz -C ~/opt
echo 'export PATH=$HOME/opt/cmake-3.29.3-linux-x86_64/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Check version:

```bash
cmake --version
# should print cmake version 3.29.3
```

---

## 7. Install essentials

```bash
sudo apt install libglew-dev libxkbcommon-dev xorg-dev libglu1-mesa-dev ibwayland-dev

```

---

## 8. Build Open3D from Source

```bash
git clone https://github.com/isl-org/Open3D && cd Open3D
mkdir build && cd build
```

---

### CUDA Architecture Table

| SM Version | GPU Family      | Examples                        |
|------------|----------------|---------------------------------|
| sm_75      | Turing         | RTX 2080, RTX 2070, T4          |
| sm_86      | Ampere         | RTX 30xx series (3080, 3090)    |
| sm_89      | Ada Lovelace   | RTX 40xx series (4080, 4090)    |
| sm_80      | A100 (datacenter GPU) | NVIDIA A100           |

- For sm_75 use the flag: `CMAKE_CUDA_ARCHITECTURES="75"`
- For multiple builds (e.g., sm_75 and 86): `CMAKE_CUDA_ARCHITECTURES="75;86"`

---

## 9. CMake Build Command

```bash
cmake -DBUILD_CUDA_MODULE=ON -DBUILD_PYTHON_MODULE=ON -DPYTHON_EXECUTABLE=$(which python) -D CUDA_TOOLKIT_ROOT_DIR="/usr/local/cuda-12.4" -DCMAKE_INSTALL_PREFIX=~/open3d_install -D CUDA_TOOLKIT_ROOT_DIR="/usr/local/cuda-12.4" -D CMAKE_CUDA_ARCHITECTURES="86;89" -DBUILD_GUI=ON -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.4/bin/nvcc ..
```

---

## 10. Build

> Either limit the number of jobs or increase the WSL swap memory

```bash
make -j2
```
---

## 11. Create Virtual Environment

```bash
python3 -m venv <env-name>
source env-name/bin/activate
```
---
## 12. Make the pip wheel & install it
Once the build is complete and you are inside your python virtual environment, run 
```
make install-pip-package
```
## 13. Minimalist test to check cuda :
```
python -c "import open3d; print(open3d.core.cuda.is_available())"
```

 > Check the [sample](/test.py) for basic usage
