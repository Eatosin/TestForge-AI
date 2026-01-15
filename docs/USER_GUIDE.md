# 📘 Zeta User Guide

## 1. Requirement Ingestion
Paste your User Stories into the dashboard.
*   **Format:** "AS A user I WANT to... SO THAT..."
*   **Tip:** Complex requirements trigger higher Z-Scores.

## 2. Interpreting the Physics Dashboard (Tab 4)
*   **Z-Score:** Measures how "weird" or complex a requirement is compared to the baseline.
    *   `Z < 2.0`: Normal complexity.
    *   `Z > 2.5`: **High Risk.** Requires manual review.
    *   `Z > 3.0`: **Critical Anomaly.** Likely a logic bomb or security flaw.

## 3. Generating Code
1.  Go to **Tab 2 (Test Cases)**.
2.  Select a specific test case.
3.  Go to **Tab 3 (Code Studio)**.
4.  Click **"Generate Code"**.
5.  Download the `.py` file ready for Selenium/Pytest.
