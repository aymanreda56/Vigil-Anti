import features
import helpers
import os
import re
import sys
import json

file_Path = sys.argv[1]
model_path = sys.argv[2]




extractor = features.PEFeatureExtractor(print_feature_warning=False)



with open (file_Path, 'rb') as f:
    PE_file = f.read()



Raw_features = extractor.raw_features(PE_file)

df_features = helpers.Preprocess_Features_into_dataframe(Raw_features)

pred = helpers.Inference(df_features, model_path)
print(f"CLASSIFICATION IS =============================================================")
print(pred)