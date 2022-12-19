"""Data Preprocessing Module

Handles data ingestion, cleaning, transformation, validation and output.

Public Functions (called in dags.data_pipeline module):
    - ingest_and_process_data
    - check_output_data_validity

Private Functions:
    - _get_processed_list
    - _clean_dob
    - _validate_email
    - _validate_mobile_number
    - _clean_data
    - _validate_data
    - _generate_member_id
"""
import os
import hashlib
import pandas as pd
import dataproc_config as cfg
from airflow.exceptions import AirflowFailException

# =============================================
# Public Functions
# =============================================
def ingest_and_process_data():
    """Ingest and process raw data.

    Steps include:
        - ingest data
        - clean data
        - validate data to identify successful and failed applications
        - generate member ID for successful applications
        - output successful and failed applications

    Returns:
        int: 0 if function is completed successfully, else 1.
    """
    # Check for existence of output directories
    for datair in [cfg.SUCCESS_DATA_DIR, cfg.FAIL_DATA_DIR]:
        if not os.path.exists(datair):
            os.mkdir(datair)
    
    # Get processed list
    processed_list = _get_processed_list()
    print("Processed files: {}\n".format(processed_list))

    for filename in os.listdir(cfg.INPUT_DATA_DIR):
        # skip over filenames that have been processed before
        # if filename in processed_list:
        #     print("{} already processed.\n".format(filename))
        #     continue    
        if filename.endswith(".csv"):
            print("{}:".format(filename))
            filepath = os.path.join(cfg.INPUT_DATA_DIR,filename)
            print("- ingest data from {}...".format(filepath))
            df = pd.read_csv(filepath)

            print("- clean data...")
            df = _clean_data(df)

            print("- validate data...")
            df = _validate_data(df)
            success_mask = df["success"]==True

            print("- generate member id for successful applications")
            df["member_id"] = df[["last_name","date_of_birth"]].apply(lambda x: _generate_member_id(x["last_name"], x["date_of_birth"]), axis=1)

            print("- output successful applications...")
            relevant_columns = ["member_id","first_name","last_name","email","date_of_birth","mobile_no","above_18"]
            df[success_mask][relevant_columns].to_csv(os.path.join(cfg.SUCCESS_DATA_DIR,"successful_"+filename), index=False)

            print("- output failed applications...")
            relevant_columns = ["first_name","last_name","email","date_of_birth","mobile_no","above_18"]
            df[~success_mask][relevant_columns].to_csv(os.path.join(cfg.FAIL_DATA_DIR,"failed_"+filename), index=False)

            print("- Done!\n")
        else:
            print("invalid filename: {}".format(filename))
            raise AirflowFailException("Invalid input filename")
    
    return 0

def check_output_data_validity():
    """Check validity of output data (all in successful output folder are success).

    Checks that:
        - all in successul output folder are valid applications.
        - all in failed output folder are non-valid applications.

    Returns:
        int: 0 if function is completed successfully.
    """
    pass_check = True
    for datadir in [cfg.SUCCESS_DATA_DIR, cfg.FAIL_DATA_DIR]:
        print(datadir)
        for filename in os.listdir(datadir):
            if filename.endswith(".csv"):
                filepath = os.path.join(datadir,filename)
                print("- ingest and check {}...".format(filepath))
                df = pd.read_csv(filepath, dtype=str)
                df = _validate_data(df)

                if "successful" in datadir:
                    num_success = df["success"].sum()
                    fract_success = num_success/len(df)
                    print("  - Successful applications = {0:d} out of {1:d} ({2:.2f}%)".format(num_success, len(df), fract_success*100))
                    print("  - All successful = {}".format(df["success"].all()==True))
                    pass_check = pass_check and (df["success"].all()==True)
                elif "failed" in datadir:
                    num_fail = (~df["success"]).sum()
                    print("  - Failed applications = {0:d} out of {1:d} ({2:.2f}%)".format(num_fail, len(df), num_fail/len(df)*100))
                    print("  - All failed = {}".format(df["success"].all()==False))
                    pass_check = pass_check and (df["success"].all()==False)
            else:
                print("invalid filename: {}".format(filename))
        print("")
    print("Pass Validity Check:", pass_check)
    if pass_check:
        return 0
    else:
        raise AirflowFailException("Output data fail validity check")


# =============================================
# Private Functions
# =============================================
def _get_processed_list():
    """Get list of processeded application input data files.

    Returns:
        list: list of processed application input data filenames.
    """
    processed_list1 = set([fname.lstrip("successful").lstrip("_") for fname in os.listdir(cfg.SUCCESS_DATA_DIR)])
    processed_list2 = set([fname.lstrip("failed").lstrip("_") for fname in os.listdir(cfg.FAIL_DATA_DIR)])
    processed_list = list(processed_list1.union(processed_list2))
    return processed_list

def _clean_dob(dob_string):
    """Cleans input data of birth string and sets it to YYYYMMDD format.

    Splits date into its three fields and attenpts to identify
        - year field: 4 digits (can be either the first or last field)
        - month field: defaults to middle field if it is <= 12, else the remaining non-year field
        - day field: remaining non-year, non-month field

    Args:
        dob_string (str): data of birth of applicant.

    Returns:
        str: cleaned date of birth in YYYYMMDD format.
    """
    # replace all "-" separators with "/"
    dob_string = dob_string.replace("-","/")

    # split date of birth into fields by "/" separator
    [field1, field2, field3] = dob_string.split("/")

    # Identify year, month, day field.
    if field1.isdigit() and len(field1) == 4:
        year = field1
        if int(field2) <= 12:
            month = field2
            day = field3
        else:
            month = field3
            day = field2
    elif field3.isdigit() and len(field3) == 4:
        year = field3
        if int(field2) <= 12:
            month = field2
            day = field1
        else:
            month = field1
            day = field2
    else:
        print(f"invalid date of birth {dob_string}")
        return None

    cleaned_dob = "".join([year,month,day])
    return cleaned_dob

def _validate_email(email_string):
    """Validates input email string is valid (i.e. ends with @emailprovider.com or @emailprovider.net). 

    Args:
        email_string (str): email address of applicant

    Returns:
        bool: True if email string is valid, else False.
    """
    field = email_string.split("@")
    if (len(field[-1].split("."))==2) and (field[-1].endswith(".com") or field[-1].endswith(".net")):
        return True
    else:
        return False

def _validate_mobile_number(mobile_string):
    """Validates if input mobile number is valid (i.e. 8 digits)

    Args:
        mobile_string (str): mobile number of applicant

    Returns:
        bool: True if mobile number is valid, else False.
    """
    if (len(mobile_string) == 8) and (mobile_string.isdigit()):
        return True
    else:
        return False    

def _clean_data(df):
    """Function to clean raw application data.

    Cleaning steps incldue
        - strip leading and trailing white space from all columns and check for nulls
        - drop duplicates
        - split name into first and last name
        - remove white space within mobile number
        - clean date of birth (dob) into YYYYMMDD format.

    Args:
        df (pandas dataframe): raw application data

    Returns:
        pandas dataframe: cleaned application data
    """
    # strip all leading and trailing white spaces and check for nulls
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].str.strip()
            num_nulls = (df[col].isnull() | df[col]=="").sum()
            if num_nulls > 0:
                print("{}: # null = {}".format(col, num_nulls))
    
    # drop duplicates
    df = df.drop_duplicates()

    # split name into first and last name
    df[["first_name","last_name"]] = df["name"].str.split(pat=" ",n=1,expand=True)
    
    # clean mobile number: remove white space within number
    df["mobile_no"] = df["mobile_no"].str.replace(' ', '')

    # clean dob and set to YYYYMMDD
    df["date_of_birth"] = df["date_of_birth"].apply(_clean_dob)

    return df

def _validate_data(df):
    """Function to validate cleaned data to be output.

    Validation steps include:
        - mobile number is 8 digits
        - email is valid (i.e. ends with @emailprovider.com or @emailprovider.net)
        - age (as of cfg.REF_DATE 2022-01-01) is > 18 years old

    Args:
        df (pandas dataframe): cleaned application data

    Returns:
        pandas dataframe: validated application data
    """
    # validate mobile no and email
    df["valid_mobile_no"] = df["mobile_no"].apply(_validate_mobile_number)
    df["valid_email"] = df["email"].apply(_validate_email)

    # compute age as of REF_DATE and validate > 18 years old
    df["age"] = (pd.to_datetime(cfg.REF_DATE,format="%Y%m%d") - pd.to_datetime(df["date_of_birth"],format="%Y%m%d"))/pd.Timedelta(365,"days")
    df["above_18"] = df["age"] > 18.0

    # create name column if it does not exist
    if "name" not in df.columns:
        df["name"] = df["first_name"] + " " + df["last_name"]

    df["success"] = (~df["name"].isnull()) & df["valid_mobile_no"] & df["above_18"] & df["valid_email"]
    return df

def _generate_member_id(last_name, dob_string):
    """Generate member id from last name and date of birth (only for successful applications).

    Args:
        last_name (str): last name of applicant
        dob_string (str): date of birth of applicant

    Returns:
        str: member ID given by <last_name>_<hash(dob_string)> where the second part is the first 5 digits of the SHA256 hash of the dob_string.
    """
    dob_hash = hashlib.sha256(dob_string.encode()).hexdigest()[0:5]
    member_id = last_name + "_" + dob_hash
    return member_id
