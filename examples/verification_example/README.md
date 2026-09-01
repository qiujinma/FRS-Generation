#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maqiujin
"""

# Verification Example

This example demonstrates the use of the FRS generation procedure and provides a verification case based on the FRS results of the idealized 5DOF2 structure published in Ma and Kwon (2026).

## Files

The example includes:

- `spectrum_input/` — input response spectrum and corresponding frequency values;
- `Modal_Properties.csv` — structural modal properties;
- `Mode_Shapes.csv` — structural mode-shape values;
- `example_excecution.py` — execution file for the FRS calculation; and
- `reference_results/` — reference results used for verification.

## Running the Example

Run the example from the repository root using:

```bash
python examples/verification_example/example_excecution.py
```

The calculated FRS can then be compared with the reference results provided in the `reference_results` folder.

## Verification Case

The example corresponds to a verification case presented in the associated publication.

[**FRS results for 5DOF2 in Figure 7 from Section 3.1**

Ma, Q., and Kwon, O.-S. (2026).  
“A direct floor-response spectrum generation method for multiple degree-of-freedom structures.”  
*Engineering Structures*, 356, Part B, 122426.  
https://doi.org/10.1016/j.engstruct.2026.122426
]