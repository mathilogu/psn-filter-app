import streamlit as st
import pandas as pd

st.set_page_config(page_title="PSN Chemistry Filter", layout="wide")
st.title("🔍 PSN Chemistry Filter Dashboard")

uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df_psn = pd.read_excel(uploaded_file, sheet_name="PSN_DATA")
        df_dash = pd.read_excel(uploaded_file, sheet_name="Dashboard")

        elements = df_dash.iloc[0, 1:20].tolist()
        min_vals = df_dash.iloc[1, 1:20].tolist()
        max_vals = df_dash.iloc[2, 1:20].tolist()

        input_ranges = {
            e: (min_v, max_v) for e, min_v, max_v in zip(elements, min_vals, max_vals) if pd.notna(e)
        }

        st.subheader("📌 Input Chemistry Range")
        st.dataframe(pd.DataFrame(input_ranges).T.rename(columns={0: "Min", 1: "Max"}))

        df_aim = df_psn[df_psn["SPEC"] == "AIM"].copy()

        def matches(row):
            for elem, (min_v, max_v) in input_ranges.items():
                val = row.get(elem)
                if pd.notna(val):
                    if pd.notna(min_v) and val < min_v:
                        return False
                    if pd.notna(max_v) and val > max_v:
                        return False
            return True

        filtered = df_aim[df_aim.apply(matches, axis=1)]

        if not filtered.empty:
            st.success(f"✅ {len(filtered)} matching PSNs found")
            st.dataframe(filtered[["PSN_NO", "PSN_Grade"] + list(input_ranges.keys())], use_container_width=True)
        else:
            st.warning("No matches found. Try adjusting the Min/Max values.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
