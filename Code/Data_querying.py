from rdflib import Graph, URIRef
# Load the ontology
g = Graph()
g.parse("composer_populated.owl", format="xml")
print(f"Ontology loaded ontology with {len(g)} triples")
print("\n -----------------------------------------------------------------------------------\n")
# Query: Get all composers whose genres contain the word "Film"
query = """
SELECT DISTINCT ?composer WHERE {
  ?composer rdf:type :Composer .
  ?composer :hasGenre ?genre .
  FILTER (regex(str(?genre), "Film", "i"))
}
"""
result = g.query(query)
print("Composers who do Film Music:")
for row in result:
    composer_name = row[0].split("/")[-1].replace("_", " ")
    print(composer_name)


print("\n -----------------------------------------------------------------------------------\n")

# Query: Get all composers who have received an award
query2 = """
SELECT DISTINCT ?composer WHERE {
  ?composer rdf:type :Composer .
  ?composer :hasAward ?award .
}
"""
result = g.query(query2)
print("Composers who have an Award:")
for row in result:
    composer_name = row[0].split("/")[-1].replace("_", " ")
    print(composer_name)

print("\n -----------------------------------------------------------------------------------\n")

from owlready2 import *

onto_path.append("coursework")

# Load the ontology
onto = get_ontology("composer_populated.owl").load()

# Get all instances of the RecordLabel class
record_labels = onto.search(type=onto.RecordLabel)

# Get the names of the record labels
record_label_names = [label.name for label in record_labels]
# Iterate over all record labels
record_labels = {}
for record_label in onto.RecordLabel.instances():
    # Get the associated composers using the hasArtist property
    composers = record_label.hasArtist
    # Save the record label and its associated composers in a dictionary
    record_labels[record_label.name] = [composer.name for composer in composers]
    target_value = ['http://example.com/composer/Anirudh_Ravichander']
    keys = [k for k, v in record_labels.items() if v == target_value] #append to a list

print("Record Labels associated with Anirudh Ravichander are:")
for key in keys:
    print(key.split("/")[-1].replace("_", " "))



