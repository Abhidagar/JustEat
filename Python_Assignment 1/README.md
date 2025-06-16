#Setup Steps
-- Create a Virtual Environment
CMD --> python -m venv venv
 
-- Activate the Virtual Environment(Linux)
CMD --> source venv/bin/activate
 
-- Install Required Packages
CMD --> pip install -r requirements.txt
 
--use autopep8 to automatically format code according to PEP 8
CMD --> autopep8 --in-place --aggressive --aggressive your_file.py
 
project-folder/
├── venv/                                     # Virtual environment
├── requirements.txt                          # Required packages
├── operator.py                               # Operator examples
├── control_flow.py                           # If-elif-else, loops
├── functions.py                              # Functions and return values
├── collections.py                            # Lists, tuples, sets, dicts
├── modules_01.py                             # Custom module
├── modules_02.py                             # Using custom module
├── Classes-Exception_handling.py             # Class with attributes/methods
├── iterators.py, decorator.py, generator.py  # Decorators, generators, iterators
└── README.md                                 # Setup and usage guide
 
 
Run the Scripts---
 
python3 operator.py
python3 control_flow.py
python3 functions.py
python3 collections.py
python3 modules_02.py
python3 Classes-Exception_handling.py
python3 iterator.py
python3 decorator.py
python3 generator.py
