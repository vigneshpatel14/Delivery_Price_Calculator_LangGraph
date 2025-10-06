from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

from database import init_db, save_delivery, get_delivery, get_all_deliveries
from workflow import build_workflow, DeliveryState


init_db()
graph = build_workflow()

app = FastAPI(title="Delivery Price Calculator")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



class DeliveryRequest(BaseModel):
    """What user sends"""
    user_id: str
    material_type: str      
    distance: float         
    urgency: str           
    weight: float          
    location_type: str     

class DeliveryResponse(BaseModel):
    """What API returns"""
    success: bool
    ticket_id: str
    total_price: float
    breakdown: dict
    action_log: list
    status: str


@app.get("/")
def home():
    return {"message": "API is running!", "docs": "/docs"}

@app.post("/calculate-price", response_model=DeliveryResponse)
def calculate_price(request: DeliveryRequest):
    print(f"\n{'='*60}")
    print(f"NEW REQUEST")
    print(f"{'='*60}")
    
    
    ticket_id = f"D-{random.randint(1000, 9999)}"
    
   
    initial_state: DeliveryState = {
        "ticket_id": ticket_id,
        "user_id": request.user_id,
        "inputs": {
            "material_type": request.material_type,
            "distance": request.distance,
            "urgency": request.urgency,
            "weight": request.weight,
            "location_type": request.location_type
        },
        "base_price": 0.0,
        "material_modifier": 1.0,
        "urgency_multiplier": 1.0,
        "weight_surcharge": 0.0,
        "location_modifier": 1.0,
        "total_price": 0.0,
        "action_log": [],
        "error": None,
        "status": "pending"
    }
    
   
    final_state = graph.invoke(initial_state)
    
   
    for log in final_state["action_log"]:
        print(f"  {log}")
    
   
    save_delivery(
        ticket_id,
        request.user_id,
        request.material_type,
        request.distance,
        request.urgency,
        request.weight,
        request.location_type,
        final_state["total_price"],
        final_state["status"]
    )
    
    print(f"\nSaved to database")
    print(f" Done! Total: ${final_state['total_price']:.2f}")
    print(f"{'='*60}\n")
    

    return DeliveryResponse(
        success=True,
        ticket_id=ticket_id,
        total_price=final_state["total_price"],
        breakdown={
            "base_price": final_state["base_price"],
            "material_modifier": final_state["material_modifier"],
            "urgency_multiplier": final_state["urgency_multiplier"],
            "weight_surcharge": final_state["weight_surcharge"],
            "location_modifier": final_state["location_modifier"]
        },
        action_log=final_state["action_log"],
        status=final_state["status"]
    )

@app.get("/delivery/{ticket_id}")
def get_delivery_info(ticket_id: str):
    result = get_delivery(ticket_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "ticket_id": result[0],
        "user_id": result[1],
        "material_type": result[2],
        "distance": result[3],
        "urgency": result[4],
        "weight": result[5],
        "location_type": result[6],
        "total_price": result[7],
        "status": result[8],
        "created_at": result[9]
    }

@app.get("/deliveries")
def get_all_deliveries_list():
    results = get_all_deliveries()
    
    deliveries = []
    for result in results:
        deliveries.append({
            "ticket_id": result[0],
            "user_id": result[1],
            "material_type": result[2],
            "distance": result[3],
            "urgency": result[4],
            "weight": result[5],
            "location_type": result[6],
            "total_price": result[7],
            "status": result[8],
            "created_at": result[9]
        })
    
    return {
        "total_count": len(deliveries),
        "deliveries": deliveries
    }