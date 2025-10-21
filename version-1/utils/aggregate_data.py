import pandas as pd


def df_merge():
    df_discharge = pd.read_csv('medical_notes_with_lab_narratives_from_testlist.csv')
    df_entities = pd.read_csv('named_entities_from_testlist.csv')
    df_labels = pd.read_csv('test_listfile.csv')

    df_merged = pd.merge(
        df_discharge,
        df_entities,
        on=["subject_id", "hadm_id"],
        how="inner"
    )
    df_final = pd.merge(
        df_merged,
        df_labels,
        on="stay",
        how="inner"
    )

    return df_final
