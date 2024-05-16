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


    if not redis_client.hexists(f"item_id:{item_id}", "item_id"):
        raise HTTPException(status_code=404, detail="Item not found.")

    item_quantity: str | None = redis_client.hget(f"item_id:{item_id}", "quantity")

    # if quantity to be removed is higher or equal to item's quantity, delete the item
    if item_quantity is None:
        existing_quantity: int = 0
    else:
        existing_quantity: int = int(item_quantity)
    if existing_quantity <= quantity:
        item_name: str | None = redis_client.hget(f"item_id:{item_id}", "item_name")
        redis_client.hdel("item_name_to_id", f"{item_name}")
        redis_client.delete(f"item_id:{item_id}")
        return {"result": "Item deleted."}
    else:
        redis_client.hincrby(f"item_id:{item_id}", "quantity", -quantity)
        return {"result": f"{quantity} items removed."}