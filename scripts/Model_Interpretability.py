import shap
import lime
import numpy as np

# Load your trained model
model = XLMRobertaForTokenClassification.from_pretrained('./ner_model')

# Define a function to predict entities
def predict_fn(texts):
    inputs = tokenizer(texts, return_tensors='pt', padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    return logits.argmax(-1).numpy()

# SHAP Analysis
explainer = shap.Explainer(model, tokenizer)
shap_values = explainer([sample_text])  # Replace with your sample text

# LIME Analysis
lime_explainer = lime.lime_text.LimeTextExplainer(class_names=list(label_map.keys()))
lime_explanation = lime_explainer.explain_instance(sample_text, predict_fn, num_features=10)

# Generate reports on the findings
shap.summary_plot(shap_values)
lime_explanation.show_in_notebook(text=sample_text)
