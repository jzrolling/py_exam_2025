# AI4Micro (AIM) Entry Exam – Environment Setup Guide
# AI4Micro (AIM) 预考核 —— 环境配置说明

Welcome!  Follow these steps **before exam day** so you have a clean, identical Python 3.10+ workspace with JupyterLab, NumPy, pandas, and Matplotlib.
同学们大家好啊！ 请在开始考试前按照以下步骤在自己的电脑上配置好Python编程环境，包括Python 3.10或更高版本以及最新的JupyterLab, NumPy, pandas, 和Matplotlib.

---

## 1  Install Miniconda (recommended)

1. Visit the official [**Miniconda download page**](https://docs.conda.io/en/latest/miniconda.html) and grab the installer that matches your OS (Windows x86‑64, macOS arm64/intel, or Linux).
2. Run the installer with *default options*.
   - **macOS/Linux:**
     ```bash
     bash Miniconda3-latest-Linux-x86_64.sh   # or the macOS installer
     ```
   - **Windows:** double‑click the `.exe` file.
3. Close and reopen your terminal (or start the *Anaconda Prompt* on Windows).
4. Confirm Conda is on your PATH:
   ```bash
   conda --version   # should print something like "conda 24.3.0"
   ```

👉 Already have Anaconda?  Skip to the next section – the commands work the same.

---

## 2  Create the exam environment

```bash
# create + activate a fresh environment called py_exam
conda create -n py_exam python=3.10 \
  numpy pandas matplotlib scikit-learn jupyterlab ipywidgets -c conda-forge -y
conda activate py_exam
```

- `python=3.10` ensures everyone uses the same interpreter.
- `-c conda-forge` pulls the latest, cross‑platform binaries.
- `ipywidgets` lets the notebook render multiple‑choice widgets without extra extensions.

### Optional: enable the fast solver

```bash
conda install -n base conda-libmamba-solver -y
conda config --set solver libmamba
```

This typically cuts environment‑solve time from minutes to seconds.

---

## 3  Install any extra packages with **pip**

After *activating* the environment you may use pip as usual – the packages will live **inside** `py_exam`:

```bash
pip install seaborn plotly  # examples only – not required for the exam
```

> **Tip:** Use `python -m pip install …` if you have multiple Python versions on your system.

---

## 4  Launch JupyterLab

```bash
jupyter lab   # Opens http://localhost:8888/lab in your browser
```

Place the exam repository in any folder and open the notebook from the left sidebar.

---

## 5  Verify everything works

Inside a new notebook or Python prompt run:

```python
import sys, platform, numpy, pandas, matplotlib, sklearn
print(platform.python_version())
print(numpy.__version__, pandas.__version__, matplotlib.__version__, sklearn.__version__)
```

If you see the version numbers without errors you are ready for the exam.

---

## 6  Troubleshooting

| Symptom                      | Fix                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| `conda: command not found`   | Open a **new** terminal after install; or run `conda init` then restart your shell. |
| `jupyter: command not found` | Make sure the `py_exam` environment is activated.                                   |
| Solver hangs                 | Install the *libmamba* solver (see above).                                          |

---

## 7  Cleaning up (after the course)

```bash
conda deactivate
conda remove -n py_exam --all
```

---

*Happy coding!*

