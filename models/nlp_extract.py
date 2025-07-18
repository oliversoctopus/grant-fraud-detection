import spacy
nlp = spacy.load("en_core_web_sm")
with open("data/budget.txt", "r") as f:
    text = f.read()
doc = nlp(text)
terms = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["MONEY", "ORG"]]
with open("data/grant_terms.txt", "w") as f:
    for term in terms:
        f.write(f"{term}\n")
print("Terms saved to data/grant_terms.txt")