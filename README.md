# AI4Micro (AIM) 预考核 —— 环境配置说明

Welcome!  Follow these steps **before exam day** so you have a clean, identical Python 3.10+ workspace with JupyterLab, NumPy, pandas, and Matplotlib.

同学们大家好啊！ 请在开始考试前按照以下步骤在自己的电脑上配置好Python编程环境，包括Python 3.10或更高版本以及最新的JupyterLab, NumPy, pandas, 和Matplotlib.

---

## 1  Install Miniconda (recommended) 安装Miniconda（这是个好东西！）

👉 Already have Anaconda?  Skip to the section 2 – the commands work the same. 

👉 如果已经安装了Anaconda/Miniconda，请忽略以下内容直奔第二部分的环境配置。

1. Visit the official [**Miniconda download page**](https://www.anaconda.com/download/success) and grab the installer that matches your OS (Windows x86‑64, macOS arm64/intel, or Linux). 请从以上链接中下载适配个人笔记本和操作系统的Miniconda安装包，需注意CPU架构适配性。

2. Run the installer with *default options*.
   - **macOS/Linux:**
     ```bash
     bash Miniconda3-latest-Linux-x86_64.sh   # or the macOS installer
     ```
     从terminal中运行以下脚本，或者直接下载macOS适配的*.pkg*安装包并手动安装。
   - **Windows:** double‑click the `.exe` file.
     直接下载安装包既可
     
3. Finish *conda* installation 完成安装.
   - **macOS/Linuex:**
     Close and reopen your terminal. 重启Terminal
   - **Windows:**
     Start the *Anaconda Prompt* or *Anaconda Powershell* 找到并启动Anaconda Prompt或Anaconda Powershell.
     
4. Confirm Conda is on your PATH 输入以下指令确认安装成功:
   ```bash
   conda --version
   ```
   Expected output:
   ```bash
   conda 24.3.0 #or something alike
   ```
---

## 2  Create the exam environment 创建考试用Python虚拟环境

Activate a fresh environment called py_exam 创建并激活一个本地虚拟环境py_exam

*This will usually take a couple minutes, be patient. 环境解析需要点时间，莫着急*
```bash
conda create -n py_exam python=3.10 numpy pandas matplotlib scikit-learn jupyterlab ipywidgets -c conda-forge -y
```
Now activate the virtual environment 让虚拟环境活过来吧！
```bash
conda activate py_exam
```
---

## 3  Install any extra packages with **pip** 利用**pip**安装其他可能用到的Python工具

After *activating* the environment you may use pip as usual – the packages will live **inside** `py_exam`:

在虚拟环境用*pip*安装的Python包仅能在虚拟环境py_exam中调用

```bash
pip install seaborn scikit-image  
```
Note that these are just examples to demonstrate *pip* usage, they are not required for the exam

上述代码对于考试不是必须的，但安装上好像也没啥坏处。

---

## 4  Clone or download the github repo 克隆或下载github答题包

If you have git installed, you may simply pull the repo using the following command:
```bash
git clone https://github.com/jzrolling/py_exam_2025.git
```
You can also go to the GitHub page, click **Code ▶ Download ZIP**, and unzip it locally. 

---

## 5  Launch JupyterLab 启动JupyterLab

```bash
jupyter lab --notebook-dir="D:/path-to-exam" 
```
Replace the "D:/py_exam_2025" to where the exam content directory is located. 

将"D:/py_exam_2025"替换成考试内容文件夹路径

Open **AI4M_notebook.ipynb** and follow the instructions to complete the test.

点开答题notebook，根据引导完成答题。

---

## 6  Deactivate the virtual environment (after the course) 考试结束后关闭虚拟环境

```bash
conda deactivate
```

---

*Happy coding!*

*码上快乐!*

