# Clinopyroxene H₂O Prediction Model

This repository provides the data, pretrained model weights, and online prediction platform associated with our machine-learning clinopyroxene hygrometer.

Clinopyroxene is widely used to infer magmatic and mantle H₂O contents, but its water record is commonly reset during magma ascent, eruption, and cooling, which can compromise its reliability as a recorder of primary hydrous conditions. In this study, we compiled a global dataset of 1,855 clinopyroxene analyses from mafic rocks and trained a machine-learning model to predict initial clinopyroxene H₂O contents from mineral compositions.

The model predicts initial clinopyroxene H₂O contents with high accuracy:

- **R² = 0.873**
- **Mean absolute error = 35.7 ppm**

Compared with conventional regression algorithms, the model performs particularly well for sparsely sampled high-H₂O compositions. It can also restore plausible melt H₂O contents for diffusion-modified clinopyroxenes from plume-related, intraplate, and ocean-island basalt systems.

These results indicate that water contributes substantially to melt generation across diverse tectonic settings, while cooling history influences the extent to which primary hydrous signals can be experimentally recovered. This work establishes a quantitative, composition-based hygrometer for clinopyroxene and broadens the mineral archive available for reconstructing mantle hydration and deep-Earth water cycling.

## Online Prediction Platform

The online prediction website is available at:

http://47.82.216.229:8000/

Users can input clinopyroxene major-element compositions and obtain predicted initial clinopyroxene H₂O contents.

## Data Availability

The compiled clinopyroxene dataset used in this study is publicly released with this project.

The released data include:

- Clinopyroxene major-element compositions
- Measured or reference H₂O contents
- Sample and tectonic-setting information where available
- Data used for model training, validation, and testing

## Model Weights

Pretrained model weight files are publicly released with this project.

These weights allow users to reproduce the prediction results and apply the trained clinopyroxene H₂O prediction model to new clinopyroxene compositions.

## Training Code Availability

The full training code will be released after the associated manuscript is accepted.

Before acceptance, this repository provides the public dataset, pretrained model weights, and online prediction platform to support model use, testing, and reproducibility of the reported predictions.

## Suggested Use

This model is designed for estimating initial clinopyroxene H₂O contents from clinopyroxene compositions, especially in cases where measured H₂O contents may have been modified by diffusion during magma ascent, eruption, or cooling.

Potential applications include:

- Reconstruction of primary clinopyroxene H₂O contents
- Estimation of melt H₂O contents from clinopyroxene records
- Evaluation of mantle hydration beneath different tectonic settings
- Investigation of deep-Earth water cycling using mineral archives

## Citation

Please cite the associated manuscript when using the dataset, model weights, online prediction platform, or prediction results.

Citation information will be updated after publication.

## Contact

For questions about the dataset, model, or online prediction platform, please contact the corresponding author of the associated manuscript.
