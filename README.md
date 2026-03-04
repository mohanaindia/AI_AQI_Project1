# AQI PREDICTION PIPELINE

## OVERVIEW
This project implements a data processing pipeline for Air Quality Index (AQI) analysis and prediction. It reads raw air quality data, performs preprocessing and cleaning, and generates structured outputs for downstream analysis or modeling.

## WHAT IS AQI?
The Air Quality Index (AQI) is a standardized indicator used to communicate how polluted the air currently is and the associated health risks. This project demonstrates how raw environmental measurements can be transformed into meaningful, structured datasets for analysis.

## HOW AQI IS COMPUTED?

We implemented the official CPCB AQI breakpoint interpolation formula.

For each pollutant:  

AQI = ((I_high - I_low)(C - C_low))/((C_high - C_low)) + I_low   (sub_index calculation)

C = pollutant concentration
(C_low, C_high) = breakpoint concentration range
(I_low, I_high) = AQI index range

AQI = max(sub_indices)

## PROJECT STRUCTURE

AQI-Project/
│
├── data/
│   ├── raw/                # Input dataset(s)
│   └── processed/          # Cleaned dataset
│
├── outputs/
│   └── predictions.csv     # Final computed results
│
├── src/
│   ├── preprocess.py       # Data cleaning & normalization
│   └── cpcb_aqi.py         # AQI calculation logic
│
├── run_pipeline.py         # Main pipeline runner
└── README.md

## MODULE BREAKDOWN

1. preprocess.py

Responsible for:
- Normalizing column names
- Converting pollutant values to numeric
- Dropping rows with all pollutants missing
- Saving cleaned dataset

2. cpcb_aqi.py

Implements:
- AQI breakpoints (CPCB-based)
- Linear interpolation formula
- AQI bucket classification
- Dominant pollutant detection

3. python run_pipeline.py

This is the entry point of the project.

Pipeline flow:
- Automatically selects CSV from data/raw/
- Preprocesses data
- Computes AQI row-by-row
- Saves final results

## SETUP
pip install -r requirements.txt

## HOW TO RUN THE PROJECT: 

1. clone repository
2. install requirements (python3, pandas, numpy)
3. run pipeline [python run_pipeline.py]


## TECHNOLOGIES
1. Python3
2. Libraries - (Pandas, Numpy)
