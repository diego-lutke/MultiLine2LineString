# MultiLine2LineString
This repository contains a Python script that converts MultiLineStrings to LineStrings. It was developed because I needed to manipulate public transport paths from OpenStreetMap data in a peculiar way, which required handling the data as LineStrings instead of MultiLineStrings.

## Repository Structure
```
.
├── MultiLine2Line.py          # Main module containing the Multi2Line class
├── main.py                    # Main script to run the transformation
├── pyproject.toml             # Poetry configuration file
├── .gitignore
└── README.md                  # This README file
```
## Usage
The main functionality of this package is provided by the Multi2Line class in the `MultiLine2Line.py` script. You can use this class to transform MultiLineStrings into LineStrings according to a given threshold.

The `main.py` script in this repository is an example of how to use the `Multi2Line` class to process MultiLineStrings stored in a PostgreSQL database created with the Osmosis Pgsnapshot 0.6 schema. However, you can customize the script to fit your needs and use it with other data sources.

### Installing Dependencies
This project uses Poetry for dependency management. To install the required dependencies, run the following command in your terminal:
```
poetry install
```
### Running the `main.py` script
Activate the Poetry virtual environment by running:
```
poetry shell
```
Then, execute the `main.py` script:
```
python main.py
```
The script will fetch MultiLineStrings from the PostgreSQL database, process them using the `Multi2Line` class, and update the database with the resulting LineStrings.

## Customization
You can modify the `main.py` script to work with different data sources or adapt it to your specific needs. The key is to provide the `Multi2Line` class with MultiLineString objects and apply the transformation as needed.

For example, you can replace the PostgreSQL database interaction with another database system or even use files as your data source. Just make sure to update the script accordingly to fetch MultiLineStrings, process them using the Multi2Line class, and store the resulting LineStrings.
