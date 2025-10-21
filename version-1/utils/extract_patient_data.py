import pandas as pd

file_path = '/data/MIMIC_dataset/mimic-iii-clinical-database-1.4/NOTEEVENTS.csv'
df = pd.read_csv(file_path, usecols=["CATEGORY", "SUBJECT_ID", "HADM_ID", "TEXT"])
discharge_df = df[df["CATEGORY"] == "Discharge summary"]

# Count number of unique subject IDs
unique_subject_count = discharge_df["SUBJECT_ID"].nunique()
subject_id_list = discharge_df["SUBJECT_ID"].unique().tolist()

print(f"Unique patient_ids with at least one 'Discharge summary' notes: {unique_subject_count}")

columns_to_filter = []
df1 = pd.read_csv('/data/MIMIC_dataset/MIMIC_III_processed_new/phenotyping/test_listfile.csv')
filtered_df1 = df1[(df1[columns_to_filter] == 1).all(axis=1)].copy()


def get_stay_prefix(filename):
    base = filename.replace("_timeseries.csv", "")
    parts = base.split("_episode")
    return f"{parts[0]}_{parts[1]}"


def get_unique_patients(stays):
    return list(set(stays.split("_")[0] for stays in stays))


icu_stays_list = filtered_df1["stay"].apply(lambda x: get_stay_prefix(x)).tolist()

# print(f"ICU stays: {len(icu_stays_list)}")
unique_icu_patients = get_unique_patients(icu_stays_list)
print(f"# Unique ICU patients: {len(unique_icu_patients)}")

unique_icu_patients = [int(p) for p in unique_icu_patients]

matching_list = [prefix for prefix in unique_icu_patients if prefix in subject_id_list]
matching_count = sum(1 for prefix in unique_icu_patients if prefix in subject_id_list)

print(f"# Unique ICU patients with Discharge summaries: {matching_count}")

matching_subject_ids_set = set(matching_list)

filtered_df = df[
    (df["CATEGORY"] == "Discharge summary") &
    (df["SUBJECT_ID"].isin(matching_subject_ids_set))
    ]

filtered_df = filtered_df[
    # filtered_df["TEXT"].str.contains("INTENSIVE CARE UNIT COURSE", case=False, na=False) &
    filtered_df["TEXT"].str.contains("HOSPITAL COURSE", case=False, na=False)
]

print(len(filtered_df))
# filtered_df.to_csv("filtered_discharge_summaries.csv", index=False)
