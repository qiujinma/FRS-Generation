#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Input Data

## Overview

The floor response spectrum (FRS) calculation requires two main groups of input data:

1. the input response spectrum; and
2. the modal properties of the supporting structure.

The input data are read from external files and supplied to the FRS calculation functions.

Users should ensure that all quantities are provided using a consistent unit system.

---

## 1. Input Response Spectrum

The input response spectrum file contains the frequency values and the corresponding spectral response values used in the FRS calculation.

A typical input file may be organized as:

```text
RS_values 			
values seperated by a comma			
F [Hz],Sa [m/s^2],Sv [m/s],Sd[m] 
0.200,0.884,0.830,0.552
0.211,0.966,0.869,0.540
0.224,1.075,0.889,0.538
0.236,1.174,0.934,0.527
0.250,1.284,0.952,0.516
0.264,1.389,0.965,0.500
0.279,1.490,0.956,0.477
0.296,1.580,0.946,0.454
...
```

### Required Columns

| Column | Description | Unit |
|---|---|---|
| `F [Hz]` | Oscillator frequency associated with the input response spectrum | Hz |
| `Sa [m/s^2]` | Spectral acceleration at the corresponding frequency | Consistent acceleration unit |
| `Sv [m/s]` | Spectral velocity at the corresponding frequency | Consistent velocity unit |
| `Sd [m]` | Spectral displacement at the corresponding frequency | Consistent displacement unit |

The frequency values in the response spectrum file also define the frequency range over which the FRS is evaluated in the current implementation.

Therefore, a separate minimum frequency, maximum frequency, or frequency increment does not need to be specified.

If spectral values are required at frequencies that are not explicitly provided in the input file, the spectrum is interpolated internally by the implementation.

### Frequency Range

Users should select a frequency range and resolution appropriate for the structural and nonstructural components' frequencies of interest.

Particular attention should be given to frequency regions close to structural modal frequencies, where the FRS may vary rapidly.

---

### Additional information

Users should specify the rigid frequency (Hz) for the input response spectrum in the excecution file, corresponding to the frequency where the difference in the spectral acceelrations beyond this frequency is within 2%.

Users sgould also specify the peak ground acceleration of the input response spectra in the excecution file, in 'm/s^2'.

For example:

```python
fr = 44
PGA = 3.5
```

## 2. Structural Modal Properties

The supporting structure is represented using its modal properties.

For each structural mode, the required information includes:

- natural frequency;
- modal damping ratio;
- modal participation factor; and
- mode-shape value at the location where the FRS is evaluated.

A typical modal-property file may be organized as:

```text
values seperated by a comma			
Mode	,Frequency [Hz],Paticipation_fac,Damping_ratio 
1,10.8299,1.48758,0.050
2,23.9535,0.675921,0.0426
3,36.7499,0.380976,0.050
...
```
### Required Columns

| Column | Description | Unit |
|---|---|---|
| `Mode` | Structural mode number | — |
| `Frequency [Hz]` | Natural frequency of the structural mode | Hz |
| `Paticipation_fac`  | Modal participation factor | Depends on mode-shape normalization |
| `Damping_ratio`  | Modal damping ratio | Decimal |

For example, a 5% damping ratio should be entered as:

```text
0.05
```

rather than:

```text
5
```

A typical mode-shape file may be organized as:
```text
values seperated by a comma
0.160175	,0.363181,0.533636,-0.751606,-0.813162
0.343707	,0.632058,0.560504,0.0062396,1

```
### Required Columns

| Row | Column | Description |
|---|---|---|
| Degree of freedom | Structural mode | Mode-shape component for the specified degree of freedom and structural mode; value depends on the adopted normalization convention |
---

## 3. Mode-Shape and Participation-Factor Convention

The mode shapes and modal participation factors must be defined using a consistent normalization convention.

Because the modal contribution to the FRS depends on the combination of the mode-shape value and modal participation factor, users should not independently rescale one quantity without consistently updating the other.

The modal properties may be obtained from external structural analysis software. Users are responsible for ensuring that the modal quantities supplied to the program are consistent with the formulation used in the associated publications.

---

## 4. FRS Location

The FRS is evaluated at a specified structural degree of freedom.

The mode-shape value supplied for each mode should therefore correspond to the same degree of freedom at which the FRS is to be calculated.

To calculate FRS at multiple locations, the calculation may be repeated using the corresponding mode-shape values for each location, or multiple degrees of freedom (DOFs) of interest may be specified directly in the execution file.

---

## 5. FRS Damping ratio

The damping ratio of the nonstructural component (NSC) is specified separately from the structural modal damping ratios.

The value should be entered as a decimal directly in the execution file.

For example:

```python
xo = 0.05
```

corresponds to a 5% damping ratio.

The specified NSC's damping ratio is assumed to remain constant over the full frequency range used for FRS calculation.

---

## 6. Units

The implementation does not automatically convert between unit systems.

Users should therefore ensure that all quantities use a consistent set of units.

Structural frequencies are specified in Hz.

Spectral acceleration should be supplied in: 
- `m/s²`.

The resulting acceleration FRS will be expressed in the unit of 'g'.

---

## 7. Modal Truncation

Users may either provide the modal properties of a sufficiently large number of structural modes or include only the modes with natural frequencies lower than the rigid frequency of the input response spectrum in the Modal_Properties file.

The treatment of modal truncation in the FRS calculation is described in methodology.md.

---

## 8. Example Input Files

Example input files are provided in:

```text
examples/verification_example/
```

The verification example includes the input files required for the FRS calculation, including:

- `spectrum_input/Damping=0.05/RS_values.csv`, containing the input response spectrum and corresponding frequency values;
- `Modal_Properties.csv`, containing the structural modal properties; and
- `Mode_Shapes.csv`, containing the structural mode-shape values.

The corresponding execution file, `example_execution.py`, demonstrates how the input data are read and used in the FRS calculation.

Verification results are provided in:
```text
examples/verification_example/reference_results/
```

This folder contains the reference results used to verify the implementation against the selected validation example.

Users are encouraged to run the verification example and compare the calculated results with the provided verification results before applying the implementation to their own structural models.