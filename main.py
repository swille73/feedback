'''
Streamlit App for Feedback Analysis
'''
import pandas as pd
import streamlit as st
from rich.console import Console
import util

console = Console()
# URL of the data
URL = "https://nevarisbuild.blob.core.windows.net/exceptiontracker/feedback.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load data from a CSV file."""
    data = pd.read_csv(URL)
    return data


def init_session_state() -> None:
    '''Initialize the session state'''
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


def set_session_state(sx_message) -> None:
    '''Set the session state'''
    if not st.session_state.data_loaded:
        st.session_state.data_loaded = True
        sx_message.success("✅ Daten erfolgreich geladen")


def main():
    """Main function to run the Streamlit app."""
    # Set page config - muss als erstes kommen
    st.set_page_config(page_title="User Feedbacks",
                       page_icon="🧊", layout="centered")

    sx_message = st.empty()
    init_session_state()

    with st.spinner('Loading data...'):
        # Load data
        df_org = load_data()

    st.title('Feedback Analyse')
    st.text("Dieses Tool hilft dir, die Feedbacks der Anwender besser zu analysieren.")

    # Daten aufbereiten
    df = prepare_data(df_org.copy())
    # Sidebar
    df_filtered = sidebar(df)
    # Main content
    display_data(df_list=df_filtered, df=df)

    plot_data(df_filtered)

    set_session_state(sx_message=sx_message)


def sidebar(df: pd.DataFrame) -> pd.DataFrame:
    '''Select the product'''
    st.sidebar.title("Filter")
    filter_begeistert = st.sidebar.radio("Begeistert", ("Alle", "Ja", "Nein"))
    if filter_begeistert == "Ja":
        return df[df["Begeistert"] == "😊"]
    if filter_begeistert == "Nein":
        return df[df["Begeistert"] == ""]
    return df


def plot_data(df: pd.DataFrame) -> None:
    '''Create a scatter plot'''
    st.divider()
    try:
        st.subheader(" 📈 Grafische Darstellung")
        chart_selection = st.selectbox(
            "Auswahl Attribut", ["Anwendung", "Version"])
        df["UserState"] = df["Begeistert"].apply(
            lambda x: "Positiv" if x == "😊" else "Negativ")
        data = df.groupby([chart_selection, "UserState"]
                          ).size().unstack().fillna(0).copy()

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Spalten-Diagramm", "Linien-Diagramm", "Scatter-Diagramm", "Area-Diagramm"])
        with tab1:
            st.bar_chart(
                data=data, x_label=f"{chart_selection}", y_label="Anzahl")
        with tab2:
            st.line_chart(data=data, x_label=f"{chart_selection}", y_label="Anzahl")
        with tab3:
            st.scatter_chart(data=data, x_label=f"{chart_selection}", y_label="Anzahl", size=200)
        with tab4:
            st.area_chart(data=data, x_label=f"{chart_selection}", y_label="Anzahl")
    except (KeyError, ValueError, TypeError) as e:
        print(st.error(f"Error: {e}"))


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    '''Prepare the data'''
    # Emojis for the column "Begeistert" else "☹️"
    df["Begeistert"] = df["IsHappy"].apply(
        lambda x: "😊" if x == 1 else "")
    df["Datum"] = pd.to_datetime(df.Datum).dt.strftime('%d.%m.%Y')
    df["Message"] = df.Message.astype(str)
    # Remove leading and trailing whitespaces
    df["Message"] = df["Message"].str.strip()
    # Remove rows with Message length less than 3 and
    # text contains only digits or special characters
    df["Kunden-Feedback"] = df["Message"].apply(
        lambda x: x if len(x) > 2 and any(char.isalpha() for char in x) else None)
    # Versionen ermitteln für eine bessere Lesbarkeit
    df["Version"] = df["AppVersion"].apply(util.get_version)
    # Remove rows with missing values in the column "Kunden-Feedback"
    df.dropna(subset=["Kunden-Feedback", "Version"], inplace=True)
    # Daten bereinigen für Anwendung
    df["Anwendung"] = df["AppName"].str.replace("NEVARIS ", "")
    return df


def highlight_headers():
    '''Highlight the headers of the table'''
    return [
        {'selector': 'th', 'props': [('background-color', 'yellow')]}
    ]


def display_data(df_list: pd.DataFrame, df: pd.DataFrame) -> None:
    '''Display the most important data'''
    st.subheader('Fakten und Zahlen')
    # Header Data
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Feedbacks: ", df.shape[0])
    with col2:
        st.write("Anwendunge: ", df["Anwendung"].nunique())
    with col3:
        st.write("Versionen: ", df["Version"].nunique())

    col4, col5, col6 = st.columns(3)
    with col4:
        st.write("😊 Feedbacks: ", df["Begeistert"].value_counts()["😊"])
    with col5:
        st.write("☹️ Feedbacks: ", df["Begeistert"].value_counts()[""])
    with col6:
        st.write("Fehlende Bewertungen: ", df["Begeistert"].isna().sum())

    st.divider()
    st.subheader("📋Listen Darstellung")
    # Grid View
    styled_df = df_list[["Datum", "Anwendung", "Version", "Begeistert",
                         "Kunden-Feedback"]].style.set_table_styles(highlight_headers())
    st.dataframe(styled_df)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        console.print_exception(show_locals=True)
        st.error(f"Error: {e}")
