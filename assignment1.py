import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# ĐỌC DỮ LIỆU
df = pd.read_csv("learnx_user_behavior_dataset_10M.csv")

print("=" * 50)
print("THÔNG TIN DATASET")
print("=" * 50)

print("Số dòng:", df.shape[0])
print("Số cột:", df.shape[1])
# KIỂM TRA MISSING VALUES
print("\nMissing Values")
print(df.isnull().sum())

# ==========================
# KIỂM TRA TRÙNG LẶP
# ==========================

duplicates = df.duplicated().sum()
print("\nDuplicate Rows:", duplicates)

df.drop_duplicates(inplace=True)

# ==========================
# THỐNG KÊ MÔ TẢ
# ==========================

print("\nThống kê mô tả")
print(df.describe())

# ==========================
# BIỂU ĐỒ 1
# PHÂN PHỐI THỜI GIAN HỌC
# ==========================

plt.figure(figsize=(8,5))
sns.histplot(df["avg_session_minutes"], bins=30, kde=True)
plt.title("Distribution of Study Time")
plt.xlabel("Average Session Minutes")
plt.ylabel("Frequency")
plt.show()

# ==========================
# BIỂU ĐỒ 2
# SỐ LẦN TRUY CẬP / TUẦN
# ==========================

plt.figure(figsize=(8,5))
sns.histplot(df["sessions_per_week"], bins=20)
plt.title("Sessions Per Week")
plt.xlabel("Sessions")
plt.ylabel("Users")
plt.show()

# ==========================
# BIỂU ĐỒ 3
# COMPLETION RATE
# ==========================

plt.figure(figsize=(8,5))
sns.histplot(df["completion_rate"], bins=20)
plt.title("Completion Rate Distribution")
plt.xlabel("Completion Rate")
plt.ylabel("Users")
plt.show()

# ==========================
# BIỂU ĐỒ 4
# VIDEOS WATCHED
# ==========================

plt.figure(figsize=(8,5))
sns.boxplot(x=df["videos_watched"])
plt.title("Videos Watched Outliers")
plt.show()

# BIỂU ĐỒ 5
# TOTAL SPENT

plt.figure(figsize=(8,5))
sns.boxplot(x=df["total_spent_usd"])
plt.title("Total Spending Outliers")
plt.show()

# ==========================
# BIỂU ĐỒ 6
# HỌC NHIỀU CÓ HOÀN THÀNH CAO?
# ==========================

plt.figure(figsize=(8,5))
sns.scatterplot(
    data=df,
    x="avg_session_minutes",
    y="completion_rate"
)

plt.title("Study Time vs Completion Rate")
plt.show()

# ==========================
# BIỂU ĐỒ 7
# VIDEO XEM VS KHẢ NĂNG MUA
# ==========================

plt.figure(figsize=(8,5))
sns.boxplot(
    x="premium_purchased",
    y="videos_watched",
    data=df
)

plt.title("Videos Watched vs Premium Purchased")
plt.show()

# ==========================
# BIỂU ĐỒ 8
# CHI TIÊU THEO NHÓM
# ==========================

plt.figure(figsize=(8,5))
sns.boxplot(
    x="future_purchase",
    y="total_spent_usd",
    data=df
)

plt.title("Spending vs Future Purchase")
plt.show()

# ==========================
# PHÁT HIỆN OUTLIERS
# ==========================

Q1 = df["total_spent_usd"].quantile(0.25)
Q3 = df["total_spent_usd"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df["total_spent_usd"] < lower)
    |
    (df["total_spent_usd"] > upper)
]

print("\nSố lượng outlier spending:")
print(len(outliers))

# ==========================
# TOP NGƯỜI HỌC NHIỀU NHẤT
# ==========================

print("\nTop 10 Study Users")

top_study = df.sort_values(
    by="avg_session_minutes",
    ascending=False
)

print(
    top_study[
        [
            "user_id",
            "avg_session_minutes",
            "sessions_per_week",
            "completion_rate"
        ]
    ].head(10)
)

# ==========================
# TOP NGƯỜI CHI TIÊU NHIỀU
# ==========================

print("\nTop 10 Spending Users")

top_spending = df.sort_values(
    by="total_spent_usd",
    ascending=False
)

print(
    top_spending[
        [
            "user_id",
            "total_spent_usd",
            "premium_purchased"
        ]
    ].head(10)
)
# ==========================
# MA TRẬN TƯƠNG QUAN
# ==========================

numeric_df = df.select_dtypes(include="number")

plt.figure(figsize=(12,8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Matrix")
plt.show()