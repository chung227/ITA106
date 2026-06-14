
# =====================================================
# ITA106 - ASSIGNMENT GIAI ĐOẠN 2
# LEARNX USER BEHAVIOR ANALYSIS
# =====================================================

# Cài thư viện:
# pip install pandas numpy matplotlib seaborn scikit-learn scipy squarify

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import squarify

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import linkage, dendrogram

# =====================================================
# 1. ĐỌC DỮ LIỆU
# =====================================================

print("Đang đọc dữ liệu...")

df = pd.read_csv("learnx_user_behavior_dataset_10M.csv")

print("\nKích thước dữ liệu:")
print(df.shape)

print("\nDanh sách cột:")
print(df.columns.tolist())

# =====================================================
# 2. LẤY MẪU 100.000 DÒNG
# =====================================================

df = df.sample(
    n=100000,
    random_state=42
)

print("\nKích thước sau khi lấy mẫu:")
print(df.shape)

# =====================================================
# 3. CHỌN THUỘC TÍNH PHÂN TÍCH
# =====================================================

features = [
    "sessions_per_week",
    "avg_session_minutes",
    "videos_watched",
    "quizzes_taken",
    "forum_posts",
    "completion_rate",
    "courses_enrolled",
    "assignments_submitted",
    "total_spent_usd"
]

# =====================================================
# 4. PHÂN TÍCH MỐI QUAN HỆ
# =====================================================

# Learning Time vs Completion Rate

plt.figure(figsize=(8,5))

sns.scatterplot(
    data=df,
    x="avg_session_minutes",
    y="completion_rate",
    alpha=0.4
)

plt.title("Learning Time vs Completion Rate")
plt.show()

# Videos Watched vs Future Purchase

plt.figure(figsize=(8,5))

sns.boxplot(
    data=df,
    x="future_purchase",
    y="videos_watched"
)

plt.title("Videos Watched vs Future Purchase")
plt.show()

# AI Recommendation vs Enrollment

plt.figure(figsize=(8,5))

sns.scatterplot(
    data=df,
    x="ai_recommend_click",
    y="ai_recommend_enroll",
    alpha=0.4
)

plt.title("AI Recommendation vs Enrollment")
plt.show()

# =====================================================
# 5. HEATMAP TƯƠNG QUAN
# =====================================================

plt.figure(figsize=(10,8))

sns.heatmap(
    df[features].corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Matrix")
plt.show()

# =====================================================
# 6. CHUẨN HÓA DỮ LIỆU
# =====================================================

X = df[features]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# =====================================================
# 7. ELBOW METHOD
# =====================================================

wcss = []

for i in range(1,11):

    km = KMeans(
        n_clusters=i,
        random_state=42,
        n_init=10
    )

    km.fit(X_scaled)

    wcss.append(
        km.inertia_
    )

plt.figure(figsize=(8,5))

plt.plot(
    range(1,11),
    wcss,
    marker="o"
)

plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")

plt.show()

# =====================================================
# 8. K-MEANS CLUSTERING
# =====================================================

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X_scaled)

# =====================================================
# 9. ĐẶT TÊN NHÓM
# =====================================================

cluster_names = {
    0: "Power Learners",
    1: "Casual Learners",
    2: "Certificate Hunters",
    3: "Passive Users"
}

df["user_group"] = (
    df["cluster"]
      .map(cluster_names)
)

print("\nSố lượng người dùng mỗi nhóm:")
print(df["user_group"].value_counts())

# =====================================================
# 10. THỐNG KÊ NHÓM
# =====================================================

cluster_summary = (
    df.groupby("user_group")[features]
      .mean()
      .round(2)
)

print("\nCluster Summary:")
print(cluster_summary)

# =====================================================
# 11. PURCHASE RATE
# =====================================================

purchase_summary = (
    df.groupby("user_group")
      ["future_purchase"]
      .mean()
      .round(3)
)

print("\nPurchase Rate:")
print(purchase_summary)

# =====================================================
# 12. CHURN RISK
# =====================================================

churn_summary = (
    df.groupby("user_group")
      ["churn_risk"]
      .mean()
      .round(3)
)

print("\nChurn Risk:")
print(churn_summary)

# =====================================================
# 13. USER SEGMENTATION VISUALIZATION
# =====================================================

plt.figure(figsize=(8,5))

sns.scatterplot(
    data=df,
    x="avg_session_minutes",
    y="completion_rate",
    hue="user_group"
)

plt.title("User Segmentation")

plt.show()

# =====================================================
# 14. STAR GLYPHS (RADAR CHART)
# =====================================================

radar_features = [
    "sessions_per_week",
    "videos_watched",
    "quizzes_taken",
    "completion_rate",
    "assignments_submitted"
]

radar_data = (
    df.groupby("user_group")[radar_features]
      .mean()
)

for group in radar_data.index:

    values = radar_data.loc[group].tolist()

    values += values[:1]

    angles = np.linspace(
        0,
        2*np.pi,
        len(radar_features),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    plt.figure(figsize=(6,6))

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        radar_features
    )

    plt.title(
        f"Star Glyph - {group}"
    )

    plt.show()

# =====================================================
# 15. TREEMAP
# =====================================================

group_count = (
    df["user_group"]
      .value_counts()
)

plt.figure(
    figsize=(10,6)
)

squarify.plot(
    sizes=group_count.values,
    label=group_count.index,
    alpha=0.8
)

plt.axis("off")

plt.title(
    "Treemap User Groups"
)

plt.show()

# =====================================================
# 16. DENDROGRAM
# =====================================================

print("\nĐang tạo Dendrogram...")

sample = X_scaled[:1000]

linked = linkage(
    sample,
    method="ward"
)

plt.figure(
    figsize=(12,6)
)

dendrogram(
    linked,
    truncate_mode="lastp",
    p=20
)

plt.title(
    "Dendrogram User Behavior"
)

plt.xlabel("Clusters")
plt.ylabel("Distance")

plt.show()

# =====================================================
# 17. XUẤT FILE KẾT QUẢ
# =====================================================

df.to_csv(
    "learnx_cluster_result.csv",
    index=False
)

print(
    "\nĐã lưu learnx_cluster_result.csv"
)

# =====================================================
# 18. PRODUCT INSIGHTS
# =====================================================

print("\n========== PRODUCT INSIGHTS ==========")

print("""
Power Learners:
- Học thường xuyên.
- Completion rate cao.
- Có khả năng mua khóa học nâng cao.

Casual Learners:
- Hoạt động ở mức trung bình.
- Học khi có nhu cầu.

Certificate Hunters:
- Thực hiện nhiều quiz.
- Quan tâm tới chứng chỉ.

Passive Users:
- Hoạt động thấp.
- Nguy cơ rời bỏ nền tảng cao.
""")

# =====================================================
# 19. PRODUCT TEAM RECOMMENDATION
# =====================================================

print("\n========== PRODUCT TEAM RECOMMENDATION ==========")

print("""
1. Power Learners
   - Gợi ý khóa học nâng cao.
   - Upsell Premium.

2. Casual Learners
   - Email nhắc học.
   - Gamification.

3. Certificate Hunters
   - Thêm huy hiệu.
   - Tăng giá trị chứng chỉ.

4. Passive Users
   - Khuyến mãi quay lại.
   - Email re-engagement.
""")

print("\n========== HOÀN THÀNH GIAI ĐOẠN 2 ==========")
