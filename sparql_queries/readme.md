# SPARQL Queries

- ### Fetch all the data based on category, i.e., AmplifiedCdna  
    ```sparql
    PREFIX bican: <https://identifiers.org/brain-bican/vocab/>
    PREFIX NIMP: <http://example.org/NIMP/>
    PREFIX biolink: <https://w3id.org/biolink/vocab/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT (?s as ?ID) (?p as ?Property) (?o as ?Data)  
    WHERE {
      ?s ?p ?o.
      { 
        SELECT ?entity 
        WHERE { ?entity biolink:category bican:AmplifiedCdna. }
      } FILTER (?s = ?entity)
    }
    GROUP BY ?s ?p ?o
    ```
- ### Get property count based on category
    ```sparql
    PREFIX bican: <https://identifiers.org/brain-bican/vocab/>
    PREFIX NIMP: <http://example.org/NIMP/>
    PREFIX biolink: <https://w3id.org/biolink/vocab/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT (?s as ?ID) (COUNT(?p) as ?PropertyCount)
    WHERE {
      ?s ?p ?o.
      { 
        SELECT ?entity 
        WHERE { ?entity biolink:category bican:AmplifiedCdna. }
      } FILTER (?s = ?entity)
    }
    GROUP BY ?s
    ```
- ### Select distinct classes properties filtered based on regex expressions.
    ```sparql
    SELECT DISTINCT ?s WHERE {
      ?s ?p ?o .
      FILTER regex(STR(?s), "bican|prov|biolink")
    }
    ```
- ### Get data filtered by NIMP ID.
    ```sparql
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX NIMP: <http://example.org/NIMP/>
    select *  where {
        ?s ?p ?o.
       FILTER (?s = NIMP:LI-DDFMNG372245)
    } 
    ```
  - ### Get data where either subject, predicate or object match to BC-ABUEKB857169.
      ```sparql
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
      SELECT ?subject ?predicate ?object
      WHERE {
        { BIND(<http://example.org/NIMP/BC-ABUEKB857169> AS ?id)
          ?subject ?predicate ?id . }
        UNION
        { BIND(<http://example.org/NIMP/BC-ABUEKB857169> AS ?id)
          ?id ?predicate ?object . }
        UNION
        { BIND(<http://example.org/NIMP/BC-ABUEKB857169> AS ?id)
          ?subject ?id ?object . }
      }
      ```
- ## SPARQL query to get data of LibraryPool category
  ```sparql
  PREFIX bican: <https://identifiers.org/brain-bican/vocab/>
  PREFIX NIMP: <http://example.org/NIMP/> 
  PREFIX biolink: <https://w3id.org/biolink/vocab/> 
  PREFIX prov: <http://www.w3.org/ns/prov#> 
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
  
  SELECT ?id ?label ?local_tube_id
  WHERE {
    ?id ?p ?o.
    { 
      SELECT DISTINCT ?entity ?label ?local_tube_id
      WHERE { ?entity biolink:category bican:LibraryPool. 			
              ?entity rdfs:label ?label.
              ?entity bican:local_tube_id ?local_tube_id
          }
    } FILTER (?id = ?entity)
  }
  ```
- ## Tissue Sample
  ```sparql
  PREFIX bican: <https://identifiers.org/brain-bican/vocab/>
  PREFIX NIMP: <http://example.org/NIMP/> 
  PREFIX biolink: <https://w3id.org/biolink/vocab/> 
  PREFIX prov: <http://www.w3.org/ns/prov#> 
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
  
  SELECT ?id ?label ?structure
  WHERE {
    ?id ?p ?o.
    { 
      SELECT DISTINCT ?entity ?label ?structure
      WHERE { ?entity biolink:category bican:TissueSample.  
              ?entity rdfs:label ?label.
              ?entity bican:structure ?structure.
          }
    } FILTER (?id = ?entity)
  }
  ```
  - ## GET doner and tissue sample as well as the intermediate hops count
  ```sparql
  PREFIX BICAN: <https://identifiers.org/brain-bican/vocab/>
  PREFIX biolink: <https://w3id.org/biolink/vocab/> 
  PREFIX prov: <http://www.w3.org/ns/prov#> 
  PREFIX bican: <https://identifiers.org/brain-bican/vocab/>
  
  SELECT ?entity ?target ?targetType ?intermediate ?hopCount
  WHERE {
    {
      SELECT ?entity ?target ?targetType (COUNT(?mid) AS ?hopCount)
      WHERE {
        ?entity biolink:category BICAN:DissociatedCellSample.
        ?entity (prov:wasDerivedFrom)* ?mid.
        ?mid prov:wasDerivedFrom ?target.
        ?target biolink:category ?targetType.
        FILTER(?targetType IN (bican:Donor, bican:TissueSample))
      }
      GROUP BY ?entity ?target ?targetType
    }
  
    ?entity biolink:category BICAN:DissociatedCellSample.
    ?entity (prov:wasDerivedFrom)* ?intermediate.
    ?intermediate (prov:wasDerivedFrom)+ ?target.
    ?target biolink:category ?targetType.
    FILTER(?targetType IN (bican:Donor, bican:TissueSample))
  }
  ORDER BY ?entity ?hopCount
  ```
  
- ## GET doner and tissue sample as well as species value from doner and structure from tissue sample to link to GARS and ANSRS
```sparql
  PREFIX BICAN: <https://identifiers.org/brain-bican/vocab/>
  PREFIX biolink: <https://w3id.org/biolink/vocab/> 
  PREFIX prov: <http://www.w3.org/ns/prov#> 
  PREFIX bican: <https://identifiers.org/brain-bican/vocab/>
  
  SELECT ?entity ?target ?targetType ?intermediate ?species_value_for_taxon_match ?structure_value_for_tissue_sample
  WHERE {
    {
      SELECT ?entity ?target ?targetType (COUNT(?mid) AS ?hopCount)
      WHERE {
        ?entity biolink:category BICAN:DissociatedCellSample.
        ?entity (prov:wasDerivedFrom)* ?mid.
        ?mid prov:wasDerivedFrom ?target.
        ?target biolink:category ?targetType.
        FILTER(?targetType IN (bican:Donor, bican:TissueSample))
      }
      GROUP BY ?entity ?target ?targetType
    }
  
    ?entity biolink:category BICAN:DissociatedCellSample.
    ?entity (prov:wasDerivedFrom)* ?intermediate.
    ?intermediate (prov:wasDerivedFrom)+ ?target.
    ?target biolink:category ?targetType.
    FILTER(?targetType IN (bican:Donor, bican:TissueSample))
  
    OPTIONAL {
      ?target bican:species ?species_value_for_taxon_match.
      FILTER(?targetType = bican:Donor)
    }
  
    OPTIONAL {
      ?target bican:structure ?structure_value_for_tissue_sample.
      FILTER(?targetType = bican:TissueSample)
    }
  }
  ORDER BY ?entity ?hopCount

```

- ## Get GARS detail
  Use ?species_value_for_taxon_match
```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX NIMP: <http://example.org/NIMP/>
PREFIX bican: <https://identifiers.org/brain-bican/vocab/>

SELECT *
WHERE { 
    ?gar_id biolink:in_taxon ?gar_obj.
  	?gar_obj biolink:iri ?biriiri.
  	FILTER(CONTAINS(STR(?biriiri), "NCBITaxon_9544"))
}

```