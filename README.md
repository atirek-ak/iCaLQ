# CaLQ

#### _LHC Dilepton Limits Calculator_
Version 1.0.0

## Introduction
This is a dilepton limits calculator. It supports the U1 & S1 leptoquark models. The calculator can be used in two modes: [interactive](#interactive-mode) and [non-interactive](#non-interactive-mode) to find limits for leptoquark couplings.

Theory and implementation details can be found in this [paper]. LHC data is taken from [here](https://www.hepdata.net/record/ins1782650).

## Setting Up
The calculator is written in python3 and only needs the packages mentioned in _requirements.txt_. To install those, set up a virtual environment & install the dependencies.
```sh
cd <calq-direcory>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Interactive Mode

To use the calculator in interactive mode,
```sh
python3 calq.py
```
You will be greeted with CaLQ banner and a list of available commands. The prompt will be `calq > `. Example commands include:
```
calq > import_model = U1
calq > mass = 1234
calq > couplings = LM23L LM33R
calq > significance = 1
calq > ignore_single_pair = no
calq > systematic_error = 0.1
calq > status
calq > help
calq > initiate
```
The list of valid commands are:

- `import_model` to specify which leptoquark model to use.
- `mass` should be an integer between 1000 and 3000 (inclusive).
- `couplings` should list couplings in the format _LMxyL_ or _LMxyR_ where _x_ is the quark number and _y_ is the lepton number and the last _L_ or _R_ denote left or right handedness respectively.
- `significance` takes values 1 or 2.
- `extra_width` take any positive value. In case of an additional
decay mode, you can input extra width
- `ignore_single_pair` takes values _yes_ or _no_. Input _yes_ means that the single and pair productions will be ignored and this will speed up calculations.
- `systematic_error` denotes the systematic error margin. Default is 10%.
- `status` displays the current values of input parameters.
- `help` displays the list of commands available.
- `initiate` will compute the chi-square polynomial and its minima corresponding to the current values of input parameters.

Once initiated, the calculator goes to input values accepting mode and the prompt changes to ` > `. This prompt will only accept queries of the `<f1> <f2> ... <fn>`, where _\<f1\>_ to _\<fn\>_ are floating point numbers, _n_ is the number of couplings in the parameters and the values are space separated. The expected order of couplings (which is the same as the input order) is mentioned after initiating.

Corresponding to every query, the delta chi-square value will be displayed. Whether this is allowed withing the {1,2} sigma limit is also displayed.

Type `done` to exit query mode. An example query after executing the above commands would be:
```
 > 0.1 0
 > 0.37 0.0001
 > 0.5 0.7
 > done
```

The prompt returns to the input mode and input parameters hold the previous values which can be updated. Finally, to exit the calculator,
```
calq > exit
```

## Non-interactive Mode

To use the calculator in non-interactive mode, use the tag `-ni` or `--non-interactive`. Note that input cards and query values must be provided in this mode. An example of usage in this mode:
```sh
python3 calq.py -ni --input-card sample/sample_1.card --input-values sample/sample_1.vals --output-yes sample/sample_1_yes.csv --output-no sample/sample_1_no.csv --output-common sample/sample_1_common.csv
```

```sh
python3 calq.py [options]
```
Options:
- `--help`: Display this help message.
- `--input-card=[filename]`: Input card file. Line 1: mass, line 2: couplings, line 3: ignore_single_pair, line 4: sigma. These are same as input parameter values mentioned in the interactive version.
- `--input-values=[filename]`: Input values to check from the given file. Each line contains a query value. If there are _n_ couplings, then each line would be `<f1> <f2> ... <fn>`, where _\<fi>_ are float values.
- `--non-interactive` or `-ni`: Run in non-interactive mode. This requires input-card and input-values to be specified
- `--no-banner` or `-nb`: calq banner is not printed.
- `--output-yes=[filename]`: Specify the name of output file (allowed values) (overwrites the existing file). Default: calq_yes.csv
- `--output-no=[filename]`: Specify the name of output file (disallowed values) (overwrites the existing file). Default: calq_no.csv

## Caveats

The calculator is in its version 1.0.0 and currently only U1 & S1 leptoquark models are used. You can refer to section [Adding a new leptoquark Model](#Adding-a-new-Leptoquark-Model) for adding your own leptoquark model. Any comments regarding the calculator can be emailed to [us](mailto:atirek.kumar@research.iiit.ac.in).

## Adding a new Leptoquark Model
Currently, we have added the models S1 & U1 to the leptoquark calculator. To add your own models to the calculator, you must have the cross-section & efficiency data generated for various mass points & decay processes. To add a model, called **X1**, follow these steps:
1. Add the data in  directory. Follow the naming conventions used in the other models. 
   * `data/model/X1` should have 2 directories: `cross_section` & `efficiency`
   * The `cross-section` directory should have _csv_ files with the same decay process names as used in the other models.
   * The `efficiency` directory should have sub-directories with the same decay process names as used in the other models. Each decay process subdirectory in `efficiencies` should be followed by a coupling name(format: {quark index}{lepton index}{chirality}). Inside these directories there should be either _csv_ files named as _{mass value}.csv_ or in case of tau, subdirectories with integer mass value, with _csv_ files inside corresponding to the decay process tags.
2. In `classes/branching_fraction.py` add the formula to compute the branching fraction for couplings in model **X1**, else the branching fraction will be taken as 0 by default.
3. In `classes/custom_datatypes.py` , in class _KFactor_, add the K-factor value for **X1**, corresponding to all decay processes. If you are not sure about what value to use here, input it as 1.0.
4. In `config/physics.json`, append **X1** to either _scalar_leptoquark_models_ or _vector_leptoquark_models_. 
  
That's it! You should be good to go.