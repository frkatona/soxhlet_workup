# Soxhlet wash data extraction script

This project uses Flory-Huggins theory to estimate the number of polymer chains in PDMS after a solvent wash. 

 ## Flory-Huggins theory

 Flory-Huggins theory models the free energy of mixing for a polymer solution (here, PDMS in hexane).  This can be used to estimate the number of polymer chains in a given volume of solvent, n:

$$
n = \frac{ln(1-v) + v+ \chi v^{2}}{V(v - \frac{v}{2})}
$$

where $v$ ($v_{poly}$) is the volume fraction of polymer in the swollen mass, $\chi$ ($\chi_1$) is the system-dependent Flory-Huggins interaction parameter, and $V$ ($V_{mol,solv}$) is the molar volume of the solvent.

The value $n$ is useful directly, but it can also be related to the elastic modulus ($E$) of the polymer by the equation:

$$
E = 3 \cdot n \cdot R \cdot T
$$

where $R$ is the gas constant and $T$ is the absolute temperature.

## Usage
for use with custom csv format where:
   - row 1 is "sample, pre-wash, wash, post-dry"
   - sample names are formatted as "this_1", "this_2", "that_1", "that_2", etc.
   - mass is in grams

 ![example csv](images/example_csv.png "Example CSV Format")
 
 ![example output](images/example_output.png "Example Output")

 ## To Do:
   - [ ] Add support for different solvent and polymer systems
   - [ ] Rework stats workup