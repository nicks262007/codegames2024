import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
rf_model = joblib.load("random_forest_model.joblib")

from models import ItemPayload

app = FastAPI()



# Route to find success rate
@app.post("/evals/")
def add_item(body_data: ItemPayload) -> float:
    print("body data",body_data)
    input_df = pd.DataFrame({
    "Aggregator": [body_data.Aggregator],
    "BankName": [body_data.BankName],
    "Reason": [body_data.Reason]
})  # Wrap the input data in a list to create a DataFrame
 
    # Convert categorical variables into numerical representations
    input_df = pd.get_dummies(input_df, columns=["Aggregator", "BankName", "Reason"])
 
    # Ensure that the columns and their order in input_df match the feature names used during training
    # Add missing columns if necessary
    input_final = input_df.reindex(columns=rf_model.feature_names_in_, fill_value=0)
    success_rate = rf_model.predict_proba(input_final)[0][1]

    return success_rate


   
