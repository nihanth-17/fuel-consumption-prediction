<div align="center">

# ⛽ FuelNet
### Real-Time Fuel Consumption Prediction & Driving Profile Classification

[![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)](https://java.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-FF6F00?style=for-the-badge&logo=scikit-learn&logoColor=white)]()

*An intelligent system combining Machine Learning, Python, and Java to analyze ECU data, classify driving profiles, and predict real-time fuel consumption.*

</div>

---

## 📖 About the Project

**FuelNet** is a hybrid software project inspired by the IEEE research paper: *"Machine learning for real-time fuel consumption prediction and driving profile classification based on ECU data"* (Canal, Riffel, & Gracioli).

The system leverages data extracted directly from a vehicle's Electronic Control Unit (ECU) via the CAN bus (CCP protocol) to:
1. **Classify** driving behavior as fuel-friendly (eco) or non-eco-friendly.
2. **Predict** instantaneous fuel consumption using regression models.

This repository contains the data pipeline, the Machine Learning implementation, and the Java components for the FuelNet application.

---

## ✨ Key Features

- 🧠 **ML-Powered Predictions**: Implements Ridge Regression, Support Vector Regression (SVR), and XGBoost to predict fuel consumption.
- 🚗 **Driving Profile Classification**: Uses K-Means, Logistic Regression, and XGBoost to classify driver behavior.
- ☕ **Java Application**: A robust cross-platform application (`FuelNet` / `java-fuelnet`) for end-user interaction.
- 📊 **Feature Selection Pipeline**: Python scripts (`dataset_creator.py`) designed to preprocess ECU data, select features, and train the models.

---

## 🗂️ Repository Structure

| Directory / File | Description |
| :--- | :--- |
| **`FuelNet/`** & **`java-fuelnet/`** | Java-based application components. |
| **`fuelapp/`** | Dedicated fuel tracking application components. |
| **`Machine_learning_...pr.pdf`** | The foundational IEEE research paper detailing the ML methodology. |
| **`dataset/`** | Raw and processed datasets used for training the ML models. |
| **`Database/`** | SQL scripts and database schema for storing records. |
| **`dataset_creator.py`** | Python script to generate, clean, and prepare the ECU dataset. |
| **`manage.py`** | Python backend management script (likely for serving predictions). |
| **`Req.txt`** | Python package dependencies. |

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Frontend / App** | Java (JavaFX / Swing / Console) |
| **Backend** | Python (Django / Flask) |
| **Machine Learning** | Python, Pandas, NumPy, Scikit-Learn, XGBoost |
| **Database** | SQL (MySQL / SQLite) |

---

## 📊 Research Reference

This project implements models from:
> R. Canal, F. K. Riffel, and G. Gracioli, *"Machine learning for real-time fuel consumption prediction and driving profile classification based on ECU data,"* IEEE Access, 2023.

The ML models evaluate data using metrics like Mean Square Error (MSE), Mean Absolute Error (MAE), and R-squared (R²).

---

## 🤝 Contributing
Contributions are welcome! Please fork the repo and submit a pull request.

## 📜 License
This project is open-source and available for educational and research purposes.

---
<div align="center">
  <b>Developed by <a href="https://github.com/nihanth-17">Nihanth</a></b>
</div>
