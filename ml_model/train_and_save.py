import joblib
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor


def model_fitting(model_name):
    model_name.fit(X_train_scaled, y_train)
    return model_name

# Paths
ROOT = Path(__file__).resolve().parent
DATA_PATH = "C:\\Users\\Tony\\PycharmProjects\\Price_Prediction_Api\\data\\Housing.csv"
OUT_DIR = ROOT / "model"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "best_pipeline.joblib"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Create a copy for preprocessing
df_processed = df.copy()

# Label encode categorical variables
label_encoders = {}
categorical_columns = df_processed.select_dtypes(include='object').columns

print("Encoding categorical variables:")
for col in categorical_columns:
    le = LabelEncoder()
    df_processed[col] = le.fit_transform(df_processed[col])
    label_encoders[col] = le
    print(f"{col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# Define features and target (matches your notebook)
FEATURES = [
    'area','bedrooms','bathrooms','stories','mainroad','guestroom',
    'basement','hotwaterheating','airconditioning','parking','prefarea',
    'furnishingstatus'
]
TARGET = 'price'

# Keep only expected columns (helps if CSV has extra)
df_processed = df_processed[FEATURES + [TARGET]].copy()

# 3) Train/test split
X = df_processed[FEATURES]
y = df_processed[TARGET]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Scaling completed!")
print(f"Scaled training data shape: {X_train_scaled.shape}")

# Models

# 1 Baseline Random Forest Model
# Train baseline Random Forest
rf_baseline = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    min_samples_split=5,
    max_depth=15
)
rfr_baseline = model_fitting(rf_baseline)
# rf_baseline.fit(X_train_scaled, y_train)
y_pred_rf_baseline = rf_baseline.predict(X_test_scaled)

# Evaluate
r2_rf_baseline = r2_score(y_test, y_pred_rf_baseline)
mae_rf_baseline = mean_absolute_error(y_test, y_pred_rf_baseline)
rmse_rf_baseline = np.sqrt(mean_squared_error(y_test, y_pred_rf_baseline))

print("=" * 50)
print("BASELINE RANDOM FOREST MODEL")
print("=" * 50)
print(f"R² Score: {r2_rf_baseline:.4f}")
print(f"MAE: {mae_rf_baseline:,.0f}")
print(f"RMSE: {rmse_rf_baseline:,.0f}")


# 2 Hyperparameter Tuning with GridSearchCV
# Define parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20, 25],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Grid search
print("Starting GridSearchCV... This may take a few minutes.")
grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1,
    verbose=1
)

grid_search = model_fitting(grid_search)
# grid_search.fit(X_train_scaled, y_train)

print("\n" + "=" * 50)
print("GRID SEARCH RESULTS")
print("=" * 50)
print(f"Best Parameters: {grid_search.best_params_}")
print(f"Best Cross-Validation R² Score: {grid_search.best_score_:.4f}")

# Evaluate tuned model
rf_tuned = grid_search.best_estimator_
y_pred_rf_tuned = rf_tuned.predict(X_test_scaled)

r2_rf_tuned = r2_score(y_test, y_pred_rf_tuned)
mae_rf_tuned = mean_absolute_error(y_test, y_pred_rf_tuned)
rmse_rf_tuned = np.sqrt(mean_squared_error(y_test, y_pred_rf_tuned))

print("\n" + "=" * 50)
print("TUNED RANDOM FOREST MODEL")
print("=" * 50)
print(f"R² Score: {r2_rf_tuned:.4f}")
print(f"MAE: {mae_rf_tuned:,.0f}")
print(f"RMSE: {rmse_rf_tuned:,.0f}")

# 3 Gradient Boost Model
# Train Gradient Boosting model
gb_model = GradientBoostingRegressor(
    n_estimators=200,
    max_depth=10,
    learning_rate=0.1,
    random_state=42
)

gb_model = model_fitting(gb_model)
# gb_model.fit(X_train_scaled, y_train)
y_pred_gb = gb_model.predict(X_test_scaled)

# Evaluate
r2_gb = r2_score(y_test, y_pred_gb)
mae_gb = mean_absolute_error(y_test, y_pred_gb)
rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))

print("=" * 50)
print("GRADIENT BOOSTING MODEL")
print("=" * 50)
print(f"R² Score: {r2_gb:.4f}")
print(f"MAE: {mae_gb:,.0f}")
print(f"RMSE: {rmse_gb:,.0f}")

# 4 XGBoost Model
# Train XGBoost model
xgb_model = XGBRegressor(
    n_estimators=200,
    max_depth=10,
    learning_rate=0.1,
    random_state=42
)

xgb_model = model_fitting(xgb_model)
# xgb_model.fit(X_train_scaled, y_train)
y_pred_xgb = xgb_model.predict(X_test_scaled)

# Evaluate
r2_xgb = r2_score(y_test, y_pred_xgb)
mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
rmse_xgb = np.sqrt(mean_squared_error(y_test, y_pred_xgb))

print("=" * 50)
print("XGBOOST MODEL")
print("=" * 50)
print(f"R² Score: {r2_xgb:.4f}")
print(f"MAE: {mae_xgb:,.0f}")
print(f"RMSE: {rmse_xgb:,.0f}")


# Create comparison dataframe
results = pd.DataFrame({
    'Model': [
        'Random Forest (Baseline)',
        'Random Forest (Tuned)',
        'Gradient Boosting',
        'XGBoost'
    ],
    'R² Score': [r2_rf_baseline, r2_rf_tuned, r2_gb, r2_xgb],
    'MAE': [mae_rf_baseline, mae_rf_tuned, mae_gb, mae_xgb],
    'RMSE': [rmse_rf_baseline, rmse_rf_tuned, rmse_gb, rmse_xgb]
})

results = results.sort_values('R² Score', ascending=False).reset_index(drop=True)
print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)
print(results.to_string(index=False))

# Select the best model
best_model_name = results.iloc[0]['Model']
print(f"Best Model: {best_model_name}")

# Get predictions from the best model
if 'Tuned' in best_model_name:
    best_model = rf_tuned
    best_predictions = y_pred_rf_tuned
elif 'XGBoost' in best_model_name:
    best_model = xgb_model
    best_predictions = y_pred_xgb
elif 'Gradient' in best_model_name:
    best_model = gb_model
    best_predictions = y_pred_gb
else:
    best_model = rf_baseline
    best_predictions = y_pred_rf_baseline


# Define preprocessing
# numeric columns (explicit)
numeric_cols = ['area','bedrooms','bathrooms','stories','parking']
# categorical columns (explicit, but these are numeric-coded in your notebook; treat them as categorical for OneHotEncoder)
categorical_cols = ['mainroad','guestroom','basement','hotwaterheating','airconditioning','prefarea','furnishingstatus']

# Defining the preprocessing for the intake data
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ],
    remainder="drop"
)

# Build the pipeline with a simple RandomForestRegressor (you can replace with your tuned model)
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", best_model)
])

# Fit pipeline
pipeline.fit(X_train, y_train)

# Evaluate quickly
y_pred = pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred)

print("\nQuick evaluation on test set:")
print(f"R2: {r2:.4f}  MAE: {mae:.2f}  RMSE: {rmse:.2f}")

# Save pipeline to single file
joblib.dump(pipeline, OUT_FILE)
print("Saved pipeline to:", OUT_FILE)