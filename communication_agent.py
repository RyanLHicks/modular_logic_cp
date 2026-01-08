import pandas as pd

# ==========================================
# 1. SETUP (Mocking Phase 2 Output)
# ==========================================
# In a real pipeline, these pass directly from the Phase 2 script.
# We manually define them here so this script is standalone executable.

delete_candidate = {
    'name': 'Home Item 34 - CozyNest Pillow',
    'metric': '$0.85 SPLI',
    'reason': 'Lowest sales efficiency in Category',
    'width': 15.0
}

add_candidate = {
    'name': 'Home Item 89 - GreenThumb Ceramic Planter',
    'metric': '$1.45 Projected SPLI',
    'reason': 'High margin trend, matches 15" dimension gap',
    'width': 15.0
}

store_context = "Store 3000 (Bentonville Supercenter)"

# ==========================================
# 2. THE AI PROMPT ENGINEER (The "Brain")
# ==========================================

def generate_strategic_comms(delete_item, add_item, context):
    """
    Constructs detailed prompts for an LLM to generate role-specific communications.
    """
    
    # PROMPT 1: The Merchant Pitch (Strategic/Financial Tone)
    merchant_prompt = f"""
    ACT AS: Senior Analyst, Assortment Activation.
    TASK: Write a justification email to the Category Manager.
    CONTEXT: We are optimizing the Assortment for {context}.
    ACTION: Remove '{delete_item['name']}' ({delete_item['metric']}).
    REPLACE WITH: '{add_item['name']}' (Matches {add_item['width']}" gap).
    GOAL: Persuade the merchant that this improves 'Return on Space'.
    TONE: Professional, Concise, Data-Driven.
    """

    # PROMPT 2: The Store Ops Instruction (Instructional/Clear Tone)
    ops_prompt = f"""
    ACT AS: Retail Operations Specialist.
    TASK: Write a 'Modular Update Card' for the Stocking Associate.
    ACTION: Physically swap items on the shelf.
    OLD ITEM: '{delete_item['name']}' -> Remove and mark for clearance.
    NEW ITEM: '{add_item['name']}' -> Place in empty 15" gap.
    CRITICAL: Verify shelf tag alignment.
    TONE: Direct, Simple, Action-Oriented. Use Bullet points.
    """
    
    return merchant_prompt, ops_prompt

# ==========================================
# 3. THE AI SIMULATOR (The Output)
# ==========================================

def get_ai_response(prompt):
    # IN REAL LIFE: You would call openai.ChatCompletion.create() here.
    # FOR PORTFOLIO: We return a pre-written "Mock" response to show what it LOOKS like.
    
    if "Category Manager" in prompt:
        return f"""
        SUBJECT: Assortment Optimization Proposal - {store_context}
        
        Hi Team,
        
        Based on Q3 performance data, I recommend an immediate modular update for the Home category in Bentonville.
        
        The Proposal:
        We are currently allocating 15 inches of shelf space to '{delete_candidate['name']}', which is yielding only {delete_candidate['metric']}. This is performing 40% below category average.
        
        The Solution:
        I propose swapping this for '{add_candidate['name']}'.
        1. Fit Compliance: Matches the exact 15" gap (No shelf moves required).
        2. Upside: Based on regional trends, we project a margin lift of 15%.
        
        Please approve this swap by EOD Friday for execution next week.
        """
        
    elif "Stocking Associate" in prompt:
        return f"""
        [MODULAR UPDATE TASK CARD]
        LOCATION: Home Department, Aisle 12, Section 4
        
        1. REMOVE:
           [ ] '{delete_candidate['name']}'
           -> Action: Pull all units and apply yellow 'Clearance' stickers. Move to Flex Aisle.
           
        2. CLEAN:
           [ ] Wipe down the empty 15-inch shelf section.
           
        3. SET:
           [ ] Place '{add_candidate['name']}'
           -> Facings: 1 Row (Fits exactly).
           -> Alignment: Align left edge with shelf notch.
           
        4. TAG:
           [ ] Print and set new shelf label (UPC ends in 89).
        """

# ==========================================
# 4. EXECUTION
# ==========================================

m_prompt, o_prompt = generate_strategic_comms(delete_candidate, add_candidate, store_context)

print(">>> GENERATING MERCHANT PITCH (Strategic Insights)...")
print(get_ai_response(m_prompt))
print("-" * 50)
print(">>> GENERATING OPS INSTRUCTIONS (Training Materials)...")
print(get_ai_response(o_prompt))