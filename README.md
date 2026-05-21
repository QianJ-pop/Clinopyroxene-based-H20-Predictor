# Clinopyroxene H₂O Prediction Model

This repository provides the data, pretrained model weights, and online prediction platform associated with our machine-learning clinopyroxene hygrometer.

The model predicts initial clinopyroxene H₂O contents with high accuracy:

- **R² = 0.873**
- **Mean absolute error = 35.7 ppm**
---

## Online Prediction Platform

The online prediction website is available at:

http://47.82.216.229:8000/

Users can input clinopyroxene major-element compositions and obtain predicted initial clinopyroxene H₂O contents.

---

## Data Availability

The compiled clinopyroxene dataset used in this study is publicly released with this project.

The released data include:

- Clinopyroxene major-element compositions
- Measured or reference H₂O contents
- Sample and tectonic-setting information where available
- Data used for model training, validation, and testing

---

## Model Weights

Pretrained model weight files are publicly released with this project.

These weights allow users to reproduce the prediction results and apply the trained clinopyroxene H₂O prediction model to new clinopyroxene compositions.

The fitted TabPFN model file is provided in the `models/` directory.

Example model file:

```text
models/last_water1.tabpfn_fit
```

---

## Training Code Availability

The full training code will be released after the associated manuscript is accepted.

Before acceptance, this repository provides the public dataset, pretrained model weights, and online prediction platform to support model use, testing, and reproducibility of the reported predictions.

---

## Suggested Use

This model is designed for estimating initial clinopyroxene H₂O contents from clinopyroxene compositions, especially in cases where measured H₂O contents may have been modified by diffusion during magma ascent, eruption, or cooling.

Potential applications include:

- Reconstruction of primary clinopyroxene H₂O contents
- Estimation of melt H₂O contents from clinopyroxene records
- Evaluation of mantle hydration beneath different tectonic settings
- Investigation of deep-Earth water cycling using mineral archives

---

## Local Model Usage

Users can also run the pretrained clinopyroxene H₂O prediction model locally using Python.

### Installation

Install the required Python packages:

```bash
pip install tabpfn pandas
```

If GPU acceleration is available, users may run the model with CUDA. Otherwise, the model can be loaded on CPU.

---

### Load the pretrained model

```python
from tabpfn.model_loading import load_fitted_tabpfn_model

# Load the fitted TabPFN regression model
regressor = load_fitted_tabpfn_model(
    "models/last_water1.tabpfn_fit",
    device="cuda"   # change to "cpu" if CUDA is not available
)
```

---

### Predict new clinopyroxene H₂O contents

```python
import pandas as pd
from tabpfn.model_loading import load_fitted_tabpfn_model

# Load the fitted model
regressor = load_fitted_tabpfn_model(
    "models/last_water1.tabpfn_fit",
    device="cuda"   # use "cpu" if CUDA is not available
)

# Load new clinopyroxene compositions
X_new = pd.read_csv("example_input.csv")

# Predict initial clinopyroxene H₂O contents
predicted_h2o = regressor.predict(X_new)

# Save prediction results
output = X_new.copy()
output["Predicted_H2O_ppm"] = predicted_h2o
output.to_csv("prediction_results.csv", index=False)

print(output)
```

---

## TabPFN Documentation

This model was implemented using TabPFN.

For more information about TabPFN, please refer to the official repository:

https://github.com/PriorLabs/TabPFN

---

## Citation

Please cite the associated manuscript when using the dataset, model weights, online prediction platform, or prediction results.

Citation information will be updated after publication.

---

## Contact

For questions about the dataset, model, or online prediction platform, please contact the corresponding author of the associated manuscript.
