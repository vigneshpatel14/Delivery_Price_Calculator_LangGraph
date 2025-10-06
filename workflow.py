from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from typing import Dict, List, Optional

class DeliveryState(TypedDict):
    ticket_id: str
    user_id: str
    inputs: Dict                    
    base_price: float               
    material_modifier: float        
    urgency_multiplier: float       
    weight_surcharge: float         
    location_modifier: float        
    total_price: float              
    action_log: List[str]           
    error: Optional[str]            
    status: str                  

def node_1_user_input(state: DeliveryState) -> DeliveryState:
    state["action_log"].append(f"Request started: {state['ticket_id']}")
    state["status"] = "processing"
    return state

def node_2_distance(state: DeliveryState) -> DeliveryState:
    distance = state["inputs"]["distance"]
    state["base_price"] = distance * 5.0
    state["action_log"].append(f"Distance: {distance}km -> Base price: ${state['base_price']:.2f}")
    return state

def node_3_material(state: DeliveryState) -> DeliveryState:
    rates = {"standard": 1.0, "fragile": 1.5, "perishable": 1.4, "heavy": 1.3}
    material = state["inputs"]["material_type"]
    state["material_modifier"] = rates.get(material, 1.0)
    state["action_log"].append(f"Material: {material} (x{state['material_modifier']})")
    return state

def node_4_urgency(state: DeliveryState) -> DeliveryState:
    rates = {"standard": 1.0, "express": 1.5, "same-day": 2.0}
    urgency = state["inputs"]["urgency"]
    state["urgency_multiplier"] = rates.get(urgency, 1.0)
    state["action_log"].append(f"Urgency: {urgency} (x{state['urgency_multiplier']})")
    return state

def node_5_weight(state: DeliveryState) -> DeliveryState:
    weight = state["inputs"]["weight"]
    state["weight_surcharge"] = max(0, (weight - 5) * 10)
    state["action_log"].append(f"Weight: {weight}kg -> Surcharge: ${state['weight_surcharge']:.2f}")
    return state

def node_6_location(state: DeliveryState) -> DeliveryState:
    rates = {"urban": 1.0, "rural": 1.2}
    location = state["inputs"]["location_type"]
    state["location_modifier"] = rates.get(location, 1.0)
    state["action_log"].append(f"Location: {location} (x{state['location_modifier']})")
    return state

def node_7_final_price(state: DeliveryState) -> DeliveryState:
    """Node 7: Calculate total price"""
    total = (
        state["base_price"] * 
        state["material_modifier"] * 
        state["urgency_multiplier"] * 
        state["location_modifier"]
    ) + state["weight_surcharge"]
    
    state["total_price"] = round(total, 2)
    state["status"] = "completed"
    state["action_log"].append(f"TOTAL PRICE: ${state['total_price']:.2f}")
    return state

def node_8_notification(state: DeliveryState) -> DeliveryState:
    state["action_log"].append(f"Notification sent to: {state['user_id']}")
    return state


def build_workflow():
    workflow = StateGraph(DeliveryState)

    workflow.add_node("user_input", node_1_user_input)
    workflow.add_node("distance", node_2_distance)
    workflow.add_node("material", node_3_material)
    workflow.add_node("urgency", node_4_urgency)
    workflow.add_node("weight", node_5_weight)
    workflow.add_node("location", node_6_location)
    workflow.add_node("final_price", node_7_final_price)
    workflow.add_node("notification", node_8_notification)
    
    workflow.set_entry_point("user_input")
    workflow.add_edge("user_input", "distance")
    workflow.add_edge("distance", "material")
    workflow.add_edge("material", "urgency")
    workflow.add_edge("urgency", "weight")
    workflow.add_edge("weight", "location")
    workflow.add_edge("location", "final_price")
    workflow.add_edge("final_price", "notification")
    workflow.add_edge("notification", END)
    
    return workflow.compile()