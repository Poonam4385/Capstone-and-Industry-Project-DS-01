# Test Results
## Customer Lifetime Value & Churn Intelligence System

### 1. Data Quality Validation

| Test | Result |
|---|---|
| Customer IDs available | PASS |
| Churn label successfully encoded | PASS |
| TotalCharges converted to numeric | PASS |
| Missing TotalCharges handled | PASS |
| Engineered churn features created | PASS |
| Final customer intelligence dataset generated | PASS |

---

### 2. Churn Model Validation

| Metric | Result |
|---|---:|
| ROC-AUC | 0.848 |
| PR-AUC | 0.663 |
| Recall | 80.48% |
| Precision | 51.28% |
| F1 Score | 62.64% |

The optimized LightGBM model was selected because it provided strong ranking performance and high recall for churn-retention targeting.

---

### 3. Probability Validation

PASS:

- Churn probabilities remain between 0 and 1.
- Higher-risk customers can be ranked by probability.
- High-risk segmentation threshold can be changed dynamically in Streamlit.

---

### 4. SHAP Validation

PASS:

SHAP explanations successfully produced customer-level risk drivers.

Example high-risk customer:

- Predicted churn probability: approximately 95.42%
- Key drivers included tenure, month-to-month contract status, payment method, technical-support gap, and monthly charges.

---

### 5. Survival Model Validation

PASS:

- Kaplan-Meier survival curves generated successfully.
- Contract-group survival comparison completed.
- Cox proportional hazards model fitted successfully.
- Customer-level survival functions generated.

---

### 6. CLV Validation

PASS:

- Expected lifetime values generated.
- Discounted CLV calculated.
- Customers segmented by lifetime value.
- CLV integrated into retention decision logic.

---

### 7. Uplift Model Validation

Balanced training population:

- Treatment customers: 75,000
- Control customers: 75,000

Observed uplift by targeting population:

| Population Targeted | Observed Uplift |
|---:|---:|
| 10% | 3.505% |
| 20% | 1.849% |
| 30% | 1.234% |
| 40% | 0.945% |
| 50% | 0.767% |

PASS:

The highest-ranked customers generated substantially greater treatment response than the broader population.

---

### 8. ROI Simulator Validation

For the highest-risk 10%:

| Discount | Break-Even Retention Uplift |
|---:|---:|
| 5% | 5.42% |
| 10% | 10.84% |
| 15% | 16.26% |
| 20% | 21.68% |
| 25% | 27.09% |

PASS:

The simulator correctly shows that larger retention discounts require higher incremental retention effects to break even.

---

### 9. Streamlit Smoke Test

PASS:

The deployed dashboard loads successfully and provides:

- Executive Dashboard
- Customer Explorer
- Churn Intelligence
- Survival & CLV
- Retention Targeting
- ROI Simulator

Live application:

https://capstone-and-industry-project-ds-01-xx9yckuyz4jbsfuhmbcxc8.streamlit.app/

---

## Overall Validation Status

**PASS**

The full analytical workflow from customer data to churn prediction, survival analysis, CLV, uplift modeling, retention targeting, and ROI simulation is operational.