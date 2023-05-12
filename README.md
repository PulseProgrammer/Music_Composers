# Music Composer Ontology

This repository presents an ontology for representing information about music composers, their songs, birthdate, birth location, genres, record labels, and awards. The ontology was designed using OWL 2 and Protege, and populated with data from various sources, including DBpedia and Wikidata.

## Source Code Files, Models, and Steps to Run the Code:
In this project, the following source code files and models are included:
1. composer.owl: The base ontology file containing the classes, object properties, and data properties designed in Protege.
2. composer_populated.owl: The populated ontology file containing instances retrieved from DBpedia and Wikidata.
3. data_population(2 Databases).py: The Python script responsible for populating the ontology with data from DBpedia and Wikidata.
4. Data_querying.py: The Python script that demonstrates querying the populated ontology using SPARQL.

### To run the code, follow these steps:
1. Install the required Python libraries, if not already installed, by running the following command: **pip install owlready2 SPARQLWrapper rdflib**
2. Ensure that the composer.owl file is in the same directory as the data_population(2 Databases).py and Data_querying.py scripts.
3. Run the data_population(2 Databases).py script to populate the ontology with data from DBpedia and Wikidata. This script will generate the composer_populated.owl file.
4. After the composer_populated.owl file has been generated, run the Data_querying.py
script to execute the SPARQL queries on the populated ontology.

## Data Sources

DBpedia and Wikidata are two of the primary data sources utilized for this ontology. DBpedia extracts structured material from Wikipedia using semantic web technologies, while Wikidata is a collaborative knowledge network containing structured data on a variety of subjects. Both sources provide valuable data related to music composers, their works, genres, record companies, and accolades. SPARQL endpoints for DBpedia and Wikidata were used to retrieve and integrate data from these sources.

## Ontology Design

The ontology design involves creating a structured representation of concepts, relationships, and properties to facilitate data integration, sharing, and reasoning. The ontology includes classes, object properties, and data properties.

### Classes

The ontology defines the following classes:
1. Award
2. BirthDate
3. BirthLocation
4. Composer
5. DeathDate
6. Genre
7. Nationality
8. RecordLabel
9. Song

Disjoint constraints have been defined on these classes to ensure that they do not overlap, ensuring a clear representation of each concept.

### Object Properties

The ontology includes the following object properties, defining relationships between instances of different classes:
1. hasAward (domain: Composer, range: Award)
2. hasBirthDate (domain: Composer, range: BirthDate)
3. hasBirthLocation (domain: Composer, range: BirthLocation)
4. hasDeathDate (domain: Composer, range: DeathDate)
5. hasGenre (domain: Song, range: Genre)
6. hasNationality (domain: Composer, range: Nationality)
7. hasComposer (domain: Song, range: Composer)
8. hasArtist (domain: Record Label, range: Composer)
9. hasRecordLabel (domain: Composer, range: Record Label)

These object properties define relationships between instances of the classes, capturing associations such as awards received by composers, birth dates and locations, genres of songs, and record labels associated with composers.

### Data Properties

The ontology includes the following data property:
1. date (range: xsd:dateTime)

This data property is used to represent specific dates, such as the birth or death date of a composer, using the XML Schema datatype "dateTime."

## Ontology Population and Queries

The given Python script demonstrates the process of populating an ontology with data from external sources and querying the ontology to retrieve specific information. The script employs several libraries to facilitate the process, including owlready2 for working with OWL ontologies in Python, SPARQLWrapper for querying SPARQL endpoints and retrieving results in JSON format, rdflib for working with RDF graphs and executing SPARQL queries on them, and urllib.parse and re for sanitizing text and constructing IRIs.

Once the ontology is populated, the second script demonstrates how to query the ontology to retrieve specific information. The rdflib library is utilized to load the ontology into an RDF graph and execute SPARQL queries on it. 

The script showcases three queries:
1. Retrieving composers who are involved in film music by filtering their associated genres.
2. Listing composers who have received awards by examining the hasAward property.
3. Finding record labels associated with a specific composer (Anirudh Ravichander) by
searching the hasArtist property of record labels

## References:
1. Noy, N. F., & McGuinness, D. L. (2001). Ontology development 101: A guide to creating your first ontology. Stanford Knowledge Systems Laboratory Technical Report KSL-01-05 and Stanford Medical Informatics Technical Report SMI-2001-0880.
2. Hitzler, P., Krötzsch, M., & Rudolph, S. (2010). Foundations of Semantic Web Technologies. CRC Press.
3. Protege. (n.d.). A free, open-source ontology editor and framework for building intelligent systems. Retrieved from https://protege.stanford.edu/
4. DBpedia. (n.d.). A crowd-sourced community effort to extract structured information from Wikipedia. Retrieved from https://wiki.dbpedia.org/
5. Wikidata. (n.d.). A free, collaborative, multilingual, secondary database, collecting structured data to provide support for Wikipedia, Wikimedia Commons, and other Wikimedia projects. Retrieved from https://www.wikidata.org/
6. OWLReady2. (n.d.). A Python module for ontology-oriented programming. Retrieved from https://owlready2.readthedocs.io/
7. SPARQLWrapper. (n.d.). A Python wrapper for the SPARQL endpoint. Retrieved from https://sparqlwrapper.readthedocs.io/
