import pandas as pd

train_df = pd.read_csv('/data/MIMIC_dataset/MIMIC_III_processed_new/phenotyping/test_listfile.csv')
icustays_df = pd.read_csv("/data/MIMIC_dataset/mimic-iii-clinical-database-1.4/ICUSTAYS.csv",
                          usecols=["SUBJECT_ID", "HADM_ID", "ICUSTAY_ID", "LOS"])
notes_df = pd.read_csv("/data/MIMIC_dataset/mimic-iii-clinical-database-1.4/NOTEEVENTS.csv",
                       usecols=["SUBJECT_ID", "HADM_ID", "CATEGORY", "TEXT"])


def get_subject_id(stay_name):
    return int(stay_name.split("_")[0])


train_df["SUBJECT_ID"] = train_df["stay"].apply(get_subject_id)

all_matching_notes = []

for _, row in train_df.iterrows():
    subject_id = row["SUBJECT_ID"]
    stay_value = row["stay"]
    target_period_length = float(row["period_length"])

    patient_icustays = icustays_df[icustays_df["SUBJECT_ID"] == subject_id]

    matched_hadm_ids = patient_icustays[
        round(patient_icustays["LOS"] * 24, 4) == target_period_length
        ]["HADM_ID"].tolist()

    for hadm_id in matched_hadm_ids:
        matched_notes = notes_df[
            (notes_df["SUBJECT_ID"] == subject_id) &
            (notes_df["HADM_ID"] == hadm_id) &
            (notes_df["CATEGORY"] == "Discharge summary")
            ]

        filtered_notes = matched_notes[
            matched_notes["TEXT"].str.contains("HOSPITAL COURSE", case=False, na=False) &
            ~matched_notes["TEXT"].str.contains("ADDENDUM", case=False, na=False)
            ]

        filtered_notes = filtered_notes.copy()
        filtered_notes["stay"] = stay_value
        all_matching_notes.append(filtered_notes)

result_df = pd.concat(all_matching_notes, ignore_index=True)
result_df = result_df[["stay", "SUBJECT_ID", "HADM_ID", "CATEGORY", "TEXT"]]

result_df.to_csv("medical_notes_from_testlist.csv", index=False)

print(f"Total matched discharge summaries: {len(result_df)}")
