# Insurance-Risk-Analytics-and-Predictive-Modeling
A project aimed at providing a marketing strategy and insight to handle low-risk targets in a better way and attract new clents.
## Overview

# 🏥 Insurance Risk Analytics & Predictive Modeling
## 📋 Project Overview
This project analyzes historical car insurance data for AlphaCare Insurance Solutions (ACIS) to identify low-risk segments and optimize marketing strategies through data-driven insights.

### 🎯 Business Objective
Discover "low-risk" insurance targets for premium reduction opportunities to attract new clients while maintaining profitability.

### 📊 Dataset Information
Data Structure (Pipe-separated .txt file)
Column Group	Column Name	Description	Data Type
Insurance Policy	UnderwrittenCoverID	Unique coverage identifier	String
PolicyID	Unique policy identifier	String
TransactionMonth	Month of transaction (Feb 2014-Aug 2015)	Date
Client Information	IsVATRegistered	VAT registration status	Boolean
Citizenship	Client's citizenship	String
LegalType	Legal entity type	String
Title	Client's title	String
Language	Preferred language	String
Bank	Banking institution	String
AccountType	Type of bank account	String
MaritalStatus	Marital status	String
Gender	Client's gender	String
Client Location	Country	Country of residence	String
Province	Province in South Africa	String
PostalCode	Postal/ZIP code	String
MainCrestaZone	Primary CRESTA zone	String
SubCrestaZone	Sub CRESTA zone	String
Car Information	ItemType	Type of insured item	String
Mmcode	Manufacturer model code	Numeric
VehicleType	Type of vehicle	String
RegistrationYear	Year of vehicle registration	Numeric
Make	Vehicle manufacturer	String
Model	Vehicle model	String
Cylinders	Number of cylinders	Numeric
Cubiccapacity	Engine capacity (cc)	Numeric
Kilowatts	Engine power (kW)	Numeric
Bodytype	Vehicle body type	String
NumberOfDoors	Number of doors	Numeric
VehicleIntroDate	Date vehicle introduced to market	Date
CustomValueEstimate	Estimated vehicle value	Numeric
AlarmImmobiliser	Security alarm system	String
TrackingDevice	Vehicle tracking device	String
CapitalOutstanding	Outstanding finance amount	Numeric
NewVehicle	Is vehicle new?	String
WrittenOff	Previously written off?	Boolean
Rebuilt	Rebuilt vehicle?	Boolean
Converted	Converted vehicle?	Boolean
CrossBorder	Cross-border vehicle?	Boolean
NumberOfVehiclesInFleet	Vehicles in client's fleet	Numeric
Insurance Plan	SumInsured	Total insured amount	Numeric
TermFrequency	Premium payment frequency	String
CalculatedPremiumPerTerm	Calculated premium amount	Numeric
ExcessSelected	Chosen excess amount	String
CoverCategory	Coverage category	String
CoverType	Type of coverage	String
CoverGroup	Coverage group	String
Section	Policy section	String
Product	Insurance product type	String
StatutoryClass	Statutory class	String
StatutoryRiskType	Statutory risk type	String
Payment & Claims	TotalPremium	Total premium collected	Numeric
TotalClaims	Total claims paid	Numeric
### 🏗️ Project Structure
text
insurance-analytics/
├── data/
│   ├── raw/               # Original dataset
│   └── processed/         # Cleaned data files
├── notebooks/
│   └── insurance_analysis.ipynb  # Main analysis notebook
├── src/
│   ├── data_loader.py     # Data loading and type conversion
│   ├── cleaner.py         # Data cleaning functions
│   └── eda_analyzer.py    # Exploratory Data Analysis
├── reports/
│   ├── figures/           # Generated visualizations
│   └── interim_report.md  # Interim findings
├── requirements.txt       # Python dependencies
└── README.md             # This file
🔧 Setup & Installation
Prerequisites
Python 3.8+

Git

Installation Steps
Clone the repository

bash
git clone https://github.com/yourusername/insurance-analytics.git
cd insurance-analytics
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Helps to install Required Dependencies

📈 Analysis Workflow
Task 1: Exploratory Data Analysis (EDA)
Data quality assessment and cleaning

Statistical distributions and outlier detection

Temporal trend analysis (Feb 2014 - Aug 2015)

Risk profiling across provinces and vehicle types

Task 2: Data Version Control (DVC)
Reproducible data pipeline setup

Version-controlled data transformations

Local remote storage configuration

Task 3 and 4 are yet to be performed