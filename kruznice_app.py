import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import fitz  # PyMuPDF
import io
from datetime import datetime

# Sidebar navigation
st.sidebar.title("Navigace")
page = st.sidebar.radio("Vyberte stránku:", ["Generátor kružnice", "O autorovi", "Export do PDF"])

# Default author info
author_name = "Filip Zouhar"
author_email = "278567@vutbr.cz"

# Page: Generátor kružnice
if page == "Generátor kružnice":
    st.title("🟠 Generátor bodů na kružnici")

    # Input parameters
    x_center = st.number_input("Souřadnice X středu kružnice [m]:", value=0.0)
    y_center = st.number_input("Souřadnice Y středu kružnice [m]:", value=0.0)
    radius = st.number_input("Poloměr kružnice [m]:", min_value=0.0, value=1.0)
    num_points = st.slider("Počet bodů na kružnici:", min_value=3, max_value=500, value=10)
    point_color = st.color_picker("Barva bodů:", "#ff0000")

    # Calculate points
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x_points = x_center + radius * np.cos(angles)
    y_points = y_center + radius * np.sin(angles)

    # Plot
    fig, ax = plt.subplots()
    circle = plt.Circle((x_center, y_center), radius, color='lightgray', fill=False)
    ax.add_artist(circle)
    ax.scatter(x_points, y_points, color=point_color)
    ax.set_aspect('equal', 'box')
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.grid(True)
    ax.set_title("Kružnice s rovnoměrně rozmístěnými body")
    ax.set_xlim(x_center - radius - 1, x_center + radius + 1)
    ax.set_ylim(y_center - radius - 1, y_center + radius + 1)

    st.pyplot(fig)

    # Store parameters for PDF export
    st.session_state['params'] = {
        "X střed": x_center,
        "Y střed": y_center,
        "Poloměr [m]": radius,
        "Počet bodů": num_points,
        "Barva bodů": point_color
    }

# Page: O autorovi
elif page == "O autorovi":
    st.title("👤 O autorovi")
    st.markdown(f"""
    **Jméno:** {author_name}  
    **Email:** {author_email}  

    ---
    **Použité technologie:**  
    - Streamlit  
    - Matplotlib  
    - NumPy  
    - PyMuPDF  
    """)

# Page: Export do PDF
elif page == "Export do PDF":
    st.title("📄 Export do PDF")

    if 'params' not in st.session_state:
        st.warning("Nejdříve vygenerujte kružnici na první stránce.")
    else:
        # Create PDF
        buffer = io.BytesIO()
        doc = fitz.open()
        page = doc.new_page()

        # Title
        page.insert_text((50, 50), "Parametry úlohy - Generátor kružnice", fontsize=14, fontname="helv", fill=(0, 0, 0))

        # Parameters
        y = 80
        for key, value in st.session_state['params'].items():
            page.insert_text((50, y), f"{key}: {value}", fontsize=12, fontname="helv", fill=(0, 0, 0))
            y += 20

        # Author info
        y += 20
        page.insert_text((50, y), f"Autor: {author_name}", fontsize=12, fontname="helv", fill=(0, 0, 0))
        y += 20
        page.insert_text((50, y), f"Kontakt: {author_email}", fontsize=12, fontname="helv", fill=(0, 0, 0))
        y += 20
        page.insert_text((50, y), f"Datum exportu: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", fontsize=12, fontname="helv", fill=(0, 0, 0))

        # Save PDF
        doc.save(buffer)
        doc.close()

        st.download_button(
            label="📥 Stáhnout PDF",
            data=buffer.getvalue(),
            file_name="kruznice_parametry.pdf",
            mime="application/pdf"
        )
