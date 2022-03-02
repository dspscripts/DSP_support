# DSP_support
Scripts to help plan things when playing Dyson Sphere Program

# Dependencies
tested with python 3.8.8

numpy

# dsp_calc.py
Ask for a given item at a given flow rate (item/second) and get a breakdown of all the buildings and ingredients required.

You can set the assembler, smelter, and proliferator level.

For proliferator level > 0, assumes all the inputs are proliferated with that level.

## Notes
Deuterium from fractionator assumes fully stacked Mk.3 belts of hydrogen.

Assume ray receivers run with graviton lenses.

The hydrogen used by fractionators is called hydrogen_frac

## usage
    python dsp_calc.py -h

to see the list of item names implemented use **--show-items**

## example

To see how to get 30 purple cubes per second

    python dsp_calc.py -i purple_cube -f 30 --assembler-level 3 --smelter-level 2 --proliferator-level 3
