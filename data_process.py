import matplotlib.pyplot as plt
import psycopg2
import pandas as pd


def multiterm_model_SOFAMI():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs matching a set of terms in patients taking SOF and amiodarone,
    and for all AEs reported in patients taking SOF and amiodarone.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_SOFami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug1.caseid IN (SELECT caseid FROM drug1 \
                        WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac1.pt IN ('Bradycardia', 'Sinus bradycardia', \
        'Sinus node dysfunction', 'Syncope','Sinus arrhythmia',\
        'Cardiac failure congestive','Dizziness','Chest pain',\
        'Hypotension','Tachycardia','Dyspnoea')) \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_SOFami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug2.caseid IN (SELECT caseid FROM drug2 \
                        WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac2.pt IN ('Bradycardia', 'Sinus bradycardia', \
        'Sinus node dysfunction', 'Syncope','Sinus arrhythmia',\
        'Cardiac failure congestive','Dizziness','Chest pain',\
        'Hypotension','Tachycardia','Dyspnoea'))
        GROUP BY drug2.caseid, event_dt""", con)

    SOFami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug1.caseid IN (SELECT caseid FROM drug1 \
                        WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug1.caseid, event_dt""", con)

    SOFami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug2.caseid IN (SELECT caseid FROM drug2 \
                        WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_SOFami_df = pd.concat([cardiac_SOFami_df1, cardiac_SOFami_df2], ignore_index=True)
    cardiac_SOFami = cardiac_SOFami_df.sort_values('event_dt', ascending=1)
    SOFami_df = pd.concat([SOFami_df1, SOFami_df2], ignore_index=True)
    SOFami = SOFami_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_SOFami.caseid.tolist()
    cardiac_dates = cardiac_SOFami.event_dt.tolist()
    cardiac_count = cardiac_SOFami.pt_count.tolist()
    SOFami_cases = SOFami.caseid.tolist()
    SOFami_dates = SOFami.event_dt.tolist()
    SOFami_count = SOFami.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, SOFami_cases, SOFami_dates, SOFami_count


def multiterm_model_SOF():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs matching multiterm in patients taking SOF,
    and for all AEs reported in patients taking SOF.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_SOF_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        (reac1.pt IN ('Bradycardia', 'Sinus bradycardia', \
        'Sinus node dysfunction', 'Syncope','Sinus arrhythmia',\
        'Cardiac failure congestive','Dizziness','Chest pain',\
        'Hypotension','Tachycardia','Dyspnoea')) \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_SOF_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        (reac2.pt IN ('Bradycardia', 'Sinus bradycardia', \
        'Sinus node dysfunction', 'Syncope','Sinus arrhythmia',\
        'Cardiac failure congestive','Dizziness','Chest pain',\
        'Hypotension','Tachycardia','Dyspnoea')) \
        GROUP BY drug2.caseid, event_dt""", con)

    SOF_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') \
        GROUP BY drug1.caseid, event_dt""", con)

    SOF_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_SOF_df = pd.concat([cardiac_SOF_df1, cardiac_SOF_df2], ignore_index=True)
    cardiac_SOF = cardiac_SOF_df.sort_values('event_dt', ascending=1)
    SOF_df = pd.concat([SOF_df1, SOF_df2], ignore_index=True)
    SOF = SOF_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_SOF.caseid.tolist()
    cardiac_dates = cardiac_SOF.event_dt.tolist()
    cardiac_count = cardiac_SOF.pt_count.tolist()
    SOF_cases = SOF.caseid.tolist()
    SOF_dates = SOF.event_dt.tolist()
    SOF_count = SOF.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, SOF_cases, SOF_dates, SOF_count


def multiterm_model_AMI():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs matching in patients taking amiodarone,
    and for all AEs reported in patients taking amiodarone.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_ami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac1.pt IN ('Bradycardia', 'Sinus bradycardia', \
        'Sinus node dysfunction', 'Syncope','Sinus arrhythmia',\
        'Cardiac failure congestive','Dizziness','Chest pain',\
        'Hypotension','Tachycardia','Dyspnoea')) \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_ami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac2.pt IN ('Bradycardia', 'Sinus bradycardia', \
        'Sinus node dysfunction', 'Syncope','Sinus arrhythmia',\
        'Cardiac failure congestive','Dizziness','Chest pain',\
        'Hypotension','Tachycardia','Dyspnoea'))
        GROUP BY drug2.caseid, event_dt""", con)

    ami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug1.caseid, event_dt""", con)

    ami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_ami_df = pd.concat([cardiac_ami_df1, cardiac_ami_df2], ignore_index=True)
    cardiac_ami = cardiac_ami_df.sort_values('event_dt', ascending=1)
    ami_df = pd.concat([ami_df1, ami_df2], ignore_index=True)
    ami = ami_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_ami.caseid.tolist()
    cardiac_dates = cardiac_ami.event_dt.tolist()
    cardiac_count = cardiac_ami.pt_count.tolist()
    ami_cases = ami.caseid.tolist()
    ami_dates = ami.event_dt.tolist()
    ami_count = ami.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, ami_cases, ami_dates, ami_count


def bradycardia_model_SOFAMI():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs matching "bradycardia" in patients taking SOF and amiodarone,
    and for all AEs reported in patients taking SOF and amiodarone.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_SOFami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug1.caseid IN (SELECT caseid FROM drug1 \
                        WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac1.pt='Bradycardia' OR reac1.pt='Sinus bradycardia') \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_SOFami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug2.caseid IN (SELECT caseid FROM drug2 \
                        WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac2.pt='Bradycardia' OR reac2.pt='Sinus bradycardia') \
        GROUP BY drug2.caseid, event_dt""", con)

    SOFami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug1.caseid IN (SELECT caseid FROM drug1 \
                        WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug1.caseid, event_dt""", con)

    SOFami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug2.caseid IN (SELECT caseid FROM drug2 \
                        WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_SOFami_df = pd.concat([cardiac_SOFami_df1, cardiac_SOFami_df2], ignore_index=True)
    cardiac_SOFami = cardiac_SOFami_df.sort_values('event_dt', ascending=1)
    SOFami_df = pd.concat([SOFami_df1, SOFami_df2], ignore_index=True)
    SOFami = SOFami_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_SOFami.caseid.tolist()
    cardiac_dates = cardiac_SOFami.event_dt.tolist()
    cardiac_count = cardiac_SOFami.pt_count.tolist()
    SOFami_cases = SOFami.caseid.tolist()
    SOFami_dates = SOFami.event_dt.tolist()
    SOFami_count = SOFami.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, SOFami_cases, SOFami_dates, SOFami_count


def bradycardia_model_SOF():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs matching "bradycardia" in patients taking SOF,
    and for all AEs reported in patients taking SOF.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_SOF_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        (reac1.pt='Bradycardia' OR reac1.pt='Sinus bradycardia') \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_SOF_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        (reac2.pt='Bradycardia' OR reac2.pt='Sinus bradycardia') \
        GROUP BY drug2.caseid, event_dt""", con)

    SOF_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') \
        GROUP BY drug1.caseid, event_dt""", con)

    SOF_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_SOF_df = pd.concat([cardiac_SOF_df1, cardiac_SOF_df2], ignore_index=True)
    cardiac_SOF = cardiac_SOF_df.sort_values('event_dt', ascending=1)
    SOF_df = pd.concat([SOF_df1, SOF_df2], ignore_index=True)
    SOF = SOF_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_SOF.caseid.tolist()
    cardiac_dates = cardiac_SOF.event_dt.tolist()
    cardiac_count = cardiac_SOF.pt_count.tolist()
    SOF_cases = SOF.caseid.tolist()
    SOF_dates = SOF.event_dt.tolist()
    SOF_count = SOF.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, SOF_cases, SOF_dates, SOF_count


def bradycardia_model_AMI():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs matching 'bradycardia' in patients taking amiodarone,
    and for all AEs reported in patients taking amiodarone.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_ami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac1.pt='Bradycardia' OR reac1.pt='Sinus bradycardia') \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_ami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%AMIODARONE%') AND \
        (reac2.pt='Bradycardia' OR reac2.pt='Sinus bradycardia') \
        GROUP BY drug2.caseid, event_dt""", con)

    ami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug1.caseid, event_dt""", con)

    ami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_ami_df = pd.concat([cardiac_ami_df1, cardiac_ami_df2], ignore_index=True)
    cardiac_ami = cardiac_ami_df.sort_values('event_dt', ascending=1)
    ami_df = pd.concat([ami_df1, ami_df2], ignore_index=True)
    ami = ami_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_ami.caseid.tolist()
    cardiac_dates = cardiac_ami.event_dt.tolist()
    cardiac_count = cardiac_ami.pt_count.tolist()
    ami_cases = ami.caseid.tolist()
    ami_dates = ami.event_dt.tolist()
    ami_count = ami.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, ami_cases, ami_dates, ami_count


def cardiac_model_SOFAMI():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs within the 'Cardiac disorders' SOC in patients taking SOF and amiodarone,
    and for all AEs reported in patients taking SOF and amiodarone.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_SOFami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        FULL OUTER JOIN meddra ON (meddra.pt=reac1.pt) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug1.caseid IN (SELECT caseid FROM drug1 \
                        WHERE prod_ai LIKE '%AMIODARONE%') AND \
        soc='Cardiac disorders' \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_SOFami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        FULL OUTER JOIN meddra ON (meddra.pt=reac2.pt) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug2.caseid IN (SELECT caseid FROM drug2 \
                        WHERE prod_ai LIKE '%AMIODARONE%') AND \
        soc='Cardiac disorders' \
        GROUP BY drug2.caseid, event_dt""", con)

    SOFami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug1.caseid IN (SELECT caseid FROM drug1 \
                        WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug1.caseid, event_dt""", con)

    SOFami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        drug2.caseid IN (SELECT caseid FROM drug2 \
                        WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_SOFami_df = pd.concat([cardiac_SOFami_df1, cardiac_SOFami_df2], ignore_index=True)
    cardiac_SOFami = cardiac_SOFami_df.sort_values('event_dt', ascending=1)
    SOFami_df = pd.concat([SOFami_df1, SOFami_df2], ignore_index=True)
    SOFami = SOFami_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_SOFami.caseid.tolist()
    cardiac_dates = cardiac_SOFami.event_dt.tolist()
    cardiac_count = cardiac_SOFami.pt_count.tolist()
    SOFami_cases = SOFami.caseid.tolist()
    SOFami_dates = SOFami.event_dt.tolist()
    SOFami_count = SOFami.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, SOFami_cases, SOFami_dates, SOFami_count


def cardiac_model_SOF():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs within the 'Cardiac disorders' SOC in patients taking SOF,
    and for all AEs reported in patients taking SOF.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_SOF_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        FULL OUTER JOIN meddra ON (meddra.pt=reac1.pt) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        soc='Cardiac disorders' \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_SOF_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        FULL OUTER JOIN meddra ON (meddra.pt=reac2.pt) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') AND \
        soc='Cardiac disorders' \
        GROUP BY drug2.caseid, event_dt""", con)

    SOF_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') \
        GROUP BY drug1.caseid, event_dt""", con)

    SOF_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%SOFOSBUVIR%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_SOF_df = pd.concat([cardiac_SOF_df1, cardiac_SOF_df2], ignore_index=True)
    cardiac_SOF = cardiac_SOF_df.sort_values('event_dt', ascending=1)
    SOF_df = pd.concat([SOF_df1, SOF_df2], ignore_index=True)
    SOF = SOF_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_SOF.caseid.tolist()
    cardiac_dates = cardiac_SOF.event_dt.tolist()
    cardiac_count = cardiac_SOF.pt_count.tolist()
    SOF_cases = SOF.caseid.tolist()
    SOF_dates = SOF.event_dt.tolist()
    SOF_count = SOF.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, SOF_cases, SOF_dates, SOF_count


def cardiac_model_AMI():
    """
    Queries faers db and returns case IDs, event dates, and AE counts per case
    for AEs within the 'Cardiac disorders' SOC in patients taking amiodarone,
    and for all AEs reported in patients taking amiodarone.
    """

    con = psycopg2.connect(database = 'faers', user = 'irene')

    cardiac_ami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        FULL OUTER JOIN meddra ON (meddra.pt=reac1.pt) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%AMIODARONE%') AND \
        soc='Cardiac disorders' \
        GROUP BY drug1.caseid, event_dt""", con)

    cardiac_ami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        FULL OUTER JOIN meddra ON (meddra.pt=reac2.pt) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%AMIODARONE%') AND \
        soc='Cardiac disorders' \
        GROUP BY drug2.caseid, event_dt""", con)

    ami_df1 = pd.read_sql_query("""
        SELECT DISTINCT(drug1.caseid), event_dt, \
        COUNT(DISTINCT(reac1.pt)) AS pt_count FROM drug1 \
        FULL OUTER JOIN reac1 ON (reac1.caseid=drug1.caseid) \
        FULL OUTER JOIN demo1 ON (demo1.caseid=drug1.caseid) \
        FULL OUTER JOIN ther1 ON (ther1.caseid=drug1.caseid) \
        WHERE drug1.caseid IN (SELECT caseid FROM drug1 \
                                WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug1.caseid, event_dt""", con)

    ami_df2 = pd.read_sql_query("""
        SELECT DISTINCT(drug2.caseid), event_dt, \
        COUNT(DISTINCT(reac2.pt)) AS pt_count FROM drug2 \
        FULL OUTER JOIN reac2 ON (reac2.caseid=drug2.caseid) \
        FULL OUTER JOIN demo2 ON (demo2.caseid=drug2.caseid) \
        FULL OUTER JOIN ther2 ON (ther2.caseid=drug2.caseid) \
        WHERE drug2.caseid IN (SELECT caseid FROM drug2 \
                                WHERE prod_ai LIKE '%AMIODARONE%') \
        GROUP BY drug2.caseid, event_dt""", con)
    con.close()

    cardiac_ami_df = pd.concat([cardiac_ami_df1, cardiac_ami_df2], ignore_index=True)
    cardiac_ami = cardiac_ami_df.sort_values('event_dt', ascending=1)
    ami_df = pd.concat([ami_df1, ami_df2], ignore_index=True)
    ami = ami_df.sort_values('event_dt', ascending=1)
    cardiac_cases = cardiac_ami.caseid.tolist()
    cardiac_dates = cardiac_ami.event_dt.tolist()
    cardiac_count = cardiac_ami.pt_count.tolist()
    ami_cases = ami.caseid.tolist()
    ami_dates = ami.event_dt.tolist()
    ami_count = ami.pt_count.tolist()

    return cardiac_cases, cardiac_dates, cardiac_count, ami_cases, ami_dates, ami_count


def process_dataframes(flagged_cases, flagged_dates, flagged_event_counts, 
                        all_cases, all_dates, all_event_counts):
    """
    Organizes data by separating cases with no event dates, and 
    removing duplicate cases.
    """

    for idx, val in enumerate(flagged_dates):
        if val is None:
            key_idx = idx
            break

    for idx, val in enumerate(all_dates):
        if val is None:
            key_idx2 = idx
            break

    flagged_NaN_cases = flagged_cases[key_idx:]
    flagged_NaN_dates = flagged_dates[key_idx:]
    flagged_NaN_count = flagged_event_counts[key_idx:]

    print sum(flagged_NaN_count)

    flagged_ae_cases = []
    flagged_ae_dates = []
    flagged_ae_counts = []

    for idx, caseid in enumerate(flagged_cases[0:key_idx]):
        if caseid not in flagged_ae_cases:
            flagged_ae_cases.append(caseid)
            flagged_ae_dates.append(flagged_dates[idx])
            flagged_ae_counts.append(flagged_event_counts[idx])

    all_NaN_cases = all_cases[key_idx2:]
    all_NaN_dates = all_dates[key_idx2:]
    all_NaN_count = all_event_counts[key_idx2:]

    print sum(all_NaN_count)

    all_ae_cases = []
    all_ae_dates = []
    all_ae_counts = []

    for idx, caseid in enumerate(all_cases[0:key_idx2]):
        if caseid not in all_ae_cases:
            all_ae_cases.append(caseid)
            all_ae_dates.append(all_dates[idx])    
            all_ae_counts.append(all_event_counts[idx])  

    return flagged_ae_dates, flagged_ae_counts, all_ae_dates, all_ae_counts


def get_flagged_proportions(flagged_ae_dates, flagged_ae_counts, 
                            all_ae_dates, all_ae_counts):
    """
    Returns a list of the proportion of flagged AEs versus
    total AEs observed over the duration of the investigation.
    """

    proportions_per_month = []
    month_list = ['201405','201406','201407','201408','201409','201410','201411','201412',
              '201501','201502','201503','201504','201505','201506','201507','201508',
             '201509','201510','201511','201512','201601','201602','201603','201604',
             '201605','201606']

    cum_numerator = 0
    cum_denom = 0
    proportions_by_month = []

    for month in month_list:
        count1=0
        count2=0
        for idx, date in enumerate(flagged_ae_dates):
            if date[0:len(month)] == month:
                count1 += flagged_ae_counts[idx]

        for idx, date in enumerate(all_ae_dates):
            if date[0:len(month)] == month:
                count2 += all_ae_counts[idx]
        try:
            proportions_per_month.append(float(count1)/count2)
        except:
            proportions_per_month.append(0)

        cum_numerator += count1
        cum_denom += count2
        proportions_by_month.append(float(cum_numerator)/cum_denom)
        #cum_list.append(cum_denom)
        #cum_list.append(cum_count+33)    
    
    return proportions_by_month