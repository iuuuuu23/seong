import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from main import load_and_clean_data, detect_anomalies

def run_app():
    st.set_page_config(page_title="Hệ thống Phát hiện Giao dịch Bất thường", layout="wide")
    
    st.title("📊 Ứng dụng Phát hiện Giao dịch Bất thường (Anomaly Detection)")
    st.write("Hệ thống phân tách mã nguồn rõ ràng giữa logic thuật toán (`main.py`) và hiển thị (`web.py`).")
    
    try:
        df_raw = load_and_clean_data()
        
        # Thanh trượt cấu hình tham số mô hình ở Sidebar bên trái
        st.sidebar.header("⚙️ Cấu hình Mô hình")
        contamination = st.sidebar.slider("Tỷ lệ bất thường dự kiến (Contamination)", 0.01, 0.10, 0.05, step=0.01)
        
        # Tính toán thuật toán
        df_processed = detect_anomalies(df_raw, contamination_rate=contamination)
        anomalies = df_processed[df_processed['Status'] == 'Bất thường (Anomaly)']
        
        # Thẻ hiển thị số liệu tổng quan
        st.subheader("📋 Tổng quan dữ liệu Sổ cái")
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng số giao dịch", f"{len(df_processed):,}")
        col2.metric("Số giao dịch bất thường", f"{len(anomalies)}", delta=f"{len(anomalies)} nghi vấn", delta_color="inverse")
        col3.metric("Tỷ lệ bất thường thực tế", f"{(len(anomalies)/len(df_processed))*100:.2f}%")
        
        # Bộ lọc danh sách bảng dữ liệu
        st.markdown("---")
        st.subheader("🔍 Danh sách chi tiết giao dịch")
        filter_status = st.selectbox("Lọc danh sách theo trạng thái giao dịch:", ["Tất cả giao dịch", "Chỉ giao dịch bất thường", "Chỉ giao dịch bình thường"])
        
        if filter_status == "Chỉ giao dịch bất thường":
            st.dataframe(anomalies, use_container_width=True)
        elif filter_status == "Chỉ giao dịch bình thường":
            st.dataframe(df_processed[df_processed['Status'] == 'Bình thường'], use_container_width=True)
        else:
            st.dataframe(df_processed, use_container_width=True)
            
        # Vẽ biểu đồ trực quan hóa dữ liệu
        st.markdown("---")
        st.subheader("📉 Biểu đồ phân phối giao dịch")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(data=df_processed, x='Amount', hue='Status', multiple='stack', 
                     palette={'Bình thường': '#A0C4FF', 'Bất thường (Anomaly)': '#FF6B6B'}, bins=50, ax=ax)
        ax.set_title("Phân phối giá trị giao dịch và vùng bị mô hình gắn cờ đỏ cảnh báo")
        ax.set_xlabel("Số tiền (Amount)")
        ax.set_ylabel("Số lượng giao dịch")
        st.pyplot(fig)
        
    except FileNotFoundError:
        st.error("Lỗi: Không tìm thấy file dữ liệu tại đường dẫn `data/financial_anomaly_data.csv`.")
