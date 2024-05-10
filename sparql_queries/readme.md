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