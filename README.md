#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maqiujin
"""

# Floor Response Spectrum Generation

This repository provides a Python implementation for the generation of **floor response spectrum (FRS)** for multi-degree-of-freedom (MDOF) supporting structures.

The implemented methodology is based on the formulations presented in the associated publications listed below.

•	Ma, Q., & Kwon, O.-S. (2025). A direct derivation method for acceleration and displacement floor response spectra. Engineering Structures, 337, 120480. 
•	Ma, Q., & Kwon, O.-S. (2026). A direct floor-response spectrum generation method for multiple degree-of-freedom structures. Engineering Structures, 356, 122426.

The implementation is intended to provide an efficient alternative to conventional FRS generation through time history analysis. The methodology evaluates the acceleration response of nonstructural components (NSCs) using the modal properties of the supporting structure, the damping ratio of the NSC, and the input response spectrum.

## Features

The repository provides tools for:

- Generation of floor response spectrum for MDOF supporting structures.
- Calculation of modal floor response spectra.
- Combination of modal contributions to obtain the total FRS.
- Evaluation of FRS at different locations of the supporting structure.
- Generation and visualization of FRS over a specified range of secondary-system frequencies.
- Reproduction of a selected verification example.

## Repository Structure

```text
FRS-Generation/
│
├── src/
│   ├── frs_generation/
│   │   ├── main_FRS.py
│   │   ├── spectral_values_FRS.py
│   │   ├── main_modal_FRS.py
│   │   ├── modal_FRS.py
│   │   ├── coef_matrix_modal_FRS.py
│   │   ├── main_modal_combination.py
│   │   ├── lamda_matrix.py
│   │   ├── gupta_rigid.py
│   │   ├── lindley_rigid.py
│   │   ├── read_spectrum.py
│   │   ├── read_modal_prop.py
│   │   └── save_plot_FRS.py
│
├── examples/
│   ├── verification_example/
│   │   ├── example_excecution.py
│   │   ├── Modal_Properties.csv
│   │   ├── Mode_Shape.csv
│   │   ├── spectrum_input/
│   │   │   ├── Damping=0.02/
│   │   │   │   ├── RS_values.csv
│   │   │   ├──Damping=0.05/
│   │   │   │   └── RS_values.csv
│   │   │   ├── Damping=0.07/
│   │   │   │   └── RS_values.csv
│   │   │   ├── Damping=0.1/
│   │   │   │   ├── RS_values.csv
│   │   ├── reference_results/
│   │   │   ├── FRS_DOF1.csv
│   │   │   ├── FRS_DOF2.csv
│   │   │   ├── FRS_DOF3.csv
│   │   │   ├── FRS_DOF4.csv
│   │   │   ├── FRS_DOF5.csv
│   │   └── READ_ME.md
│
└── docs/
│   ├── methodology.md
│   └── inputs.md
```

The final repository structure may be updated as additional examples and implementations are added.

## Requirements

The code is implemented in Python.

Required Python packages include:

```text
numpy
matplotlib
```

The required packages can be installed using:

```bash
pip install -r requirements.txt
```

## Input

The FRS calculation requires structural modal properties and response-spectrum information. Depending on the analysis, the required inputs may include:

- Structural natural frequencies.
- Mode shapes at the location where the FRS is evaluated.
- Modal participation factors.
- Structural modal damping ratios.
- FRS damping ratio.
- FRS frequency range.
- Input response spectrum.

Detailed definitions and formatting requirements for the input parameters are provided in [`docs/inputs.md`](docs/inputs.md).

## Basic Usage

A basic FRS analysis follows the workflow:

```text
Input Response Spectrum
          ↓
Structural Modal Properties
          ↓
Modal Floor Response Spectra
          ↓
Modal Combination
          ↓
Total Floor Response Spectrum
```

Example scripts are provided in the `examples` directory.

A typical example can be executed using:

```bash
python examples/verification_example/example_excecution.py
```

The calculated FRS can then be exported as numerical data and plotted as a function of NSCs' frequencies.

## Methodology

The implementation is based on a direct formulation for deriving floor response spectra using the modal properties of the supporting structure.

The main calculation consists of:

1. Determining the contribution of each structural mode to the response of the NSC.
2. Generating the corresponding modal floor response spectra.
3. Combining the modal contributions using the implemented modal combination procedure.
4. Evaluating the total floor response spectrum at the selected structural location.

A brief description of the methodology is provided in [`docs/methodology.md`].

Equation numbers from Ma and Kwon (2026) are referenced within the main functions to facilitate comparison between the implementation and the published analytical formulation.

For the complete theoretical derivation and validation of the method, users should refer to the associated publications.

## Examples

The `examples` directory contains numerical examples demonstrating the use of the implementation.

The examples are intended to:

- Demonstrate the required input format.
- Provide simple test cases for verifying the installation.
- Illustrate FRS generation for MDOF structures.
- Reproduce selected validation results reported in the associated research.

Reference results are provided where appropriate to allow users to verify their implementation.

## Assumptions and Limitations

Users should review the assumptions associated with the implemented FRS formulation before applying the code.

The current implementation is intended primarily for systems satisfying the assumptions underlying the associated methodology. Applicability may depend on factors including:

- Structural nonlinear behavior
- NSC’s nonlinear behavior.

Additional assumptions and limitations are described in the associated publications and documentation.

## Citation

If you use this repository in academic or professional work, please cite the associated publications.

Citation information will also be provided through the `CITATION.cff` file.

## License

This project is distributed under the terms of the license provided in the [`LICENSE`](LICENSE) file.

## Contact

For questions regarding the methodology or implementation, please contact:

**[Qiujin Ma]**  
[Graduate student]  
[qiujin.ma@mail.utoronto.ca]
