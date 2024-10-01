import shap
import torch
from lime.lime_text import LimeTextExplainer

# Function to explain predictions using SHAP
def explain_with_shap(model, tokenizer, text):
    model.eval()  # Set model to evaluation mode

    # Tokenize input
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    input_ids = inputs['input_ids']

    # Move input tensors to the same device as the model
    input_ids = input_ids.to(next(model.parameters()).device)

    # Use SHAP to explain the model's predictions
    explainer = shap.Explainer(model, input_ids)

    # Calculate SHAP values
    shap_values = explainer(input_ids)

    # Visualize SHAP explanation
    shap.initjs()
    shap.plots.text(shap_values)

# Function to explain predictions using LIME
def explain_with_lime(model, tokenizer, text, label_list):
    explainer = LimeTextExplainer(class_names=label_list)
    
    # Define a prediction function for LIME
    def predict_proba(texts):
        inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=128)
        input_ids = inputs['input_ids'].to(next(model.parameters()).device)
        with torch.no_grad():
            outputs = model(input_ids).logits
        return torch.softmax(outputs, dim=-1).cpu().numpy()

    # Generate LIME explanation
    exp = explainer.explain_instance(text, predict_proba, num_features=10)
    exp.show_in_notebook(text=True)

# Example Amharic sentences for analysis
amharic_cases = [
    "አቶ ልዑል በታክሲ ተጓዝቶ በአዲስ አበባ ወደ ስራ ሄደ።",  # Standard sentence
    "ዶክተር ጌታም በአዲስ አበባ የሕክምና ሥራ እንደሚያደርግ አውቶቡስ ተጓዝቶ ሄደ።",  # Overlapping entities
    "አንድ ተማሪ በገነት ቤተ ምህረት ተማርነው ወደ ቤተ መንግሥት ይገባሉ።",  # Ambiguous location
    "በአለም አቀፍ ባለሙያ ማን ነው? ታዋቂ ወንበር አለው።",  # Ambiguous person
    "አበል ይታወቃል። በጊዜ ውስጥ አለቃ እንደ የዋነኛ ትምህርት ይሆናል።",  # Non-specific context
    "ትምህርት ይዞ ወደ ግንባር ተጓዝቶ ተመለሰ።",  # General reference
    "አቶ ልዑል ሲወዳድም በአንድ አዲስ አበባ ማርክተር ቀን ነው።",  # Mixed entities
    "በምዕራብ የሚኖር ሴት ወደ አዳም ይሂዳል።",  # Geographic reference
    "አዲስ ሙዚቃ አዋጁ ወይም እምቅደም ይደረገዋል።",  # Musical reference
    "ምን እንደሆነ ይቀይራል? ይህ የጭንቀት ምልክት ነው።"  # Conceptual reference
]

# Perform SHAP and LIME analysis on each Amharic case
for case in amharic_cases:
    print(f"Analyzing case: {case}")
    explain_with_shap(best_model, distilbert_tokenizer, case)  # SHAP explanation
    explain_with_lime(best_model, distilbert_tokenizer, case, label_list)  # LIME explanation
