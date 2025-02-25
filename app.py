# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO


# #Set up our App
# st.set_page_config(page_title="Data sweeper", layout='wide')
# st.title("Data sweeper")
# st.write("Transform your files between CSV and Excel formatswith build-in data cleaning and visualization!")


# uploaded_files = st.file_uploader("Upload your files (CSV and Excel):", type=("csv", "xlsx"), accept_multiple_files=True)

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext = os.path.splitext(file.name)[-1].lower()
        
#         if file_ext == ".csv":
#             df = pd.read_csv(file, engine="openpyxl")
#         elif file_ext == ".xlsx":
#             df = pd.read_excel(file)
#         else:
#             st.error(f"Unsupported file type: (file_exl)")
#             continue
        
        
#     #Display info about the file
#     st.write(f"**File Name:**{file.name}")
#     st.write(f"**File Size:**{file.size/1024}")
    
#     #Show 5 rows of our df
#     st.write("PReview the Head of the Dataframe")
#     st.dataframe(df.head())

#     #Options for data cleaning
#     st.subheader("Data Cleaning Option")
#     if st.checkbox(f"Clean Data for {file.name}"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             if st.button(f"Remove Duplicates form {file.name}"):
#                 df.drop_duplicates(inplace=True)
#                 st.write("Duplicates Removed!")
        
        
#         with col2:
#             if st.button(f"Fill Missing Values for {file.name}"):
#                 numeric_cols = df.select_dtypes(include=['number']).columns
#                 df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                 st.write("Missing Value have been Filled!")
                
#     #Choose Specific Columns to Keep or Convert
#     st.subheader("Select Column To Convert")
#     columns = st.multiselect(f"Choose Column for {file.name}", df.columns, default=df.columns)
#     df = df[columns]  
    
    
#     #Create Some Visualizations
#     st.subheader("Data Visualizations")
#     if st.checkbox(f"Show Visualizations for {file.name}"):
#         st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
        
        
#     #Convert the file => CSV to Execl
#     st.subheader("Conversion Options")
#     conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"],key=file.name)
#     if st.button(f"Convert {file.name}"):
#         buffer= BytesIO()
#         if conversion_type =="CSV":
#             df.to_csv(buffer,index=False)
#             file_name = file.name.replace(file_ext, ".csv")
#             mime_type = "text/csv"
            
#         elif conversion_type == "Excel":
#             df.to_excel(buffer, index=False)
#             file_name = file.name.replace(file_ext, ".xlsx")
#             mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             buffer.seek(0)
            
            
#     #Download Button
#     st.download_button(
#         label=f"Download {file.name} as {conversion_type}",
#         data=buffer,
#         filename=file_name,
#         mime=mime_type
#     )
    
    
# st.success("All files processed!")                    













import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our App
st.set_page_config(page_title="Data sweeper", layout='wide')
st.title("Data sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV and Excel):", type=("csv", "xlsx"), accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file
        if file_ext == ".csv":
            df = pd.read_csv(file, engine="openpyxl")
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024:.2f} KB")

        # Show dataframe preview
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Filled!")

        # Choose Specific Columns
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Visualizations
        st.subheader("Data Visualizations")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # **Initialize buffer, file_name, and mime_type outside the button to avoid errors**
        buffer = None
        file_name = None
        mime_type = None

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # Ensure Excel engine is specified
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

        # Show download button only if buffer is not None
        if buffer is not None:
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed!")
