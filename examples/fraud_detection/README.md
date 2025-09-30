# Fraud detection

- Some event systems collect data (transaction to be authorized and processed).
- We can run each individual transaction through some simple fraud detection algorithm:
  - this can be either a unsupervised machine learning algorithm (outlier detection + xgboost style)
  - some supervised algorithms (vae properly trained on hard and soft positives)
- agent can be responsible for a subset of transactions (allow scaling out), elasticity, and managing latency
  - run base model when transactions are received
  - run more complex analysis as well
  - some time series or graph analysis can occur for more complex pattern detections.
  - all agents can be either tools or other agents, we collect log and ask the main agent to explain the decision.
    - if agents are properly documented, it can generate a decent digest of why a certain transaction has been flagged
    - agents can escalade to limit, block, trigger a human review etc.., no need for real intelligence there but rather business role
    - could have a risk score computed
  - other judge such as compliance judge can be triggered as lower priority jobs


## General Concerns

- Versioning models
- Evaluating models
- Retraining models
- Eventually deploying on test users
- Full model deprecation/replacement
- Having various model baselines