#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maqiujin
"""

# Methodology

## 1. Overview

This repository implements direct floor response spectrum (FRS) generation procedures developed in the associated publications by Ma and Kwon.

The methodology allows acceleration FRS to be generated directly from the input response spectrum and the dynamic properties of the supporting structure and nonstructural component (NSC), without running time history analysis.

The implementation is based primarily on:

1. the direct derivation of acceleration FRS presented by Ma and Kwon (2025); and
2. the extension of the direct FRS generation procedure to multi-degree-of-freedom (MDOF) supporting structures presented by Ma and Kwon (2026).

The complete theoretical derivations and validation studies are provided in the associated publications. This document summarizes the computational procedure implemented in the repository.

## Relation to the Published Formulation

The main functions in the implementation include comments referencing the corresponding equation numbers in Ma and Kwon (2026). These references are provided to help users relate the computational steps in the code to the analytical formulation presented in the publication.

Users are encouraged to refer to Ma and Kwon (2026) for the complete derivation and definitions of the corresponding equations.

---

## 2. General Calculation Procedure

For an MDOF supporting structure, the FRS calculation follows the general procedure:

```text
Input Response Spectrum
        ↓
Structural Modal Properties
        ↓
Selection of Structural Modes
        ↓
Modal Floor Response Spectra
        ↓
Rigid-Response / High-Frequency Contribution
        ↓
Modal Correlation and Combination
        ↓
Total Floor Response Spectrum
```

The primary inputs include:

- input response spectrum and corresponding frequency values;
- structural natural frequencies;
- structural modal damping ratios;
- modal participation factors;
- structural mode shapes;
- degree(s) of freedom at which the FRS is evaluated; and
- NSC damping ratio.

The FRS is evaluated for the NSC frequencies specified through the input response spectrum.

---

## 3. Direct Floor Response Spectrum Formulation

The fundamental FRS formulation is based on the direct derivation presented by Ma and Kwon (2025).

The FRS is evaluated directly using the dynamic properties of the supporting structure and the NSC. The procedure computes acceleration FRS without requiring floor acceleration time histories.

For an individual structural modal contribution, the response depends on quantities including:

- the structural modal frequency;
- the structural modal damping ratio;
- the NSC frequency;
- the NSC damping ratio; and
- the corresponding spectral responses based on the input spectrum.

The implementation evaluates the modal FRS using the analytical expressions developed for perfect resonant and non-perfect resonance case.

Special treatment associated with perfect resonance cases is included according to the formulation presented in the associated publication.

For the complete derivation of the acceleration FRS expressions, refer to Ma and Kwon (2025).

---

## 4. Modal Representation of an MDOF Supporting Structure

For an MDOF supporting structure, the structural response is represented using its modal properties.

For structural mode 'j', the contribution at degree of freedom 'i' is scaled by the corresponding mode-shape component and modal participation factor. The modal scaling term can be represented as

'(partis[j] * phi[i][j])'

where:

- partis[j] is the modal participation factor of structural mode 'j'; and
- phi[i][j] is the mode-shape component of mode 'j' at degree of freedom 'i'.

The mode shapes and modal participation factors must therefore be provided using a consistent normalization convention.

The modal properties are read from the input files described in [`inputs.md`].

---

## 5. Modal Floor Response Spectra

A modal FRS is first evaluated for each structural mode retained in the analysis.

Each modal FRS represents the contribution of one structural mode to the NSC response at the selected degree of freedom. The calculation combines:

- the modal properties of the supporting structure;
- the NSC dynamic properties; and
- the input response spectrum.

The resulting modal FRS retains the resonance characteristics associated with the frequencies between the structural mode and the NSC.

The analytical modal FRS formulation is based on the direct derivation described in Ma and Kwon (2025) and subsequently incorporated into the MDOF FRS generation procedure of Ma and Kwon (2026).

---

## 6. Modal Correlation and Combination

The total FRS of an MDOF supporting structure should account for the correlation among modal FRS contributions, including both the correlation between structural modes and the correlation between the NSC response and the corresponding structural modal responses.

The MDOF formulation therefore incorporates analytically derived correlation coefficients between the FRS contributions of different structural modes.

The individual modal FRS contributions are combined using the complete quadratic combination (CQC)-FRS method presented by Ma and Kwon (2026).

The modal correlation coefficients are calculated using the analytical expressions developed in Ma and Kwon (2026) to account for the correlation among the modal FRS contributions.

The complete expressions and derivations are provided in Ma and Kwon (2026).

---

## 7. Modal Truncation and High-Frequency Modes

The methodology determines the structural modes that need to be explicitly considered in the FRS evaluation.

Structural modes lower than the rigid frequency of the input motion are evaluated explicitly using their modal properties using the modal FRS formulations.

The contribution of higher-frequency modes is considered using a single mode through the rigid-response formulation described by Ma and Kwon (2026). This allows the effects of modes beyond the rigid frequency to be incorporated without requiring the individual dynamic properties of all higher modes.

Accordingly, users may either:

- provide the modal properties of a sufficiently large number of structural modes; or
- provide only the modal properties of structural modes with natural frequencies lower than the rigid frequency of the input motion..

The implementation then accounts for the remaining high-frequency contribution according to the adopted rigid-response treatment.

---

## 8. Rigid Response Coefficient

The MDOF FRS methodology incorporates modified rigid response coefficients developed specifically for FRS evaluation.

These coefficients are used to account for the contribution of structural response that behaves effectively as a rigid response relative to the input motion, and these modal rigid components are combined with algebraic summation.

The modified formulation is intended to provide an appropriate and conservative representation of the total FRS.

Details of the rigid response coefficient and its derivation are provided in Ma and Kwon (2026).

---

## 9. Acceleration FRS

The direct formulation supports the evaluation of acceleration FRS.

The acceleration FRS represents the peak acceleration demand on an NSC over the specified NSC frequency range and is evaluated using the corresponding direct FRS formulations developed in Ma and Kwon (2025).

Users should ensure that the units of the input response spectrum and the resulting FRS are interpreted consistently, as described in [`inputs.md`].

---

## 10. FRS at Multiple Structural Locations

The FRS may be evaluated at any structural degree of freedom for which the corresponding mode shape values are available.

For each selected degree of freedom, the modal contribution is evaluated using the corresponding mode shape values.

FRS at multiple locations may therefore be obtained either by repeating the calculation for different degrees of freedom or by specifying multiple degrees of freedom in the execution file.

---

## 11. Assumptions and Applicability

The implementation should be used within the assumptions of the underlying analytical formulations.

Users should consider, in particular:

- the adopted structural and NSC damping ratios;
- the applicable frequency range of the input response spectrum; and
- the assumptions associated with the modal FRS and modal-combination formulations.

The complete theoretical assumptions, derivations, verification cases, and discussion of applicability are provided in the associated publications.

---

## 12. References

Ma, Q., and Kwon, O.-S. (2025).  
“A direct derivation method for acceleration and displacement floor response spectra.”  
*Engineering Structures*, 337, 120480.  
https://doi.org/10.1016/j.engstruct.2025.120480

Ma, Q., and Kwon, O.-S. (2026).  
“A direct floor-response spectrum generation method for multiple degree-of-freedom structures.”  
*Engineering Structures*, 356, Part B, 122426.  
https://doi.org/10.1016/j.engstruct.2026.122426