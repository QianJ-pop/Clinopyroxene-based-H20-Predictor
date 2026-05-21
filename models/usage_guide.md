# Clinopyroxene H₂O Prediction: Excel Usage Guide

This document describes how to use `predict_excel.py` to predict initial clinopyroxene H₂O contents from an Excel file using the pretrained model:

```text
models/last_water1.tabpfn_fit
```

---

## 1. Install Dependencies

Before running the prediction script, install the required Python packages:

```bash
pip install pandas openpyxl pydantic tabpfn
```

The required packages are:

- `pandas`: reading, processing, and saving tabular data
- `openpyxl`: reading and writing Excel files
- `pydantic`: validating input variables
- `tabpfn`: loading and running the pretrained TabPFN model

---

## 2. Required Excel Input Format

The input Excel file must contain complete clinopyroxene major-element compositions.

The following column names are required and must be exactly the same:

```text
SiO2, TiO2, Al2O3, Cr2O3, FeO, MnO, MgO, CaO, Na2O, K2O, NiO
```

Each row should represent one clinopyroxene analysis.

All oxide values should be given in wt.%.

Example:

| SiO2 | TiO2 | Al2O3 | Cr2O3 | FeO | MnO | MgO | CaO | Na2O | K2O | NiO |
|---|---|---|---|---|---|---|---|---|---|---|
| 51.20 | 0.62 | 4.35 | 0.15 | 6.80 | 0.18 | 15.40 | 20.10 | 0.55 | 0.01 | 0.03 |

---

## 3. Important Requirement

The current script assumes that the Excel file contains complete major-element compositions.

Missing values are not automatically filled in this example script.

If missing values are present, users should either:

1. provide complete clinopyroxene compositions, or
2. apply the same preprocessing workflow used during model training.

Do not fit a new KNN imputer on the prediction dataset unless this is explicitly intended, because this would make the prediction workflow inconsistent with the training workflow.

---

## 4. Run Prediction on CPU

Use the following command if running on a normal computer or server without GPU acceleration:

```bash
python examples/predict_excel.py \
  --input data/example_input.xlsx \
  --output results/prediction_results.xlsx \
  --model models/last_water1.tabpfn_fit \
  --device cpu
```

---

## 5. Run Prediction on CUDA GPU

If CUDA is available, the model can be loaded on GPU:

```bash
python examples/predict_excel.py \
  --input data/example_input.xlsx \
  --output results/prediction_results.xlsx \
  --model models/last_water1.tabpfn_fit \
  --device cuda
```

---

## 6. Output File

The output Excel file will be saved to:

```text
results/prediction_results.xlsx
```

The output file contains the original input table plus two new columns:

```text
Mg#
Predicted_H2O_ppm
```

Where:

- `Mg#` is calculated from the structural formula of clinopyroxene.
- `Predicted_H2O_ppm` is the predicted initial clinopyroxene H₂O content in ppm.

---

## 7. Example Project Structure

A typical project structure is:

```text
Clinopyroxene-H2O-Prediction/
│
├── models/
│   └── last_water1.tabpfn_fit
│
├── data/
│   └── example_input.xlsx
│
├── examples/
│   └── predict_excel.py
│
└── results/
    └── prediction_results.xlsx
```

---

## 8. Notes

- The input column names must match the required names exactly.
- Oxide concentrations should be reported in wt.%.
- The model file should be located at `models/last_water1.tabpfn_fit`, unless another path is provided using the `--model` argument.
- Use `--device cpu` if CUDA is not available.
- Use `--device cuda` only when a CUDA-compatible GPU and the required CUDA environment are available.
