import os, pandas as pd, streamlit as st
import kagglehub

@st.cache_data(show_spinner=False)
def load_csv(local_path: str = None,
             fallback_kaggle: str = None,
             fallback_filename: str | None = None) -> pd.DataFrame:
    """Carrega CSV (local > KaggleHub > upload manual)."""
    if local_path and os.path.exists(local_path):
        return pd.read_csv(local_path)

    if fallback_kaggle and fallback_filename:
        try:
            path = kagglehub.dataset_download(fallback_kaggle)
            return pd.read_csv(os.path.join(path, fallback_filename))
        except Exception as e:
            st.info(f"⚠️ Erro no download do Kaggle – {e}")

    up = st.sidebar.file_uploader("📤 Faça upload do CSV", ["csv"])
    if up: return pd.read_csv(up)

    st.stop()  # encerra o script se nada foi encontrado


def clean_diabetes(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    return df.assign(**{c: df[c].replace(0, pd.NA) for c in cols})


def protein_percentage(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(Percentual_Proteina = (df["Protein"] * 4) / df["Calories"] * 100)
