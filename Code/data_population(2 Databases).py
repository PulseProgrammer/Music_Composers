from owlready2 import *
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.parse import unquote
from rdflib import URIRef
import re

onto_path.append("coursework")
# Load the ontology
onto = get_ontology("composer.owl").load()


def sanitize_text(text):
    if text is None:
        return None
    temp = text.replace('&', '&amp;')
    temp = temp.replace('<', '&lt;')
    temp = temp.replace('>', '&gt;')
    temp = temp.replace('"', '&quot;')
    temp = temp.replace("'", '&apos;')
    temp = temp.replace('%20', ' ')
    return temp


def sanitized_iri(base_iri, value):
    if value is None:
        return None
    decoded_value = unquote(value)
    # Replace spaces with underscores and remove any invalid characters
    sanitized_value = re.sub(r'[^\w\s]', '', decoded_value).replace(" ", "_")
    return URIRef(base_iri + sanitized_value)


def execute_dbpedia_query():
    query = """
    SELECT ?composerName ?songName ?birthDate ?birthPlace ?deathDate ?nationality ?genre ?recordLabelName ?awardName
WHERE {
  ?composer a dbo:MusicalArtist ;
            foaf:name ?composerName .
  OPTIONAL { ?composer dbo:birthDate ?birthDate . }
  OPTIONAL { ?composer dbo:birthPlace ?birthPlace . }
  OPTIONAL { ?composer dbo:deathDate ?deathDate . }
  OPTIONAL { ?composer dbo:nationality ?nationality . }
  OPTIONAL { ?composer dbo:genre ?genre . }
  ?song dbo:musicComposer ?composer ;
        foaf:name ?songName .
  OPTIONAL {
    ?composer dbo:recordLabel ?recordLabel .
    ?recordLabel foaf:name ?recordLabelName .
  }
  OPTIONAL {
    ?composer dbo:award ?award .
    ?award foaf:name ?awardName .
  }
  FILTER regex(str(?composer), "Composer", "i")
}
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    results = sparql.query().convert()
    return results

def execute_wikidata_query():
    query = """
    SELECT ?song ?songLabel ?composer ?composerLabel ?birthDate
WHERE {
  ?song wdt:P31 wd:Q7366; # instance of song
        wdt:P86 ?composer; # has composer
        rdfs:label ?songLabel. # retrieve the label of the song
   OPTIONAL {
    ?composer wdt:P569 ?birthDate. # birth date of the composer
  }
  ?composer rdfs:label ?composerLabel. # retrieve the label of the composer
  FILTER(LANG(?songLabel) = "en" && LANG(?composerLabel) = "en") # filter for English labels
}

LIMIT 5000
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    results = sparql.query().convert()
    return results

def process_results(dbpedia_results, wikidata_results):
    combined_results = dbpedia_results["results"]["bindings"] + wikidata_results["results"]["bindings"]

    for result in combined_results:
        if "composerName" in result:
            composer_name = result["composerName"]["value"]
        elif "composerLabel" in result:
            composer_name = result["composerLabel"]["value"]
        else:
            continue

        composer_iri = sanitized_iri("http://example.com/composer/",sanitize_text(composer_name))
        composer = onto.Composer(composer_iri)

        birth_date = result.get("birthDate", {}).get("value")
        birth_place = result.get("birthPlace", {}).get("value")
        death_date = result.get("deathDate", {}).get("value")
        nationality = result.get("nationality", {}).get("value")
        genre = result.get("genre", {}).get("value")
        record_label_name = sanitized_iri("http://example.com/record_label/",sanitize_text(result.get("recordLabelName", {}).get("value")))
        award_name = sanitized_iri("http://example.com/award_name/",sanitize_text(result.get("awardName", {}).get("value")))
        song_name = result["songName"]["value"] if "songName" in result else result["songLabel"]["value"]
        song_iri = sanitized_iri("http://example.com/song/", sanitize_text(song_name))

        if birth_date is not None:
            bd = onto.BirthDate(birth_date)
            composer.hasBirthDate.append(bd)
        if birth_place is not None:
            bp = onto.BirthLocation(birth_place)
            composer.hasBirthPlace.append(bp)
        if death_date is not None:
            dd = onto.DeathDate(death_date)
            composer.hasDeathDate.append(dd)
        if nationality is not None:
            nat = onto.Nationality(nationality)
            composer.hasNationality.append(nat)
        if genre is not None:
            gen = onto.Genre(genre)
            composer.hasGenre.append(gen)

        song = onto.Song(song_iri)
        song.hasComposer.append(composer)

        if record_label_name:
            record_label = onto.RecordLabel(record_label_name)
            record_label.hasArtist.append(composer)

        if award_name:
            award = onto.Award(award_name)
            composer.hasAward.append(award)



# Execute the queries and retrieve the results
dbpedia_results = execute_dbpedia_query()
wikidata_results = execute_wikidata_query()

# Process the combined results
process_results(dbpedia_results, wikidata_results)


# Save the ontology with a new name
onto.save(file="composer_populated.owl", format="rdfxml")