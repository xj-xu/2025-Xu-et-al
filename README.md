# 2025-Xu-et-al
# Distinct impact of PI(4)P flux in regulating PI(4,5)P$_2$ steady states and oscillations

This repository contains data, code, and analysis supporting our manuscript:

> **Title:** _Distinct impact of PI(4)P flux in regulating PI(4,5)P$_2$ steady states and oscillations_  
> **Authors:** [XJ Xu], [Chee San Tong], [Min Wu].  
> **Status:** Submitted to *Journal*  
> **Preprint:** [arXiv link (if available)]

---

## 🔬 Summary

Phosphatidylinositol 4,5-bisphosphate [PI(4,5)P₂] is a key signaling lipid that defines the inner leaflet of the eukaryotic plasma membrane. Although PI(4)P is its canonical precursor, previous studies showed that PI(4,5)P₂ levels remain unexpectedly robust under PI(4)P depletion.

Using live-cell TIRF microscopy in RBL mast cells, we discovered:
- First discovery of **periodic traveling waves of PI(4)P** at the plasma membrane, challenging the assumption that precursor lipids exist only in steady state.
- **Critical**rate of PI(4)P synthesis required for oscillations in both PI(4,5)P₂ and active **Cdc42**, a regulator of the actin cytoskeleton.
- **Quantitative insights** into lipid-driven cortical dynamics, pointing to a dynamical-systems view of membrane identity.

---

## 📁 Repository Structure
project-root/
├── data/               # Raw and processed TIRF image data
├── scripts/            # Image analysis and quantification scripts (Python / MATLAB)
├── figures/            # Final and intermediate figure panels
├── notebooks/          # Jupyter notebooks for reproducing key analyses
├── environment.yml     # Conda environment for dependencies
└── README.md           # This file

---

## ⚙️ Requirements

To reproduce the analysis:

- Python 3.8+
- `numpy`, `scipy`, `matplotlib`, `pandas`, `scikit-image`, `tifffile`
- (optional) MATLAB R2020a+ for specific analysis scripts

Create a conda environment:
```bash
conda env create -f environment.yml
conda activate pip2-waves



This work is licensed under the MIT License.
For questions or feedback, please contact:
[Your Name] — [your.email@yale.edu]

If you use this code or data, please cite our paper:
[Authors], "Rate of PI(4)P Synthesis Tunes Plasma Membrane PI(4,5)P₂ and Rho GTPase Oscillations", *TBD*, [year].
