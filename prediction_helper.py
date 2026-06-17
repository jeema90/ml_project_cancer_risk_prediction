import joblib
import numpy as np
import pandas as pd
import sklearn
import xgboost

MODEL_PATH='artifacts/xgb_cancer_risk_model.pkl'
FEATURE_PATH='artifacts/feature_names.pkl'

model=joblib.load(MODEL_PATH)
features=joblib.load(FEATURE_PATH)


def prepare_df(Age,Gender,Cancer_Type,Stage,Treatment_Type):

  input_data={
   'Age':Age,
   'Gender_Male': 1 if Gender == 'Male' else 0,
   'Gender_Female': 1 if Gender == 'Female' else 0,
   'Cancer_Type_Cervical Cancer': 1 if Cancer_Type == 'Cervical Cancer' else 0,
   'Cancer_Type_Colorectal Cancer': 1 if Cancer_Type == 'Colorectal Cancer' else 0,
   'Cancer_Type_Breast Cancer': 1 if Cancer_Type == 'Breast Cancer' else 0,
   'Cancer_Type_Leukemia': 1 if Cancer_Type == 'Leukemia' else 0,
   'Cancer_Type_Ovarian Cancer': 1 if Cancer_Type == 'Ovarian Cancer' else 0,
   'Cancer_Type_Prostate Cancer': 1 if Cancer_Type == 'Prostate Cancer' else 0,
   'Cancer_Type_Stomach Cancer': 1 if Cancer_Type == 'Stomach Cancer' else 0,
   'Cancer_Type_Lung Cancer': 1 if Cancer_Type == 'Lung Cancer' else 0,
   'Cancer_Stage_Stage I': 1 if Stage == 'Stage I' else 0,
   'Cancer_Stage_Stage II': 1 if Stage == 'Stage II' else 0,
   'Cancer_Stage_Stage III': 1 if Stage == 'Stage III' else 0,
   'Cancer_Stage_Stage IV': 1 if Stage == 'Stage IV' else 0,
   'Treatment_Type_Chemo + Radiation': 1 if Treatment_Type == 'Personal' else 0,
   'Treatment_Type_': 1 if Treatment_Type == 'Unsecured' else 0,
   'Treatment_Type_Chemotherapy': 1 if Treatment_Type == 'Chemotherapy' else 0,
   'Treatment_Type_Palliative Care': 1 if Treatment_Type == 'Palliative Care' else 0,
   'Treatment_Type_Radiation': 1 if Treatment_Type == 'Radiation' else 0,
   'Treatment_Type_Surgery': 1 if Treatment_Type == 'Surgery' else 0,
   'Treatment_Type_Surgery + Chemotherapy': 1 if Treatment_Type == 'Surgery + Chemotherapy' else 0,
   'Treatment_Type_Targeted Therapy': 1 if Treatment_Type == 'Targeted Therapy' else 0,
  }

  df=pd.DataFrame([input_data])

  df = df.reindex(columns=features, fill_value=0)

  return df

def predict_risk(df):
    probability = model.predict_proba(df)[0][1]

    if probability >= 0.70:
        risk_level = "High Risk"
        prediction = 1

    elif probability >= 0.45:
        risk_level = "Moderate Risk"
        prediction = 1

    else:
        risk_level = "Low Risk"
        prediction = 0

    return prediction, probability,risk_level