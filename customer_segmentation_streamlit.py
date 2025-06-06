import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pickle

# Using menu
st.title("Customer Segmentation Project")
st.write("⚠️ ***This is a demo app. All data shown is for illustrative purposes only.***")
st.markdown(
    """
    <hr style="border: 2px solid #004c99; margin-top: 10px; margin-bottom: 25px;">
    """,
    unsafe_allow_html=True
)
menu = ["How To Use","About this Project", "Segmentation Searching", "Input New Customers"]
choice = st.sidebar.selectbox('📌 Menu', menu)
st.sidebar.markdown("---")  # Đường kẻ phân cách

st.sidebar.markdown("""**🍀 Sản phẩm được thực hiện bởi nhóm:**\\
                             1.  Mạch Cảnh Toàn\\
                             2.  Hoàng Thị Diệp
                        """)
st.sidebar.markdown("""**🎓 Giảng viên hướng dẫn:**\\
                             1.  Cô Khuất Thùy Phương
                            """)

# Đọc dữ liệu mẫu
# Load data mẫu vào session state nếu chưa có
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = pd.read_csv("cust_seg_sample.csv")
sample_data = st.session_state.sample_data

# cluster_summary = pd.read_csv("cluster_summary.csv")

if choice == 'How To Use':
    st.subheader("How To Use This Website")
    st.write("##### **🎉 Chào mừng bạn ghé thăm, vui lòng đọc hướng dẫn bên dưới để biết cách sử dụng trang web này.**")
    st.write("""
    
    ###### ❓ Chúng mình có gì?
    - **How To Use**: Hướng dẫn sử dụng thanh điều hướng.
    - **About this Project**: Giới thiệu tổng quan về dự án.
    - **Segmentation Searching**: Công cụ tìm kiếm thông tin phân khúc khách hàng dựa trên mã KH được cung cấp.
    - **Input New Customers**: Đẩy dữ liệu khách hàng mới vào hệ thống.
    
    ###### 📝 Một số thuật ngữ liên quan đến Customer Segmentation:
    - **Recency (R)**: Đo lường số ngày kể từ lần mua hàng cuối cùng (lần truy cập gần đây nhất) đến ngày giả định chung để tính toán (ví dụ: ngày hiện tại, hoặc ngày max trong danh sách giao dịch).
    - **Frequency (F)**: Đo lường số lượng giao dịch (tổng số lần mua hàng) được thực hiện trong thời gian nghiên cứu.
    - **Monetary Value (M)**: Đo lường số tiền mà mỗi khách hàng đã chi tiêu trong thời gian nghiên cứu.
        
    ###### 📢 So, let's get started!
    """)

elif choice == 'About this Project':    
    st.subheader("1. Business Understanding")
    st.write("""
    ###### Cửa hàng X kinh doanh theo mô hình cửa hàng tiện lợi với quy mô vừa và nhỏ và hướng tới đối tượng khách hàng mua lẻ là chủ yếu. Các sản phẩm đặc trưng tại cửa hàng bao gồm những sản phẩm thiết yếu như thực phẩm (rau, củ, quả, thịt, cá, trứng, sữa,...), nước giải khát, đồ gia dụng, vệ sinh nhà cửa, chăm sóc cá nhân, chăm sóc thú cưng, sản phẩm theo mùa... 

    ###### Thông qua dự án này, cửa hàng mong muốn:
    🔍 Giới thiệu sản phẩm đến đúng đối tượng khách hàng;\\
    🔍 Định hướng đúng chiến lược chăm sóc khách hàng cho từng phân khúc khách hàng;\\
    🔍 Nâng cao mức độ hài lòng của khách hàng;\\
    🔍 Bán được nhiều hàng hóa hơn và thúc đẩy tăng doanh thu.

    ###### Có thể thấy, việc sử dụng RFM để phân khúc khách hàng là một phương án khá phù hợp và đáp ứng mong muốn của doanh nghiệp nhằm giải quyết vấn đề này.
    """)    
    
    # Giới thiệu về Customer Segmentation
    st.subheader("2. Project Objective")
    # Hình ảnh minh họa
    st.image("Customer-Segmentation.jpg", caption="Customer Segmentation", use_container_width=True)
    st.write("""
    ###### Customer segmentation là một trong những nhiệm vụ nền tảng của trong quản lý khách hàng và xây dựng chiến lược tiếp thị. Bằng việc tiến hành nhóm các khách hàng lại với nhau dựa trên các đặc điểm chung, Customer Segmentation hỗ trợ doanh nghiệp nhắm tới mục tiêu khách hàng thông qua việc cá nhân hóa, tung ra các chiến dịch quảng cáo, truyền thông phù hợp, thiết kế ưu đãi hoặc khuyến mãi mới, và cũng để bán hàng.

    ###### Lợi ích của việc phân khúc khách hàng:
    ✔️ **Tiếp thị hiệu quả**: Tạo chiến dịch phù hợp từng nhóm khách hàng.\\
    ✔️ **Giữ chân khách hàng**: Chính sách đặc biệt để duy trì khách hàng trung thành.\\
    ✔️ **Cải thiện dịch vụ**: Hiểu nhu cầu để tối ưu hóa trải nghiệm khách hàng.\\
    ✔️ **Mở rộng thị trường**: Phát triển sản phẩm/dịch vụ theo sở thích khách hàng.\\
    ✔️ **Tối ưu giá**: Định giá hợp lý theo tình trạng tài chính khách hàng.\\
    ✔️ **Tăng doanh thu**: Tập trung vào phân khúc có lợi nhuận cao, giảm chi phí bán hàng.

    ###### Dự án này sử dụng model Kmeans để tiến hành phân khúc khách hàng, từ đó đề xuất những chiến lược bán hàng phù hợp.
    """)

elif choice == 'Segmentation Searching':
    # Chọn nhập mã khách hàng hoặc nhập thông tin khách hàng vào dataframe
    st.subheader("1. Customer Segment Searching")
    type = st.radio("Chọn cách nhập thông tin khách hàng", options=["Tìm kiểm theo mã khách hàng", "Tìm kiếm theo danh sách"])
    
    # Dữ liệu về chiến lược marketing
    mkt_strategy = pd.read_csv("mkt_strategies.csv", encoding='latin1') 
       
    if type == "Tìm kiểm theo mã khách hàng":
        # Nếu người dùng chọn nhập mã khách hàng
        st.write("#### Tìm kiểm theo mã khách hàng")
        # Tạo điều khiển để người dùng nhập mã khách hàng
        customer_id = st.text_input("***Vui lòng nhập mã khách hàng***", placeholder="Ví dụ: KH1000")
        # Nếu người dùng nhập mã khách hàng, thực hiện các xử lý tiếp theo
        # Đề xuất khách hàng thuộc cụm
        # In kết quả ra màn hình
        if customer_id in sample_data['Member_number'].values:
            customer_data = sample_data[sample_data['Member_number']==customer_id]
            customer_data = pd.merge(customer_data, mkt_strategy, on='Cluster', how='left')
            st.write(f"**Mã khách hàng:** {customer_id}")
            st.write("**Thông tin phân cụm:**")
            st.dataframe(customer_data)
        elif customer_id not in sample_data['Member_number'].values and customer_id!="":
            st.warning("Chưa có thông tin khách hàng trên hệ thống, vui lòng nhập lại")
            st.write("Ví dụ mã khách hàng hợp lệ: KH1000, KH1001, KH1002,...")
    
    elif type == "Tìm kiếm theo danh sách":
        st.write("#### Tìm kiểm theo danh sách")
        # Tạo thanh upload file
        uploaded_file = st.file_uploader("📂 Chọn file (có chứa mã khách hàng)", type=["csv", "xlsx"])

        # Nếu có file được tải lên
        if uploaded_file is not None:
            # Đọc dữ liệu vào DataFrame
            if uploaded_file.name.endswith('.csv'):
                customer_df = pd.read_csv(uploaded_file)
            else:
                customer_df = pd.read_excel(uploaded_file)
            # Thông báo thành công
            st.success("Dữ liệu đã được tải lên")
            # 2. Nút bấm để bắt đầu phân cụm
        
        if st.button("🚀 Lấy dữ liệu cụm"):
            # Kiểm tra customer_id có tồn tại trong dữ liệu mô hình không
            try:
                customer_df['Member_number'] = customer_df['Member_number'].astype(str)
            except Exception as e:
                st.warning("❌ Dữ liệu 'Member_number' không hợp lệ")
        
            merged_df = pd.merge(customer_df, sample_data, on="Member_number", how="left")

            # Lọc các khách hàng không có đặc trưng phù hợp
            missing_customers = merged_df[merged_df.isnull().any(axis=1)]['Member_number'].tolist()

            # Tiến hành gán cụm nếu đủ dữ liệu
            valid_data = merged_df.dropna()

            if not valid_data.empty:
                valid_data = pd.merge(valid_data, mkt_strategy, on='Cluster', how='left')
                # Dự đoán cụm
                st.success("🎉 Đã hoàn tất, bạn có thể tải file về!")
                st.dataframe(valid_data[['Member_number', 'Cluster', 'Objective', 'Suggestion']])

            if missing_customers:
                st.warning(f"⚠️ Các mã KH sau chưa có trên hệ thống: {', '.join(missing_customers)}")
    
    # Đọc data
    st.subheader("2. Customer Segmentation Summary")
    # Tổng số KH hiện tại
    total_member = sample_data['Member_number'].nunique()
    # Dữ liệu trung tâm cụm
    cluster_summary = sample_data.groupby("Cluster").agg(
    Mean_Recency=("Recency", "mean"),
    Mean_Frequency=("Frequency", "mean"),
    Mean_Monetary=("Monetary", "mean"),
    Count=("Member_number", "count")
    )
    cluster_summary["Percentage"] = (cluster_summary["Count"] / sample_data.shape[0]) * 100
    cluster_summary = cluster_summary.reset_index()
    
    st.write(f"Tổng số khách hàng trên hệ thống: {total_member}")
    st.write("Thông tin cụm:")
    st.write(cluster_summary)
    fig = px.pie(cluster_summary, names='Cluster', values='Count',
             title='Tỷ lệ khách hàng theo cụm')
    st.plotly_chart(fig)
    
    st.subheader("3. Marketing Strategies")
    st.dataframe(mkt_strategy)
    
elif choice == 'Input New Customers':
    st.write("##### Bạn muốn thêm thông tin khách hàng mới vào hệ thống, vui lòng thực hiện các bước sau")
    # Chọn input từng mã khách hàng hoặc input bằng file
    type = st.radio("Chọn cách input thông tin khách hàng", options=["Nhập 1 khách hàng mới", "Nhập 5 khách hàng mới", "Upload file khách hàng mới"])
    
    # Lấy mã số KH lớn nhất hiện tại
    num_part = sample_data['Member_number'].str.extract(r'KH(\d+)', expand=False).astype(int)
    max_id = num_part.max()
    
    # Load mô hình phân cụm KMeans từ file .pkl
    with open('kmeans_model.pkl', 'rb') as file:
        kmeans = pickle.load(file)

    #st.write("Số đặc trưng mô hình yêu cầu:", kmeans.n_features_in_)


    # Gán nhãn tên cụm
    label_map = {
        0: "Potential Loyalists",
        1: "Churned Customers",
        2: "Loyal Customers",
        3: "One-time Shoppers",
        4: "Big Spenders"
    }
    
    if type == "Nhập 1 khách hàng mới":
        if type == "Nhập 1 khách hàng mới":
            new_recency = st.number_input("***Nhập chỉ số Recency (ngày)***", min_value=1, max_value=730, step=1)
            new_frequency = st.number_input("***Nhập chỉ số Frequency (số lần mua)***", min_value=1, max_value=500, step=1)
            new_monetary = st.number_input("***Nhập chỉ số Monetary (đô)***", min_value=1, max_value=5000, step=1)

            if st.button("🚀 Xem trước và phân cụm"):
                new_id = f"KH{max_id + 1}"
                new_customer = pd.DataFrame([{"Member_number":new_id, "Recency": new_recency, "Frequency": new_frequency, "Monetary": new_monetary}])

                # Phân cụm
                X1 = new_customer.drop(columns=['Member_number'])
                clusters = kmeans.predict(X1)
                new_customer['Cluster'] = clusters
                new_customer['Cluster'] = new_customer['Cluster'].map(label_map)

                st.write("##### Xem trước")
                st.dataframe(new_customer)

                st.session_state.new_customer = new_customer

            # Nút lưu
            if 'new_customer' in st.session_state:
                if st.button("💾 Lưu khách hàng"):
                    st.session_state.sample_data = pd.concat([st.session_state.sample_data, st.session_state.new_customer], ignore_index=True)
                    st.session_state.sample_data.to_csv('cust_seg_sample.csv', index=False)
                    st.success("✅ Đã thêm khách hàng mới!")
                    st.dataframe(st.session_state.sample_data.tail())
    
    elif type == "Nhập 5 khách hàng mới":
        st.write("##### Thông tin khách hàng")
        df_customer = pd.DataFrame(columns=["Member_number", "Recency", "Frequency", "Monetary"])
        
        for i in range(5):
            st.write(f"Khách hàng {i+1}")
            new_id = f"KH{max_id + i + 1}"
            recency = st.slider("Recency", 1, 730, 100, key=f"recency_{i}")
            frequency = st.slider("Frequency", 1, 40, 5, key=f"frequency_{i}")
            monetary = st.slider("Monetary", 1, 380, 100, key=f"monetary_{i}")
            
            new_row = pd.DataFrame([{
                "Member_number": new_id,
                "Recency": recency,
                "Frequency": frequency,
                "Monetary": monetary
            }])
            df_customer = pd.concat([df_customer, new_row], ignore_index=True)

        # Phân cụm
        X = df_customer.drop(columns=['Member_number'])
        clusters = kmeans.predict(X)
        df_customer['Cluster'] = clusters
        df_customer['Cluster'] = df_customer['Cluster'].map(label_map)

        # Xem trước
        st.write("##### Xem trước")
        st.dataframe(df_customer)

        # Lưu tạm vào session_state
        st.session_state.df_customer = df_customer

        # Nút lưu
        if st.button("💾 Lưu khách hàng"):
            st.session_state.sample_data = pd.concat([st.session_state.sample_data, st.session_state.df_customer], ignore_index=True)
            st.session_state.sample_data.to_csv('cust_seg_sample.csv', index=False)
            
            # Cập nhật max_id sau khi thêm
            num_part = st.session_state.sample_data['Member_number'].str.extract(r'KH(\d+)', expand=False)
            max_id = num_part.astype(int).max()

            st.success("✅ Đã thêm khách hàng mới!")
            st.dataframe(st.session_state.sample_data.tail())
            
    else:
        # Tạo thanh upload file
        uploaded_file = st.file_uploader("📂 Chọn file (có chứa thông tin RFM)", type=["csv", "xlsx"])


        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                new_customer_df = pd.read_csv(uploaded_file)
            else:
                new_customer_df = pd.read_excel(uploaded_file)
            st.success("Dữ liệu đã được tải lên")

            if st.button("🚀 Lấy dữ liệu cụm"):
                try:
                    new_customer_df['Recency'] = new_customer_df['Recency'].astype(float)
                    new_customer_df['Frequency'] = new_customer_df['Frequency'].astype(float)
                    new_customer_df['Monetary'] = new_customer_df['Monetary'].astype(float)

                    X = new_customer_df[['Recency','Frequency','Monetary']]
                    clusters = kmeans.predict(X)
                    new_customer_df['Cluster'] = clusters
                    new_customer_df['Cluster'] = new_customer_df['Cluster'].map(label_map)

                    max_id = st.session_state.sample_data['Member_number'].str.extract(r'KH(\d+)', expand=False).astype(int).max()
                    new_customer_df['Member_number'] = ['KH' + str(i) for i in range(max_id + 1, max_id + 1 + len(new_customer_df))]
                    
                    st.session_state.new_customer_df = new_customer_df
                    st.write("##### Xem trước")
                    st.dataframe(new_customer_df)

                except Exception as e:
                    st.warning(f"❌ Xử lý lỗi: {e}")

        # Nút lưu
        if 'new_customer_df' in st.session_state:
            if st.button("💾 Lưu khách hàng"):
                st.session_state.sample_data = pd.concat([st.session_state.sample_data, st.session_state.new_customer_df], ignore_index=True)
                st.session_state.sample_data.to_csv('cust_seg_sample.csv', index=False)
                st.success("✅ Đã thêm khách hàng mới!")
                st.dataframe(st.session_state.sample_data.tail())