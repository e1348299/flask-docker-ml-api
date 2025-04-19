# DSS5105 Assignment 2

## Question 1: ATE
### 1(a) Use linear regression to estimate the parameters α, τ , and β.
Model: Ordinary Least Squares regression using statsmodels:
GET /get_ate endpoint: Returns the Average Treatment Effect (ATE) estimated from your regression model. It helps Understand the overall average impact of treatment on engagement score, after controlling for spending.
α = 95.9662, τ = -9.1057, β = 1.5149
### 1(b) Report the estimated ATE (τ) and its statistical significance.
τ p-value = 0.0004  This is less than p-value of 0.05 thus it is statistically significant
### 1(c) Briefly explain under what assumptions τ can be given a causal interpretation.
τ from the regression model can be given a causal interpretation under the following assumptions:

1. **Conditional Independence (Unconfoundedness)**:  
   Given a corporation’s sustainability spending (X), the decision to participate in the carbon offset program (W) is independent of its potential stakeholder engagement scores (Y).  
   → Formally: W ⫫ Y(0), Y(1) | X

2. **Overlap (Common Support)**:  
   All values of X must include both treated (W = 1) and untreated (W = 0) firms.  
   → This ensures valid comparisons across treatment groups at all levels of X.

3. **Correct Model Specification**:  
   The relationship between Y, W, and X must be correctly specified in the model.  
   → Linear regression assumes additive, linear effects and no omitted confounders.

4. **Stable Unit Treatment Value Assumption (SUTVA)**:  
   Each firm’s engagement outcome (Y) is only affected by its own treatment status (W).  
   → There should be no spillover or interference between firms.

## Question 2: Codespaces, Flask, & Docker
### 2(a) Github Repository Link: https://github.com/e1348299/flask-docker-ml-api
### 2(b) Create Flask API:
Apart from the get_ate endpoint, the predict endpoint was also developed:
POST /predict endpoint: Predicts the engagement score for a new data point using the fitted regression model.Estimates what the engagement would be for a new individual or scenario with specified treatment and spending values.
### 2(c) Predicted engagement score Yi returned by your API for a corporation that participated in the carbon offset program and spent $20,000 on sustainability initiatives
Predicted engagement Score: 117.16


## Component Overview
### app.py: Flask app that fits the regression model, returns treatment effect estimates, and predicts engagement scores for new inputs.

### Dockerfile: Defines the environment and startup logic for deploying the app in a containerized form.

### requirements.txt: Lists Python dependencies needed for the app to run (Flask, numpy, pandas, statsmodels).

### Benefits of dockerisation: Docker enables consistent and portable execution by packaging the app and its environment into a container. This improves reproducibility across machines and simplifies deployment to servers or cloud platforms.

# Build the image
docker build -t treatment-effect-app .

# Run the container
docker run -v "$(pwd):/app" -p 5000:5000 treatment-effect-app

# View model coefficients and ATE significance
add /get_ate at end of browser URL to obtain require coefficients
![image](https://github.com/user-attachments/assets/e7b1cdec-7ec8-48c4-aab9-ac2191589317)

# To return the predicted stakeholder engagement score for a treated firm (W = 1) spending 20 units on sustainability.
Key in 1 and 20 into input fields as seen below:
![image](https://github.com/user-attachments/assets/79fc51e7-8d8f-4411-b34c-3c3fd8b1be96)

Output as seen below:
![image](https://github.com/user-attachments/assets/6dbb7416-a8f1-456a-a50d-58fa04a79f49)


