from setuptools import setup, find_packages

setup(
    name="failure-aware-ml-system",
    version="1.0.0",
    description="Failure-aware, human-in-the-loop ML system across OCR, medical imaging, and video",
    author="Aman Bharadwaj",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "pillow",
        "torch",
        "torchvision",
        "pytesseract",
        "pyyaml",
        "scikit-learn",
        "tqdm"
    ],
    python_requires=">=3.8",
)
