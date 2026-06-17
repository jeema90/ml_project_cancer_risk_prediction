import streamlit as st
from prediction_helper import predict_risk,prepare_df

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef5ff 0%,
        #ffffff 100%
    );
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.high-risk {
    background-color: rgba(255,75,75,0.12);
    border-left: 5px solid red;
}

.moderate-risk {
    background-color: rgba(255,193,7,0.15);
    border-left: 5px solid orange;
}

.low-risk {
    background-color: rgba(0,200,83,0.12);
    border-left: 5px solid green;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Cancer Risk Predictor",
    page_icon="🩺",
    layout="wide"
)
st.markdown(
    "<h1 style='text-align: center;'>🩺 Cancer Risk Predictor</h1>",
    unsafe_allow_html=True
)
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    text-align: center;
    color: #1f77b4;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    text-align: center;
}

.high-risk {
    background-color: rgba(255,75,75,0.15);
    border-left: 5px solid red;
}

.moderate-risk {
    background-color: rgba(255,193,7,0.15);
    border-left: 5px solid orange;
}

.low-risk {
    background-color: rgba(0,200,83,0.15);
    border-left: 5px solid green;
}

.stButton > button {
    width: 100%;
    height: 3rem;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("🩺 About")

    st.write("""
    This application predicts the mortality risk of cancer patients based on their clinical characteristics.

    ### Model Information
    - Algorithm: XGBoost
    - Target Variable: `Status`
      - 0 → Alive
      - 1 → Deceased
    - Primary Objective: Identify patients who may require closer monitoring and attention.

    ### Features Used
    - Age
    - Gender
    - Cancer Type
    - Cancer Stage
    - Treatment Type

    ### Risk Categories
    - 🟢 Low Risk: Probability < 45%
    - 🟡 Moderate Risk: Probability between 45% and 75%
    - 🔴 High Risk: Probability ≥ 70%

    ### Model Performance
    - ROC-AUC: 0.763
    - Recall: 95.2% (Threshold = 0.45)
    - F1-Score: 0.798

    ### Disclaimer
    This tool is intended for educational purposes only and should not be used as a substitute for professional medical advice or clinical decision-making.
    """,unsafe_allow_html=True)
st.divider()

with st.expander("📋 Patient Information", expanded=True):

    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(1)

    with row1[0]:
        Age = st.number_input('👤 Age', min_value=18, max_value=100, step=1)

    with row1[1]:
        Gender = st.selectbox('Gender', ['Male','Female'])
    if Gender == "Female":
            cancer_options = [
                'Cervical Cancer',
                'Colorectal Cancer',
                'Breast Cancer',
                'Leukemia',
                'Ovarian Cancer',
                'Stomach Cancer'
            ]
    else:
            cancer_options = [
                'Colorectal Cancer',
                'Breast Cancer',
                'Leukemia',
                'Prostate Cancer',
                'Stomach Cancer'
            ]

    with row2[0]:
        Cancer_Type = st.selectbox('Cancer_Type ', ['Cervical Cancer','Colorectal Cancer','Breast Cancer','Leukemia','Ovarian Cancer','Prostate Cancer','Stomach Cancer','Lung Cancer'])

    with row2[1]:
        Stage = st.selectbox('Stage', ['Stage I', 'Stage II','Stage III','Stage IV'])

    with row3[0]:
        Treatment_Type = st.selectbox('Treatment_Type', ['Chemo + Radiation','Chemotherapy','Palliative Care','Radiation','Surgery','Surgery + Chemotherapy','Targeted Therapy'])

    if st.button("🚀 Calculate Risk"):
        df = prepare_df(
            Age, Gender, Cancer_Type,Stage,Treatment_Type
        )

        with st.spinner("Analyzing details..."):
            prediction, probability,risk_level = predict_risk(df)

        st.divider()

        st.subheader("📊 Prediction Results")

        st.metric(
            "Risk Probability",
            f"{probability:.2%}"
        )

        st.progress(float(probability))

        if risk_level == "High Risk":
            st.error("""
            🔴 High Risk

            Consider closer monitoring and further clinical evaluation.
            """)

        elif risk_level == "Moderate Risk":
            st.warning("""
            🟡 Moderate Risk

            Additional assessment may be beneficial.
            """)

        else:
            st.success("""
            🟢 Low Risk

            Continue standard follow-up procedures.
            """)
    st.markdown("---")


