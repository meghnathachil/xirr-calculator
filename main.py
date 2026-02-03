import numpy_financial as npf
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI app initialization
app = FastAPI()

# Pydantic model for input validation
class XirrInput(BaseModel):
    purchase_date: str
    purchase_amount: float
    selling_date: str
    selling_price: float

# Function to calculate XIRR
def calculate_xirr(purchase_date, purchase_amount, selling_date, selling_price):
    # Convert strings to datetime objects
    purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
    selling_date = datetime.strptime(selling_date, '%Y-%m-%d')
    
    # Calculate time difference in years
    days_diff = (selling_date - purchase_date).days / 365.25

    # Use IRR calculation instead of XIRR
    cash_flows = [-purchase_amount, selling_price]
    irr = npf.irr(cash_flows)

    # Convert IRR to annualized XIRR considering the time difference
    annual_irr = (1 + irr) ** days_diff - 1

    return annual_irr * 100

# POST endpoint to calculate XIRR
@app.post("/calculate-xirr")
async def calculate_xirr_endpoint(input_data: XirrInput):
    try:
        annual_irr = calculate_xirr(
            input_data.purchase_date,
            input_data.purchase_amount,
            input_data.selling_date,
            input_data.selling_price
        )
        return {"annualized_xirr": f"{annual_irr:.2f}%"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

