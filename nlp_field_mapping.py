import difflib
import string

# -- DistrictNameMatching.py
# Author: Anthony Louis D'Agostino (ald2187 [at] columbia.edu)
# Purpose: Given CSV lists of district-state name pairs, identifies the best match given the fuzzywuzzy library
# Notes: Default number of matches currently set to 3, though can be modified as input argument.
# **** AUTHOR NOT LIABLE FOR ANY DAMAGES INCURRED THROUGH THE USE OR [ESPECIALLY] MISUSE OF THIS PRODUCT ***** </code>

import os
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

# a function that normalizes strings by stripping punctuations, whitespaces, and cnovert to lower cases
def normalize(s):
    for p in string.punctuation:
        # included in the punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        s = s.replace(p, ' ')
    return s.lower()

def fuzzyWordMatch(sap, legacy, sap_des_col, legacy_des_col, sap_field_col, legacy_field_col, outFile, num_match):
    """
    This function takes two sets of district-state names, and produces a DTA with a set number (default=3)
    of matches with a flag for whether the district name has been completely matched.

    Manual work is then required for districts where a perfect match has not been made.

    sap: the SAP metadata description
    legacy: the legacy metadata description
    sap_des_col: column name of the column in sap that contains the description of the sap field names
    legacy_des_col: column name of the column in legacy that contains the description of the legacy field names
    sap_field_col: column name of the column in sap containing the sap field names
    legacy_field_col: column name of the column in legacy containing the legacy field names
    num_match: number of matches generated, default is 3
    outFile: includes path and filename for an outputted DTA file - should be "*.dta"
    """

    sap_data = pd.read_csv(sap, quotechar='"', skipinitialspace=True, sep=',')
    # print(" *** Now printing column values for sap file *** ")
    # print(list(sap_data.columns.values))

    legacy_data = pd.read_csv(legacy, quotechar='"', skipinitialspace=True, sep=',')
    # print(" *** Now printing column values for legacy file *** ")
    # print(list(legacy_data.columns.values))

    # store the texts in a diff obj
    sap_text = sap_data[sap_des_col]
    sap_fields = sap_data[sap_field_col]
    legacy_text = legacy_data[legacy_des_col]

    # normalize both sap & legacy text objects
    sap_text_normalized = []
    for text in sap_text:
        sap_text_normalized.append(normalize(str(text)))

    legacy_text_normalized = []
    for text in legacy_text:
        legacy_text_normalized.append(normalize(str(text)))

    # create top 3 match list using FuzzyWuzzy's built in process.extract() function, which default produce top 5 matches
    top3_matche_list = [process.extract(x, sap_text_normalized, limit=num_match) for x in legacy_text_normalized]
    # so the output is a tuple of 3 values!
    # fhp_new[x][y][z]
    # x = [0-nrow(top3_matche_list)]; row number; basically which legacy word you are trying to match
    # y = [0-2]; which match; there are 3 for each word;
    # z = [0,1]; every match has two values: (match word, score btwn 0-100)

    # -- generate column names for the new table "match_info"
    lab = "legacy_original"
    lab_index = ""
    lab_score = ""
    i = 1
    # while i <= num_match:
    #     lab = lab + " " + "Match" + str(i)
    #     lab_index = lab_index + " " + "Index" + str(i)
    #     lab_score = lab_score + " " + "Score" + str(i)
    #     i += 1
    while i <= num_match:
        lab = lab + " " + "Match" + str(i)
        # lab = lab + " " + "Index" + str(i)
        lab = lab + " " + "Description" + str(i)
        lab = lab + " " + "Score" + str(i)
        i += 1


    # so im going to create a giant table with all the matching info in it, such as the matching word and its score
    match_info = pd.DataFrame(columns=lab.split())

    for i in range(0,num_match):
        # so we create empty arrays that we can then append values to it
        word_match = []
        # index_match = []
        descri_match = []
        score_match = []
        for row in top3_matche_list:
            index_to_add = sap_text_normalized.index(row[i][0])
            word_match.append(sap_fields.iloc[index_to_add])
            # index_match.append(index_to_add)
            descri_match.append(legacy_data[legacy_des_col].iloc[index_to_add])
            score_match.append(row[i][1])
        j = i+1
        match_info['Match{}'.format(j)] = word_match
        # match_info['Index{}'.format(j)] = index_match
        match_info['Description{}'.format(j)] = descri_match
        match_info['Score{}'.format(j)] = score_match

    ## this dataframe d will be storing ALL your results, w first column being the original legacy column to match
    d = pd.DataFrame(columns=lab.split())
    d['legacy_original'] = legacy_data[legacy_field_col]
    # d['legacy_description'] = legacy_data[legacy_des_col]

    # d['legacy_original'] = legacy_data[legacy_des_col]
    # basically fill in all the columns in df d with matching column names in df match_info
    for x in range(1, num_match + 1):
        d["Match{}".format(x)] = [y for y in match_info['Match' + str(x)]]
        # d["Index{}".format(x)] = [y for y in match_info['Index' + str(x)]]
        d["Description{}".format(x)] = [y for y in match_info['Description' + str(x)]]
        d["Score{}".format(x)] = [y for y in match_info['Score' + str(x)]]

    ### dont think the'll ever be perfect match or whether this info is usefl... so i dont think i need it
    # d['perfect_match'] = d['Match1'] == d['legacy_original']

    ### insert legacy data column description since they requested it
    # using idx = 0 will insert at the beginning
    # df.insert(idx, col_name, value)
    d.insert(1,'legacy_description', legacy_data[legacy_des_col])

    out = pd.DataFrame(d)
    # out.to_stata(str(outFile + ".dta"))
    out.to_csv(str(outFile + ".csv"))
    # print("******************************************")
    # print("*** Your analysis has been completed! *** ")
    # print("******************************************")

    return out


