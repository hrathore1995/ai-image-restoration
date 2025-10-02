# AI Image Restoration Project

## Project Goal

The goal of this project is to **restore damaged or degraded images** using two different approaches:

1. **Traditional Image Processing methods (OpenCV-based)**
2. **Deep Learning-based Inpainting models (Stable Diffusion with OpenCV masks)**

We aimed to study both approaches in terms of:

* **Quantitative metrics** (PSNR, SSIM, etc.)
* **Qualitative evaluation** (visual appeal of restored images)
* **Practical usability** via a simple **web application** where users can upload damaged images and get restored outputs.

---

### The paintings of famous Italian painter Sebastiano Ricci is taken for restoration

## Traditional vs Deep Learning Models

### Traditional Image Restoration

We used OpenCV-based techniques like:

* **Inpainting with Telea’s algorithm**
* **Navier-Stokes inpainting**

**Pros:**

* Fast to run, low resource requirements
* Performs well on small cracks, scratches, and minor defects
* Quantitative metrics (PSNR/SSIM) are often **higher** than deep learning methods, meaning they preserve original pixels better.

**Cons:**

* Struggles with larger missing regions
* Cannot generate realistic textures
* Limited to “filling in” based on surrounding pixels

---

### Deep Learning Restoration (Stable Diffusion Inpainting)

We used **Stable Diffusion Inpainting (runwayml/stable-diffusion-inpainting)** along with **automatic damage mask generation using OpenCV (thresholding + morphology)**.

**Pros:**

* Capable of hallucinating realistic missing parts
* Produces visually appealing results for **old photos and large missing regions**
* Strong qualitative performance (images “look” much better after restoration)

**Cons:**

* Requires GPU, heavy on resources
* Slower inference compared to OpenCV
* Sometimes produces NSFW false positives (requires filtering)

---

## Why Traditional Models Score Higher in Metrics but Look Worse

* **Traditional methods** try to **preserve pixels** as close to original as possible → higher similarity metrics (PSNR, SSIM).
* **Deep Learning models** focus on **visual plausibility** instead of pixel similarity → lower metrics, but better **human perception**.

In short:

* Traditional = “Numerically good, visually boring”
* Deep Learning = “Numerically weaker, visually stunning”

---

## Project Structure

```
ai_image_restoration/
│── src/
│   ├── app.py              # FastAPI backend
│   ├── restore.py          # Image restoration logic
│   ├── mask_pipeline.py    # Automatic mask detection (OpenCV thresholding)
│   ├── __init__.py
│
│── frontend/ (UI)
│   ├── index.html
│   ├── 
│       ├── styles.css
│       ├── script.js
│
│── models/                 # Pretrained weights (if any in future)
│── temp/                   # Uploaded + restored images
│── README.md               # Documentation
│── requirements.txt
```

---

## Web Application

We built a **FastAPI-based web app** with a lightweight frontend:

* **Upload damaged image**
* **Automatic mask generation** (defects detected with Dalle 2)
* **Get restored output** displayed back in browser

UI Features:

* Loader animation during restoration
* Disabled button while processing

---

## How to Run

### 1. Clone Repo & Setup

```bash
git clone <repo-url>
cd ai_image_restoration
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Backend

```bash
uvicorn src.app:app --reload
```

### 3. Open Frontend

Go to [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 4. Upload an image & wait for restoration

---

## Example Results

You can see how the **traditional models and deep learning models** have restored images in the provided Jupyter Notebooks.

### Restored images

**Traditional (Telea Inpainting):**

![Traditional](results/traditional/Ca'_Rezzonico_-_Resurrezione_di_Cristo_(Inv.101)_-_Sebastiano_Ricci_telea_4.jpg)

**Deep Learning (Stable Diffusion):**

![DeepLearning](results/deep/Ca'_Rezzonico_-_Resurrezione_di_Cristo_(Inv.101)_-_Sebastiano_Ricci_sdxl_2.jpg)

---

## Demo video
Click the demo below to watch the demo

[![Watch the demo](https://img.youtube.com/vi/MuWb66dsZD8/0.jpg)](https://youtu.be/MuWb66dsZD8)


---

## Future Improvements

* Support multiple restoration prompts ("restore old film photo", "remove watermarks")
* Add user control for choosing restoration method
* Improve mask detection by integrating pretrained deep learning segmentation models like U²-Net in the future
* Deploy as a cloud-hosted service

---

## Conclusion

This project demonstrates the **trade-off between traditional and deep learning methods**:

* Traditional = numerically better, resource-light, but visually limited
* Deep Learning = visually compelling, handles complex cases, but heavier and slower

Our web app bridges both worlds by giving users an intuitive way to restore old/damaged images.
