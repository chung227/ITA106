#bài 2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Đọc dữ liệu
df = pd.read_csv('data.csv.txt')

# Kiểm tra missing values
print("\n===== DỮ LIỆU THIẾU =====")
print(df.isnull().sum())

# Chọn cột số
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

# Điền giá trị trung bình
for col in numeric_columns:
    df[col].fillna(df[col].mean(), inplace=True)

# Kiểm tra lại
print("\n===== SAU XỬ LÝ =====")
print(df.isnull().sum())

# Kiểm tra dữ liệu trùng
print("\n===== DỮ LIỆU TRÙNG =====")
print(df.duplicated().sum())

# Xóa dữ liệu trùng
df.drop_duplicates(inplace=True)

# Boxplot trước chuẩn hóa
plt.figure(figsize=(10,5))
df[numeric_columns].boxplot()
plt.title('Boxplot trước chuẩn hóa')
plt.xticks(rotation=45)
plt.show()

# Chuẩn hóa dữ liệu
scaler = StandardScaler()

df_scaled = df.copy()
df_scaled[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Boxplot sau chuẩn hóa
plt.figure(figsize=(10,5))
df_scaled[numeric_columns].boxplot()
plt.title('Boxplot sau chuẩn hóa')
plt.xticks(rotation=45)
plt.show()

# Lưu file
df_scaled.to_csv('cleaned_data.csv', index=False)

print("\nĐã lưu cleaned_data.csv")