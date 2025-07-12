# DSResSol Environment Installation Guide

This guide describes how to set up the DSResSol environment on a Linux or cloud VM (e.g., Google Cloud Platform).

## Prerequisites
- Linux-based system (tested on Ubuntu 20.04/GCP VM)
- [Anaconda/Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed
- Python 3.7+ supported
- (Optional) NVIDIA GPU drivers and CUDA 10.1 for GPU acceleration

## Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/dnnunn/DSResSol.git
   cd DSResSol
   ```

2. **Ensure the Cleaned environment.yml is Present**
   - The `environment.yml` should NOT contain any Windows- or Intel-specific dependencies.
   - If you updated the repo, pull the latest changes:
     ```bash
     git pull
     ```

3. **Create the Conda Environment**
   ```bash
   conda env create -f environment.yml
   ```

4. **Activate the Environment**
   ```bash
   conda activate DsResSol
   ```

5. **Run DSResSol**
   - For sequence-only model:
     ```bash
     python main.py --sequence_only
     ```
   - For sequence + biological features model:
     ```bash
     python main.py
     ```

6. **Testing Peptides**
   - Open Jupyter in the `Most accurate models` directory:
     ```bash
     jupyter notebook
     ```
   - Open `test.ipynb` and follow the instructions to test your peptides.

## Troubleshooting
- If you see `PackagesNotFoundError`, check `environment.yml` for any platform-specific build strings or Windows/Intel-only dependencies and remove them.
- If you need GPU support, ensure your VM has compatible NVIDIA drivers and CUDA installed.
- For further help, contact the maintainer or open an issue on GitHub.

---

## Additional Manual Changes
- All platform-specific lines and duplicate dependencies have been removed from `environment.yml`.
- Both `prefix:` lines have been deleted for portability.
- See `CHANGELOG.md` for a summary of all environment and setup changes.
