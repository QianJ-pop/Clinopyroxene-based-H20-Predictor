# examples/predict_excel.py
# -*- coding: utf-8 -*-

"""
Batch prediction script for the clinopyroxene H2O prediction model.

This script:
1. Reads clinopyroxene major-element compositions from an Excel file.
2. Calculates cations based on 6 oxygens.
3. Calculates Mg#.
4. Builds the 23-dimensional model input.
5. Loads the fitted TabPFN model: models/last_water1.tabpfn_fit
6. Predicts initial clinopyroxene H2O contents.
7. Saves the results to a new Excel file.

Required input columns:
SiO2, TiO2, Al2O3, Cr2O3, FeO, MnO, MgO, CaO, Na2O, K2O, NiO
"""

from pathlib import Path
import argparse

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from tabpfn.model_loading import load_fitted_tabpfn_model


# If this file is saved in examples/, BASE_DIR points to the project root.
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 1. Single-sample input schema
# ============================================================

class CpxInput(BaseModel):
    SiO2: float = Field(..., description="SiO2 (wt.%)")
    TiO2: float = Field(..., description="TiO2 (wt.%)")
    Al2O3: float = Field(..., description="Al2O3 (wt.%)")
    Cr2O3: float = Field(..., description="Cr2O3 (wt.%)")
    FeO: float = Field(..., description="FeO (wt.%)")
    MnO: float = Field(..., description="MnO (wt.%)")
    MgO: float = Field(..., description="MgO (wt.%)")
    CaO: float = Field(..., description="CaO (wt.%)")
    Na2O: float = Field(..., description="Na2O (wt.%)")
    K2O: float = Field(..., description="K2O (wt.%)")
    NiO: float = Field(..., description="NiO (wt.%)")


# ============================================================
# 2. Predictor class
# ============================================================

class CpxH2OPredictor:
    """
    Clinopyroxene H2O predictor using a fitted TabPFN model.

    Model input variables:
    11 oxide wt.% variables
    + 11 cation variables based on 6 oxygens
    + Mg#
    = 23 input variables
    """

    oxide_columns = [
        "SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO",
        "MnO", "MgO", "CaO", "Na2O", "K2O", "NiO"
    ]

    structural_columns = [
        "Si", "Ti", "Al", "Cr", "Fe",
        "Ca", "Mg", "Mn", "Ni", "K", "Na"
    ]

    model_columns = oxide_columns + structural_columns + ["Mg#"]

    def __init__(self, model_path: str | Path | None = None, device: str = "cpu"):
        if model_path is None:
            model_path = BASE_DIR / "models" / "last_water1.tabpfn_fit"

        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.model = load_fitted_tabpfn_model(
            str(model_path),
            device=device
        )

    # ===============================
    # Check input columns
    # ===============================
    @classmethod
    def _check_input_columns(cls, df: pd.DataFrame) -> None:
        missing_cols = [col for col in cls.oxide_columns if col not in df.columns]

        if missing_cols:
            raise ValueError(
                "Missing required columns in the input Excel file: "
                + ", ".join(missing_cols)
            )

    # ===============================
    # wt.% → 6 O structural formula
    # ===============================
    @staticmethod
    def _compute_structural_formula(df: pd.DataFrame) -> pd.DataFrame:
        molar_mass = {
            "SiO2": 60.0843,
            "TiO2": 79.8658,
            "Al2O3": 101.9982,
            "Cr2O3": 151.997,
            "FeO": 71.8444,
            "MnO": 70.9374,
            "MgO": 40.3044,
            "CaO": 56.0774,
            "Na2O": 61.9788,
            "K2O": 94.196,
            "NiO": 74.6894,
        }

        a = df["SiO2"] / molar_mass["SiO2"]
        b = df["TiO2"] / molar_mass["TiO2"]
        c = df["Al2O3"] / molar_mass["Al2O3"]
        d = df["Cr2O3"] / molar_mass["Cr2O3"]
        e = df["FeO"] / molar_mass["FeO"]
        f = df["MnO"] / molar_mass["MnO"]
        g = df["MgO"] / molar_mass["MgO"]
        h = df["CaO"] / molar_mass["CaO"]
        i = df["Na2O"] / molar_mass["Na2O"]
        j = df["K2O"] / molar_mass["K2O"]
        k = df["NiO"] / molar_mass["NiO"]

        oxygen_sum = (
            2 * a + 2 * b + 3 * c + 3 * d +
            e + f + g + h +
            2 * i + 2 * j + k
        )

        if (oxygen_sum <= 0).any():
            raise ValueError("Invalid oxide composition: oxygen sum must be positive.")

        factor = 6.0 / oxygen_sum

        struct_df = pd.DataFrame({
            "Si": a * factor,
            "Ti": b * factor,
            "Al": c * 2 * factor,
            "Cr": d * 2 * factor,
            "Fe": e * factor,
            "Mn": f * factor,
            "Mg": g * factor,
            "Ca": h * factor,
            "Na": i * 2 * factor,
            "K": j * 2 * factor,
            "Ni": k * factor,
        })

        return struct_df

    # ===============================
    # Mg#
    # ===============================
    @staticmethod
    def _compute_mg_number(struct_df: pd.DataFrame) -> pd.Series:
        denominator = struct_df["Mg"] + struct_df["Fe"]

        if (denominator <= 0).any():
            raise ValueError("Invalid composition: Mg + Fe must be positive.")

        return struct_df["Mg"] / denominator * 100.0

    # ===============================
    # Build model input from DataFrame
    # ===============================
    def _build_model_input_from_df(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        self._check_input_columns(df)

        wt_df = df[self.oxide_columns].copy()

        # Convert input oxide columns to numeric values.
        for col in self.oxide_columns:
            wt_df[col] = pd.to_numeric(wt_df[col], errors="coerce")

        # Check missing values.
        if wt_df.isna().any().any():
            rows_with_nan = wt_df[wt_df.isna().any(axis=1)].index.tolist()
            raise ValueError(
                "Missing or non-numeric values were found in oxide columns. "
                f"Problematic row indices: {rows_with_nan[:20]}"
            )

        # Check negative values.
        if (wt_df < 0).any().any():
            rows_with_negative = wt_df[(wt_df < 0).any(axis=1)].index.tolist()
            raise ValueError(
                "Negative oxide values were found. "
                f"Problematic row indices: {rows_with_negative[:20]}"
            )

        struct_df = self._compute_structural_formula(wt_df)
        mg_number = self._compute_mg_number(struct_df)

        X_df = pd.concat(
            [
                wt_df.reset_index(drop=True),
                struct_df[self.structural_columns].reset_index(drop=True),
                mg_number.reset_index(drop=True).rename("Mg#"),
            ],
            axis=1
        )

        X_df = X_df[self.model_columns]

        return X_df, mg_number

    # ===============================
    # Predict from DataFrame
    # ===============================
    def predict_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        X_df, mg_number = self._build_model_input_from_df(df)

        prediction = self.model.predict(X_df.values)

        output = df.copy()
        output["Mg#"] = mg_number.values
        output["Predicted_H2O_ppm"] = prediction

        return output

    # ===============================
    # Predict from Excel
    # ===============================
    def predict_excel(
        self,
        input_excel: str | Path,
        output_excel: str | Path,
        sheet_name=0,
    ) -> pd.DataFrame:
        input_excel = Path(input_excel)
        output_excel = Path(output_excel)

        if not input_excel.exists():
            raise FileNotFoundError(f"Input Excel file not found: {input_excel}")

        df = pd.read_excel(input_excel, sheet_name=sheet_name)

        output = self.predict_dataframe(df)

        output_excel.parent.mkdir(parents=True, exist_ok=True)
        output.to_excel(output_excel, index=False)

        return output


# ============================================================
# 3. Command-line usage
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Predict initial clinopyroxene H2O contents from an Excel file."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input Excel file, e.g., data/example_input.xlsx"
    )

    parser.add_argument(
        "--output",
        default=str(BASE_DIR / "results" / "prediction_results.xlsx"),
        help="Path to output Excel file."
    )

    parser.add_argument(
        "--model",
        default=str(BASE_DIR / "models" / "last_water1.tabpfn_fit"),
        help="Path to fitted TabPFN model file."
    )

    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device used for prediction."
    )

    parser.add_argument(
        "--sheet-name",
        default=None,
        help="Excel sheet name. If not provided, the first sheet is used."
    )

    args = parser.parse_args()

    sheet_name = 0 if args.sheet_name is None else args.sheet_name

    predictor = CpxH2OPredictor(
        model_path=args.model,
        device=args.device
    )

    output = predictor.predict_excel(
        input_excel=args.input,
        output_excel=args.output,
        sheet_name=sheet_name,
    )

    print("Prediction completed.")
    print(f"Input Excel:  {args.input}")
    print(f"Output Excel: {args.output}")
    print(f"Number of samples: {len(output)}")
    print(output[["Mg#", "Predicted_H2O_ppm"]].head())


if __name__ == "__main__":
    main()