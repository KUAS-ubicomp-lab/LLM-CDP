import os

import pandas as pd

df = pd.read_csv('/data/MIMIC_dataset/MIMIC_III_processed_new/phenotyping/train_listfile.csv')

columns_to_filter = [
    # "Coronary atherosclerosis and other heart disease"
    # "Congestive heart failure; nonhypertensive"
    # "Essential hypertension"
    # "Acute myocardial infarction"
    # "Cardiac dysrhythmias"
    # "Respiratory failure; insufficiency; arrest (adult)"
    # "Other liver diseases"
    # "Other lower respiratory disease"
    # "Other upper respiratory disease"
]
columns_to_exclude = [
    # "Coronary atherosclerosis and other heart disease"
    # "Congestive heart failure; nonhypertensive",
    # "Essential hypertension",
    # "Acute myocardial infarction",
    # "Cardiac dysrhythmias"
]

filtered_df = df[(df[columns_to_filter] == 1).all(axis=1)].copy()
filtered_df = filtered_df[(filtered_df[columns_to_exclude] == 0).all(axis=1)]


# stay_prefix_list = filtered_df["stay"].str.split("_").str[0].add('_1').tolist()
def get_stay_prefix(filename):
    base = filename.replace("_timeseries.csv", "")
    parts = base.split("_episode")
    return f"{parts[0]}_{parts[1]}"


def get_first_stay_prefix(filename):
    base = filename.replace("_timeseries.csv", "")
    parts = base.split("_episode")
    return f"{parts[0]}"


def get_unique_patients(stays):
    return list(set(stays.split("_")[0] for stays in stays))


# Extract prefix from the "stay" column and store in a list
icu_stays_list = filtered_df["stay"].apply(lambda x: get_stay_prefix(x)).tolist()
icu_first_stays_list = set(filtered_df["stay"].apply(lambda x: get_first_stay_prefix(x)).tolist())

print(f"ICU stays: {len(icu_stays_list)}")
# print(stay_prefix_list)

unique_patients = get_unique_patients(icu_stays_list)
print(f"Unique patients: {len(unique_patients)}")
# print(unique_patients)

json_folder = '/data/MIMIC_dataset/MIMIC_III_processed_new/root/train_text_fixed'
clinical_notes = {f.split(".")[0] for f in os.listdir(json_folder)}
matching_count = sum(1 for prefix in icu_stays_list if prefix in clinical_notes)

print(f"Number of matching stay_prefix values with .json files: {matching_count}")
