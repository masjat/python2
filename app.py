import streamlit as st
import cv2
from pyzbar.pyzbar import decode

class QRScannerApp:
    def __init__(self):
        self.initialize_session_state()
        self.title = "AMIKOM PARKIR"
        self.frame_window = st.image([])

    def initialize_session_state(self):
        if 'qr_data' not in st.session_state:
            st.session_state.qr_data = ""
        if 'vehicle_number' not in st.session_state:
            st.session_state.vehicle_number = ""
        if 'vehicle_brand' not in st.session_state:
            st.session_state.vehicle_brand = ""
        if 'page' not in st.session_state:
            st.session_state.page = "Scan QR KTM"
        if 'data' not in st.session_state:
            st.session_state.data = []
        if 'run' not in st.session_state:
            st.session_state.run = False
        if 'search_number_text' not in st.session_state:
            st.session_state.search_number_text = ""
        if 'search_number' not in st.session_state:
            st.session_state.search_number = False

    def reset_state(self):
        st.session_state.qr_data = ""
        st.session_state.vehicle_number = ""
        st.session_state.vehicle_brand = ""

    def decode_qr(self, frame):
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qr_codes = decode(gray_img)
        return qr_codes

    def scan_qr_page(self):
        st.write("Scan QR KTM")

        st.session_state.run = st.checkbox('Jalankan QR Scan', value=st.session_state.run)
        if st.session_state.run:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Cannot open camera. Please make sure you have given camera permissions and no other application is using the camera.")
            else:
                while st.session_state.run:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Failed to grab frame")
                        break

                    qr_codes = self.decode_qr(frame)
                    if qr_codes:
                        for qr_code in qr_codes:
                            st.session_state.qr_data = qr_code.data.decode("utf-8")
                            st.write("QR Code Data:", st.session_state.qr_data)
                            st.session_state.run = False  # Stop the loop after reading the QR code
                            break

                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.frame_window.image(rgb_frame)

                cap.release()

    def input_data_page(self):
        st.write("Input Data Kendaraan")

        if st.session_state.qr_data:
            st.write("QR Code Data:", st.session_state.qr_data)

            st.session_state.vehicle_number = st.text_input("No Kendaraan", st.session_state.vehicle_number)
            st.session_state.vehicle_brand = st.text_input("Merk Kendaraan", st.session_state.vehicle_brand)

            if st.button("Lanjut Simpan"):
                if st.session_state.vehicle_number and st.session_state.vehicle_brand:
                    st.write("Data Berhasil diInputkan!")
                    st.write("No Kendaraan:", st.session_state.vehicle_number)
                    st.write("Merk Kendaraan:", st.session_state.vehicle_brand)
                    st.write("QR Code Data:", st.session_state.qr_data)

                    # Save the data
                    st.session_state.data.append({
                        'qr_data': st.session_state.qr_data,
                        'vehicle_number': st.session_state.vehicle_number,
                        'vehicle_brand': st.session_state.vehicle_brand
                    })

                    self.reset_state()
        else:
            st.write("Silakan pindai QR Code terlebih dahulu di halaman 'Scan QR KTM'.")

    def search_data_page(self):
        st.write("Cari Data Kendaraan")

        search_number = st.checkbox("Cari berdasarkan No Kendaraan", value=st.session_state.search_number)
        st.session_state.search_number = search_number

        if search_number:
            st.session_state.search_number_text = st.text_input("Masukkan No Kendaraan", st.session_state.search_number_text)
        else:
            st.session_state.search_number_text = ""

        # Only show results if the search number checkbox is selected and text is provided
        if search_number and st.session_state.search_number_text:
            filtered_data = [
                entry for entry in st.session_state.data
                if st.session_state.search_number_text.lower() in entry['vehicle_number'].lower()
            ]
            st.subheader("Hasil Pencarian")
            if filtered_data:
                for entry in filtered_data:
                    st.write(f"QR Code Data: {entry['qr_data']}")
                    st.write(f"No Kendaraan: {entry['vehicle_number']}")
                    st.write(f"Merk Kendaraan: {entry['vehicle_brand']}")
                    st.write("---")
            else:
                st.write("Tidak ada data yang sesuai dengan kriteria pencarian.")
        else:
            st.write("Silakan pilih kriteria pencarian dan masukkan nomor kendaraan untuk mencari.")

    def view_data_page(self):
        st.write("Lihat Data Kendaraan yang Disimpan")

        if st.session_state.data:
            for entry in st.session_state.data:
                st.write(f"QR Code Data: {entry['qr_data']}")
                st.write(f"No Kendaraan: {entry['vehicle_number']}")
                st.write(f"Merk Kendaraan: {entry['vehicle_brand']}")
                st.write("---")
        else:
            st.write("Belum ada data yang disimpan.")

    def run(self):
        # Custom CSS
        st.markdown("""
            <style>
            .main {
                background-color: #3a3a4a;
            }
            .sidebar .sidebar-content {
                background-color: #003366;
                color: white;
            }
            h1 {
                color: #1f77b4;
            }
            </style>
            """, unsafe_allow_html=True)

        # Sidebar
        st.sidebar.title("Menu")
        st.sidebar.image("assets/logo.png", width=100)  # Adjust width as needed
        st.sidebar.write("Navigasi:")

        st.title(self.title)
        page = st.sidebar.radio(
            "Pilih Halaman",
            ["Scan QR KTM", "Input Data Kendaraan", "Cari Data Kendaraan", "Lihat Data Disimpan"],
            index=["Scan QR KTM", "Input Data Kendaraan", "Cari Data Kendaraan", "Lihat Data Disimpan"].index(st.session_state.page),
            format_func=lambda page: {
                "Scan QR KTM": "🔍 Scan QR KTM",
                "Input Data Kendaraan": "🚗 Input Data Kendaraan",
                "Cari Data Kendaraan": "🔍 Cari Data Kendaraan",
                "Lihat Data Disimpan": "📋 Lihat Data Disimpan"
            }[page]
        )

        if page != st.session_state.page:
            st.session_state.page = page

        if st.session_state.page == "Scan QR KTM":
            self.scan_qr_page()
        elif st.session_state.page == "Input Data Kendaraan":
            self.input_data_page()
        elif st.session_state.page == "Cari Data Kendaraan":
            self.search_data_page()
        elif st.session_state.page == "Lihat Data Disimpan":
            self.view_data_page()

if __name__ == "__main__":
    app = QRScannerApp()
    app.run()
