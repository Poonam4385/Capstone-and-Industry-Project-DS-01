# Data Dictionary
## Customer Lifetime Value & Churn Intelligence System

This document describes the major input, engineered, model-output, and business-decision fields used in the project.

---

## 1. Customer Identification

| Field | Type | Description |
|---|---|---|
| customerID | String | Unique identifier for each telecom customer |

---

## 2. Customer Profile

| Field | Type | Description |
|---|---|---|
| gender | Category | Customer gender |
| SeniorCitizen | Integer | Indicates whether the customer is a senior citizen |
| Partner | Category | Whether the customer has a partner |
| Dependents | Category | Whether the customer has dependents |
| tenure | Integer | Number of months the customer has stayed with the company |

---

## 3. Services

| Field | Type | Description |
|---|---|---|
| PhoneService | Category | Whether phone service is active |
| MultipleLines | Category | Multiple phone-line service status |
| InternetService | Category | DSL, Fiber optic, or no internet |
| OnlineSecurity | Category | Online security subscription status |
| OnlineBackup | Category | Online backup subscription status |
| DeviceProtection | Category | Device protection status |
| TechSupport | Category | Technical support subscription status |
| StreamingTV | Category | Streaming TV subscription status |
| StreamingMovies | Category | Streaming movie subscription status |

---

## 4. Billing and Contract

| Field | Type | Description |
|---|---|---|
| Contract | Category | Month-to-month, one-year, or two-year contract |
| PaperlessBilling | Category | Whether paperless billing is enabled |
| PaymentMethod | Category | Customer payment method |
| MonthlyCharges | Float | Monthly amount charged to the customer |
| TotalCharges | Float | Total charges accumulated over customer tenure |

---

## 5. Churn Target

| Field | Type | Description |
|---|---|---|
| Churn | Category | Original churn label: Yes/No |
| ChurnFlag | Integer | Binary churn target: 1 = churned, 0 = retained |

---

## 6. Engineered Features

| Field | Description |
|---|---|
| ServiceCount | Number of active telecom services |
| AvgMonthlySpend | Average historical monthly spending |
| MonthToMonthFlag | Binary indicator for month-to-month contract |
| LongTermContractFlag | Indicates one- or two-year contract |
| SupportGap | Internet customer without technical support |
| SecurityGap | Internet customer without online security |
| AutoPayment | Indicates automatic payment method |
| NewCustomer | Customer with tenure <= 6 months |
| LoyalCustomer | Customer with tenure >= 48 months |
| ChargesPerService | Monthly charges divided by number of services |
| TenureGroup | Tenure-based customer group |
| MonthlySpendGroup | Monthly-spend category |

---

## 7. Churn Model Outputs

| Field | Description |
|---|---|
| ChurnProbability | Probability of churn predicted by optimized LightGBM |
| ChurnPrediction | Binary churn decision based on chosen probability threshold |

The optimized churn model achieved approximately:

- ROC-AUC: 0.848
- PR-AUC: 0.663
- Recall: 80.48%
- Precision: 51.28%
- F1 Score: 62.64%

---

## 8. Survival Analysis Outputs

| Field | Description |
|---|---|
| ExpectedLifetimeMonths | Estimated customer lifetime derived from survival analysis |
| SurvivalProbability | Estimated probability of remaining active at a future time |

Kaplan-Meier and Cox Proportional Hazards methods were used for portfolio-level survival analysis.

---

## 9. Customer Lifetime Value Outputs

| Field | Description |
|---|---|
| EstimatedMonthlyMargin | Estimated monthly gross margin |
| BasicCLV | Undiscounted lifetime-value estimate |
| DiscountedCLV | Present-value-adjusted estimate of customer lifetime value |
| CLVSegment | Low, Medium, High, or Very High CLV segment |

---

## 10. Business Segmentation

| Field | Description |
|---|---|
| BusinessSegment | Customer segment based on churn risk and value |
| RetentionStrategy | Suggested high-level retention strategy |

Example segments:

- High-Value At-Risk
- High-Value Loyal
- Low-Value At-Risk
- Low-Value Stable

---

## 11. Retention Economics

| Field | Description |
|---|---|
| OfferCost | Estimated cost of a customer retention offer |
| ExpectedRetentionBenefit | Expected incremental financial value of retention |
| NetRetentionBenefit | Expected benefit minus offer cost |
| RetentionROI | Net financial return divided by campaign cost |
| RecommendedAction | Final action recommended by decision engine |

Possible actions include:

- SEND OFFER
- DO NOT DISCOUNT
- PROTECT / LOYALTY
- NO ACTION

---

## 12. Uplift Modeling Dataset

A separate Criteo randomized-treatment dataset was used for uplift-model methodology.

Important columns:

| Field | Description |
|---|---|
| f0-f11 | Anonymized customer/context features |
| treatment | 1 = treatment, 0 = control |
| visit | Customer visit outcome |
| conversion | Conversion outcome |
| exposure | Post-treatment exposure variable; excluded from model features |

`exposure` was deliberately excluded to avoid post-treatment data leakage.

The uplift dataset was not merged customer-by-customer with the telecom dataset because the two datasets represent different populations.

---

## 13. Uplift Model Output

| Field | Description |
|---|---|
| prob_if_treated | Predicted response probability if treated |
| prob_if_control | Predicted response probability without treatment |
| uplift_score | Difference between treated and control response probabilities |
| uplift_decile | Ranking group based on predicted treatment effect |

Observed uplift for the highest-ranked 10% was approximately 3.505 percentage points.

---

## 14. ROI Scenario Inputs

The Streamlit simulator allows users to modify:

- Discount offered
- Offer duration
- Expected incremental retention uplift
- Percentage of customers targeted

The dashboard calculates:

- Campaign cost
- Expected retained value
- Net benefit
- ROI
- Break-even retention uplift

---

## Methodological Note

The telecom dataset does not contain randomized retention-treatment data. Therefore, treatment uplift derived from the Criteo dataset is used to demonstrate uplift-model methodology rather than being directly applied as a measured telecom treatment effect.

The telecom ROI simulator treats retention uplift as a configurable business scenario assumption.