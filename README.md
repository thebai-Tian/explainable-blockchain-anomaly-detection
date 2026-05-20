# Explainable Blockchain Anomaly Detection (PoC)
A Proof-of-Concept on Distance-Based Rule Interpolation for Ethereum Transactions**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-PoC%20Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

## Project Overview
Traditional Fuzzy Inference Systems (FIS) used in blockchain auditing often suffer from the **"Rule Sparsity Bottleneck"**, leading to catastrophic inference interruptions (system halts) when unmapped transaction patterns occur. 

This repository contains the lightweight **Proof-of-Concept (MVP)** developed to validate a purely mathematical solution: a **Kóczy-Hirota (KH) Distance-Based Interpolation Engine**. By mapping transactions into a normalized geometric space, this engine guarantees **100% logical coverage** without requiring an exhaustive expert rule base.

## Core Features
- **Dynamic Normalization Layer**: Automatically scales vastly divergent dimensions (Time Frequency & Ether Balance) into a strict `[0, 1]` closed interval via Min-Max scaling.
- **Geometric Interpolation Engine**: Calculates exact multidimensional Euclidean distances to hardcoded expert anchors (High-Risk vs. Safe).
- **Inverse Distance Weighting**: Derives a continuous mathematical `Risk_Score` for every single transaction, neutralizing blind spots.
- **O(N) Complexity Scanning**: Successfully processed 9,841 real Ethereum transactions without a single logical gap.

## Repository Structure
```text
.
├── anomaly_detector_mvp.py       # The core interpolation engine and scanning logic
├── transaction_dataset.csv       # The raw ingestion data (9,841 records)
├── High_Risk_Report.csv          # The exported list of flagged anomalous accounts
├── PoC_Research_Report_Zebai_Tian.pdf # The full IEEE academic report
└── README.md                     # You are here
