import nlp_field_mapping as nfm
import os

"""
BASIC FILES/PATHS WHOSE USE IS REPEATED
"""

# -- Replace below path with your correct directory structure
baseDir = "/Users/yisilala/Documents/IBM/projects/schlumberger oil company/"
inDir = os.path.join(baseDir, 'data')
outDir = os.path.join(baseDir, "mapping/output")

# -- In case preferred path does not already exist
if not os.path.exists(outDir):
    os.makedirs(outDir)

"""
call the matching function
"""

sap_file = os.path.join(inDir, "sap_metadata.csv")
legacy_file = os.path.join(inDir, "legacy_metadata.csv")

# -- Directory into which matched results spreadsheet is saved
outFile = os.path.join(outDir, "field_match_based_on_description")
# match_vals = nfm.fuzzyWordMatch(sap_file, legacy_file, 'Text', 'DESCRIPTION', 'Field', 'COLUMN_NAME', outFile, 3)
match_vals = nfm.fuzzyWordMatch(legacy_file, sap_file, 'DESCRIPTION', 'Text', 'COLUMN_NAME', 'Field', outFile, 2)

# they want the descriptions in them too so
print(type(match_vals))

# outFile = os.path.join(outDir, "Column_matches")
# match_vals = districtMatch(sap_file, legacy_file, 'Field', 'COLUMN_NAME', outFile)
# print(match_vals)
# -- Alternatively, don't save as an object in the workspace
# districtMatch(sap_file, legacy_file, 'Text', 'DESCRIPTION', outFile)