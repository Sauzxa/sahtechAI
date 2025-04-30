import os
import re
import requests

# Import dotenv for loading environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables directly.")

# Get Groq API key from environment variables
api_key = os.environ.get("GROQ_API_KEY")

# Check if API key is available
if not api_key:
    print("Warning: GROQ_API_KEY not found in environment variables.")
    print("Please set it using the .env file or directly in your environment.")
    print("See env_setup.md for instructions.")
    # For demo purposes, use the key only if it's not defined in environment
    api_key = "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"  # This will be removed in production

# Import Groq
from groq import Groq

# Initialize Groq client
client = Groq(
    api_key=api_key,
)

# Define Agent class
class Agent:
    def __init__(self, client, system):
        self.client = client
        self.system = system
        self.messages = []
        if self.system is not None:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message=""):
        if message:
            self.messages.append({"role": "user", "content": message})
            result = self.execute()
            self.messages.append({"role": "assistant", "content": result})
            return result

    def execute(self):
        completion = self.client.chat.completions.create(
            messages=self.messages,
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content

# Mock data flag
USE_MOCK = True

# Define tools
def get_product_data(barcode: str) -> dict:
    """
    Retrieve product data by barcode.
    """
    if USE_MOCK:
        # Mock data (for testing now)
        mock_product_db = {
            "1234567890": {
                "name": "Soumam Nature Yogurt",
                "brand": "Soumam",
                "category": "Fermented dairy",
                "ingredients": ["Milk", "Partially skimmed milk", "Lactic ferments"],
                "additives": [],
                "nutrition_values": {
                    "fat": "1.5% to 2.5%",
                    "sugar": "3.5g",
                    "protein": "4g"
                },
                "nutri_score": "B",
                "eco_score": "C"
            },
            "1234568709": {
                "name": "Bimo Tango Biscuits enrobés de chocolat",
                "brand": "Bimo",
                "category": "Snacks / Biscuits",
                "ingredients": ["Milk", "Partially skimmed milk", "Cocoa", "Sugar", "Flour", "Vegetable oils", "Lactic ferments"],
                "additives": ["Preservatives", "Artificial coloring (if applicable)"],
                "nutrition_values": {
                    "fat": "1.5% to 2.5%",
                    "sugar": "3.5g",
                    "protein": "4g"
                },
                "nutri_score": "B",
                "eco_score": "C"
            }
        }
        product = mock_product_db.get(barcode)
        if product is None:
            raise ValueError(f"Product with barcode {barcode} not found.")
        return product
    else:
        # Real API call (for production)
        response = requests.get(f"https://your-backend-api.com/products/{barcode}")
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")
        return response.json()

def get_user_profile(user_id: str) -> dict:
    """
    Retrieve user profile by user ID.
    """
    if USE_MOCK:
        # Mock data
        mock_user_db = {
            "user_001": {
                "age": 22,
                "height": 178,
                "weight": 90,
                "diseases": ["milk allergy"],
                "activity_level": "active",
                "dietary_preferences": [],
                "goal": "maintain weight"
            },
            "user2": {
                "age": 23,
                "height": 182,
                "weight": 90,
                "diseases": ["iron deficiency anemia"],
                "activity_level": "active",
                "dietary_preferences": [],
                "goal": "maintain weight"
            }
        }
        profile = mock_user_db.get(user_id)
        if profile is None:
            raise ValueError(f"User profile with ID {user_id} not found.")
        return profile
    else:
        # Real API call
        response = requests.get(f"https://your-backend-api.com/users/{user_id}")
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")
        return response.json()

# List of all diseases we handle
handled_diseases = [
    "milk allergy",
    "diabetes",
    "celiac disease",
    "iron deficiency anemia",
    # Add more diseases here easily
]

def compare_product_with_user(profile: dict, product: dict) -> dict:
    """
    Analyze if the product is suitable for the user.
    """
    result = {
        "suitable": True,
        "issues": []
    }

    for disease in profile.get("diseases", []):
        disease = disease.lower()

        if disease not in handled_diseases:
            continue  # skip diseases we don't handle (optional)

        if disease == "milk allergy":
            if any("milk" in ing.lower() for ing in product["ingredients"]):
                result["suitable"] = False
                result["issues"].append("Product contains milk, dangerous for users with milk allergy.")

        elif disease == "diabetes":
            sugar_str = product["nutrition_values"].get("sugar", "0g")
            sugar_value = float(sugar_str.replace("g", "").strip())
            if sugar_value > 5:  # Example threshold for diabetic users
                result["suitable"] = False
                result["issues"].append("Product has high sugar content, not suitable for users with diabetes.")

        elif disease == "celiac disease":
            if any("gluten" in ing.lower() for ing in product["ingredients"]):
                result["suitable"] = False
                result["issues"].append("Product contains gluten, dangerous for users with celiac disease.")

        elif disease == "iron deficiency anemia":
            # Iron deficiency anemia => the user needs iron-rich food
            # If the product has low iron or no mention of iron, warn the user
            nutrition = product.get("nutrition_values", {})
            iron = nutrition.get("iron")  # Assume "iron" value in mg is included if available

            if iron is None:
                result["suitable"] = False
                result["issues"].append("Product does not provide iron information; may not be suitable for users with iron deficiency anemia.")
            else:
                iron_value = float(str(iron).replace("mg", "").strip())
                if iron_value < 2:  # Example: less than 2mg iron is considered low
                    result["suitable"] = False
                    result["issues"].append("Product is low in iron, not suitable for users with iron deficiency anemia.")

    return result

def detailed_product_report(product: dict) -> str:
    """
    Returns a human-readable summary of the product's nutritional content and ingredients.
    """
    return (
        f"📦 Product: {product['name']} ({product['brand']})\n"
        f"🏷️ Category: {product['category']}\n"
        f"🥣 Ingredients: {', '.join(product['ingredients'])}\n"
        f"🧪 Additives: {', '.join(product['additives']) if product['additives'] else 'None'}\n"
        f"🍽️ Nutrition Values: {product['nutrition_values']}\n"
        f"✅ Nutri-Score: {product.get('nutri_score', 'N/A')}\n"
        f"🌎 Eco-Score: {product.get('eco_score', 'N/A')}"
    )

def save_recommendation(result: dict) -> bool:
    """
    Save the AI's recommendation to the database or logs.
    Return True if successful.
    """
    # Example mock implementation
    print("✅ Recommendation saved:", result)
    return True

# Define agent loop
def agent_loop(max_iterations, system_prompt, user_id, barcode):
    # Initialize the agent
    agent = Agent(client, system_prompt)
    tools = {
        "get_product_data": get_product_data,
        "get_user_profile": get_user_profile,
        "compare_product_with_user": compare_product_with_user,
        "detailed_product_report": detailed_product_report
    }

    # Get user profile and product data before starting the loop
    profile = get_user_profile(user_id)
    product = get_product_data(barcode)

    # Create a query that includes user profile and product details
    query = f"User with the following details: Age: {profile['age']}, Height: {profile['height']}cm, Weight: {profile['weight']}kg, Diseases: {', '.join(profile['diseases'])}, Dietary Preferences: {', '.join(profile['dietary_preferences'])}. Can I consume the product {product['name']} by {product['brand']}? Ingredients: {', '.join(product['ingredients'])}. Nutrition: {product['nutrition_values']}."

    prompt = query
    i = 0

    while i < max_iterations:
        i += 1
        result = agent(prompt)
        print(f"\n🌀 Iteration {i}:\n{result}")

        if "PAUSE" in result and "Action" in result:
            # Robust regex: allows optional spacing, handles () if needed
            match = re.search(r"Action:\s*([a-z_]+)\s*\(?(.+?)?\)?\s*$", result, re.IGNORECASE)
            if match:
                chosen_tool = match.group(1)
                arg = match.group(2).strip().strip('"').strip("'") if match.group(2) else ""

                if chosen_tool in tools:
                    try:
                        # You can customize argument handling here based on tool
                        tool_func = tools[chosen_tool]
                        if chosen_tool == "compare_product_with_user":
                            # Use the profile and product objects directly here
                            result_tool = tool_func(profile, product)
                        else:
                            result_tool = tool_func(arg)
                        prompt = f"Observation: {result_tool}"
                    except Exception as e:
                        prompt = f"Observation: Tool execution failed - {e}"
                else:
                    prompt = "Observation: Tool not found"
            else:
                prompt = "Observation: No valid action found"

        elif "Answer" in result or "Réponse" in result:
            print("\n✅ Final Answer:")
            print(result)
            break

# Define system prompt
system_prompt = """
You are an AI agent acting as a **virtual nutritionist or doctor** within the Sahtech health application.

Your purpose is to help users determine whether scanned food products are safe and suitable for them, based on their **health profile**.

🔁 You operate in a loop using the ReAct framework:
**Thought → Action → PAUSE → Observation**
At the end of the loop, output your **final recommendation** as the Answer.

---

🧠 Behavior:
- Think like a smart and responsible medical expert.
- Be empathetic and clear – users aren't doctors.
- Always explain your reasoning step by step.
- If a product is **not suitable**, clearly explain **why** it is harmful based on the user's health profile.


---

🧩 Inputs:
- **Product Data** (from barcode scan):
  - Name, brand, category
  - Ingredients
  - Additives
  - Nutrition values
  - Nutri-Score / Eco-Score (if available)

- **User Health Profile**:
  - Age, height, weight
  - Diseases / allergies
  - Dietary preferences (vegan, halal, etc.)
  - Activity level
  - Goal (e.g., lose weight, gain muscle, maintain weight)

---

🛠️ Available Actions:
- `get_product_data(barcode)`: Retrieve product details (ingredients, additives, scores).
- `get_user_profile(user_id)`: Retrieve health profile.
- `compare_product_with_user(profile, product)`: Analyze compatibility.
- `detailed_product_report(product)`: Explain nutrition, additives, ingredients.
- `save_recommendation(result)`: Save final output.

---

📦 Sample Session:

**Question**: Barcode scanned for "Soumam Nature Yogurt".
**Product info**:
  - Category: Fermented dairy
  - Ingredients: Milk, partially skimmed milk, lactic ferments
  - Fat: 1.5% to 2.5%
  - NutriScore: B
**User Profile**:
  - Age: 22
  - Weight: 90kg
  - Activity: Yes
  - Disease: Milk allergy
  - Goal: Maintain weight

---

**Thought**: I need to check if the user's milk allergy conflicts with the ingredients in this yogurt.
**Action**: compare_product_with_user(profile, product)
**PAUSE**

→ Called again with:

**Observation**: Product contains milk proteins like casein and whey, which are known allergens. Not safe for allergic individuals.

**Thought**: Confirm if these proteins are high-risk for this condition.
**Action**: Search medical references or dietary sources.
**PAUSE**

→ Called again with:

**Observation**: Medical consensus confirms milk proteins pose a high risk of reaction for those with milk allergies, including hives, swelling, digestive issues, or anaphylaxis.

**Answer**: ❌ **No, the user cannot consume this product.**
No  , you cn=an't consume this product , because nature Soumam yogurt contains milk proteins (casein and whey), which are common allergens. For those with milk allergies, consuming dairy can trigger serious reactions. It's important to avoid all dairy-based products, including yogurt, to prevent possible allergic responses.

---

🎯 Always remember:
- Use **thought** to plan
- Use **actions** to fetch or compare data
- Use **observation** to analyze outcomes
- Give **answer** only when confident

Now begin your loop.
""".strip()

# Run the agent loop for user with milk allergy
print("===== EXAMPLE 1: USER WITH MILK ALLERGY =====")
agent_loop(max_iterations=3, system_prompt=system_prompt, user_id="user_001", barcode="1234567890")

# Run the agent loop for user with iron deficiency anemia
print("\n\n===== EXAMPLE 2: USER WITH IRON DEFICIENCY ANEMIA =====")
agent_loop(max_iterations=3, system_prompt=system_prompt, user_id="user2", barcode="1234568709") 