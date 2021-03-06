# Data Integration Tool (DIT) User's Guide
Below you will find an introduction to how to use DIT.
-------
### Table of Contents
* [Project overview](#project-overview)
    * [Important Links](#important-links)
* [Getting Started](#getting-started)
    * [DIT Installation](#dit-installation)
    * [Running DIT Command Line Interface](#running-dit-command-line-interface)
    * [DIT Flow Project Structure](#dit-flow-project-structure)
* [Widget Reference](#widget-reference)
    * [Arithmetic](#arithmetic-widgets)
    * [Numeric Replacement](#numeric-replacement-widgets)
        * [Open Range](#open-range-replacement)
        * [Single Value](#single-value-replacement)
        * [Closed Range](#closed-range-replacement)
        * [Rounding](#rounding)
    * [Statistical](#statistical-widgets)
        * [Probability Density Function](#probability-density-function)
        * [General statistics](#general-statistics)
    * [Data integrity verification](#data-integrity-verification)
    * [Data existence verification](#data-existence-verification)
    * [Data characterization](#data-characterization)
    * [Date manipulation](#date-manipulation)
    * [Text manipulation](#text-manipulation)
        * [Relocation](#relocation)
        * [Replacement](#replacement)
        * [Removal](#removal)
    * [Coordinate manipulation](#coordinate-manipulation)
## Project Overview
DIT is an outcome of the PermaData project.

#### Important links
* [Github Repository](https://github.com/PermaData/DIT) - online repository for DIT code and installation downloads.
* [Issue Tracking](https://github.com/PermaData/DIT/issues) - file bug and improvement issues for DIT

## Getting Started
### DIT Installation
DIT assumes it is being installed within a directory where you have read, write, and execute permissions.

#### On Linux
- The following system tools are required to run the automatic
  installation script:
  - curl
  - unzip
- Run the installation script:
  `$ curl -L
https://raw.githubusercontent.com/PermaData/DIT/widget_work/install_linux.sh
|bash`
  The result of this step should be a 'DIT-widget-work' directory
containing DIT.
- To test the installation:
  - `$ cd DIT-widget-work`
  - `$ source env.sh`
  - `$ inv test`

All of the tests run should pass.

### Running DIT Command Line Interface
To run DIT from the command line:
- `$ source env.sh` -> activates the conda python environment
- `$ python run_flow.py <path to flow configuration file>` -> a log file path can be passed in from the command line with the `-l` option. e.g. `python run_flow.py example/example_config.yml` runs the example project flow.

### DIT Flow Project Structure
An small example project is provided in the 'example' subdirectory.
Important structural elements of a project:
1. Separate input and output directories. This is needed as the list of
   input files is created from scanning the input directory.
2. A YAML configuration file. The configuration file is read by DIT to
   construct the workflow. This file can have either a '.yml' or a
'.yaml' extension. Important structural elements of a configuration
file:
  - It is divided into an 'input' and an 'output' section under those
    labels.
  - Input section required elements:
    - `reader` -> the name of the widget that can read the input
      files and return a 2D matrix of the data.
    - `data_directory` -> the path to the subdirectory to be scanned for
      input data files.
    - `variable_map` -> a file describing the column mapping between the
      input data matrix and the output data matrix.
    - `manipulations` -> an ordered list of manipulation widgets to run on the
      input data.
  - Input section optional elements:
    - `missing_values` -> a list of missing value constants. This list can be
      used as inputs to widgets in the configuration file by marking the list with an "anchor" (e.g. &ms) and then used with an "alias" (e.g. *ms) where the list should be as demonstrated in the example configuration file.
    - `missing_characters` -> a list of strings that represent missing
      characters in the data.
  - Output section required elements:
    - `data_directory` -> the path to the directory to be used to store
      the output files including the widget input and output files.
    - `writer`-> the name of the widget that can take a 2D matrix of
      data and write it to an output file.
    - `manipulations` -> an ordered list of manipulation widgets to run on the 2D
      data matrix after the variable map has been applied so the data is
in 'output' format.
  - Widget entry required elements:
    - `widget` -> the name of the widget to be run.
    - `do_it` -> a boolean flag to indicate whether or not this widget
      will be run. This can be used in iterative debugging to only run a
widget during certain runs without having to remove it from the flow.
    - `with_header` -> a boolean flag indicating whether the subsetted
      data used by the widget will include the first (header) row.
  - Widget entry optional elements:
    - `inputs` -> a list of name, value pairs of method arguments to be
      passed to the widget.
    - `input_columns` -> a list of columns to be added to the subset of
      data used by the widget from the full 2D data matrix. Use `['all']` to indicate the inclusion of the entire matrix.
    - `output_columns` -> a list of columns referencing the columns to
      be replaced in the full 2D data matrix by the widget's output
data. Use `['all']` to indicate the replacement of the entire matrix.


## Widget Reference
### Arithmetic widgets

- add_constant
- subtract_constant
- multiply_constant
- divide_constant

Interpretation:  
"Look at every value and {add to it/subtract from it/multiply it by/divide it by} {constant}."

Columns:  
These widgets must take columns that are numeric. If the entries have any characters that are non-numeric, I recommend cleaning them out with the remove_characters widget first.

Inputs:  
*constant*: The number to add/subtract/multiply/divide with every number in the column


### Numeric replacement widgets

#### Open range replacement
- replace_less_equal
- replace_less_than
- replace_greater_equal
- replace_greater_than

Interpretation:  
"Replace values {less than/greater than/less than or equal to/greater than or equal to} {threshold} with {value}."

Columns:  
These widgets must take columns that are numeric. If the entries have any characters that are non-numeric, I recommend cleaning them out with the remove_characters widget first.

Inputs:  
*threshold*: The boundary beyond which the replacement will take place. It functions as expected, like   
*value*: The number which will replace each entry selected by the comparison above.

#### Single value replacement
- replace_equal

Interpretation:  
"Replace values equal to {target} with {value}."

Columns:  
Same as above.

Inputs:  
*target*: The number that will be replaced within the data.  

#### Closed range replacement
- replace_in_range

Interpretation:  
"Replace values within the range {lower} to {upper} (inclusive) with {value}."

Columns:  
Same as above.

Inputs:  
*upper*: The top bound where the replacement will happen. It is inclusive, so instances of this value within the data column will be replaced.  
*lower*: The lower bound where the replacement will happen. It is inclusive, so instances of this value within the data column will be replaced.  
*value*: Same as others.

#### Rounding
- rounding

Interpretation:  
"Round all values in a specific way."

Columns:  
One or more numeric columns.

Inputs:  
*mode*: May be 'up', 'down', 'truncate', or 'nearest'. If it is 'up', rounds all values to the next highest integer, towards +inf. If it is 'down', rounds to the next lowest integer, towards -inf. If it is 'truncate', takes off the decimal part, rounding towards 0. If it is 'nearest', round to the nearest integer.  
*precision*: If an integer precision is given, instead round to that many digits beyond the decimal point.


### Statistical widgets

#### Probability density function
- pdf

Interpretation:  
"Calculate a numerical probability density function from the data."

Columns:  
Any numeric data. If the entries have any characters that are non-numeric, I recommend cleaning them out with the remove_characters widget first.

Inputs:  
*bins*: The number of bins for values to be sorted into. It should be an integer, but if it isn't, it will be truncated down.  
*minmax*: Can be 'auto' or 'manual'. If it is 'auto', the range captured by the distribution will be the entire range of the data. If 'manual', it will instead use the range defined by the *lower* and *upper* inputs.  
*lower*: Only used when *minmax* is 'manual'. The lower bound on a user-defined range.  
*upper*: Only used when *minmax* is 'manual'. The upper bound on a user-defined range.  
*outliers*: May be 'exclude' or 'include'. If it is 'exclude', values that fall outside the range of the distribution will be ignored. If it is 'include', these values will be sorted into the tail bins.  
*norm*: May be 'raw' or 'probability'. If it is 'raw', returns the number of values that fall in each bin. If 'probability', returns the proportion of values that fall in each bin.

#### General statistics
- statistics

Interpretation:  
"Calculate some general statistics of the data."

Columns:  
Any numeric data. If the entries have any characters that are non-numeric, I recommend cleaning them out with the remove_characters widget first.


Inputs:  
None.


### Data integrity verification

- check_int

Interpretation:  
"Check whether every value in the data is an integer."

Columns:  
Any numeric data. If the entries have any characters that are non-numeric, I recommend cleaning them out with the remove_characters widget first.

Inputs:  
None.


### Data existence verification

- count_records

Interpretation:  
"Count how many complete records (those that contain no missing entries) there are."

Columns:  
Any. The primary use cases will likely either be to inspect a particular column for missing values, or to examine all the columns at once to look for any type of missing data.

Inputs:  
None.


### Data characterization

- count_distinct

Interpretation:  
"Count the number of distinct values within a column."

Columns:  
A single column of any type of data.

Inputs:  
None.


- count_corresponding

Interpretation:  
"Count the number of different values in column B that are paired with each different value in column A."

Columns:  
Two of any type.

Inputs:  
None.


### Date manipulation

- reformat_dates_to_gtnp

Interpretation:  
"Reformat a date given into the GTN-P standard format."

Columns:  
A column of date information.

Inputs:  
*format*: A description of the current format of the date information, using [Python's *strptime* specification](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior). An abbreviated version of the table given at the link is below. Note that if characters other than date information appear in the column, they need to be included in the format. For instance, the correct format string corresponding to the date 'Y1998M07D24' (representing July 24, 1998) is 'Y%YM%mD%d'. This way the program will read only the relevant information.

| Directive | Meaning                                                                                                                                                                          | Example                                                                         |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| %a        | Weekday as locale’s abbreviated name.                                                                                                                                            | Sun, Mon, ..., Sat (en_US);So, Mo, ..., Sa (de_DE)                              |
| %A        | Weekday as locale’s full name.                                                                                                                                                   | Sunday, Monday, ..., Saturday (en_US);Sonntag, Montag, ..., Samstag (de_DE)     |
| %w        | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.                                                                                                                | 0, 1, ..., 6                                                                    |
| %d        | Day of the month as a zero-padded decimal number.                                                                                                                                | 01, 02, ..., 31                                                                 |
| %b        | Month as locale’s abbreviated name.                                                                                                                                              | Jan, Feb, ..., Dec (en_US);Jan, Feb, ..., Dez (de_DE)                           |
| %B        | Month as locale’s full name.                                                                                                                                                     | January, February, ..., December (en_US);Januar, Februar, ..., Dezember (de_DE) |
| %m        | Month as a zero-padded decimal number.                                                                                                                                           | 01, 02, ..., 12                                                                 |
| %y        | Year without century as a zero-padded decimal number.                                                                                                                            | 00, 01, ..., 99                                                                 |
| %Y        | Year with century as a decimal number.                                                                                                                                           | 0001, 0002, ..., 2013, 2014, ..., 9998, 9999                                    |
| %H        | Hour (24-hour clock) as a zero-padded decimal number.                                                                                                                            | 00, 01, ..., 23                                                                 |
| %I        | Hour (12-hour clock) as a zero-padded decimal number.                                                                                                                            | 01, 02, ..., 12                                                                 |
| %p        | Locale’s equivalent of either AM or PM.                                                                                                                                          | AM, PM (en_US);am, pm (de_DE)                                                   |
| %M        | Minute as a zero-padded decimal number.                                                                                                                                          | 00, 01, ..., 59                                                                 |
| %S        | Second as a zero-padded decimal number.                                                                                                                                          | 00, 01, ..., 59                                                                 |
| %z        | UTC offset in the form +HHMM or -HHMM (empty string if the object is naive).                                                                                                     | (empty), +0000, -0400, +1030                                                    |
| %j        | Day of the year as a zero-padded decimal number.                                                                                                                                 | 001, 002, ..., 366                                                              |
| %%        | A literal '%' character.                                                                                                                                                         | %                                                                               |


### Text manipulation

#### Relocation
- move_text

Interpretation:  
"Move text that is in a pattern from one place and overwrite a different pattern."


Columns:  
Any single column.

Inputs:  
*from_regex*: A regular expression that will choose which text to move.  
*to_regex*: A regular expression that determines which text will be overwritten.


#### Replacement
- replace_text

Interpretation:  
"Replace text that matches a regular expression with some other text."

Columns:  
Any

Inputs:  
*to_replace*: The regular expression that will be replaced.  
*with_replace*: The substring to replace the text selected by *to_replace*.  

#### Removal
- remove_characters

Interpretation:  
"Any time one of these characters shows up in the data, delete it."

Columns:  
Any

Inputs:  
*characters*: a set of characters to be removed in every entry within the data.


### Coordinate manipulation

- minsec_to_decimal

Interpretation:  
"Convert latitude/longitude data from degrees, minutes and seconds into decimal format."

Columns:  
The coordinates may be spread over several columns or all in one.

Inputs:  
None

- decimal_to_minsec

Interpretation:  
"Convert latitude/longitude data from decimal to degrees/minutes/seconds form."

Columns:  
The coordinates may be spread over several columns or all in one.

Inputs:  
None.

- utm_to_latlong

Interpretation:  
"Convert UTM data into latitude/longitude."

Columns:  
The columns must be easting (in meters), northing (in meters), zone number, and optionally a zone letter.

Inputs:  
None.

- latlong_to_utm

Interpretation:  

Columns:  

Inputs:  
None.
