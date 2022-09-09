from monarch_py.datamodels.solr import SolrQuery
import pytest


@pytest.mark.parametrize(
    "query,query_string",
    [
        (SolrQuery(), "q=%2A%3A%2A&rows=20&start=1&facet=false"),
        (SolrQuery(rows=10), "q=%2A%3A%2A&rows=10&start=1&facet=false"),
        (SolrQuery(start=101), "q=%2A%3A%2A&rows=20&start=101&facet=false"),
        (SolrQuery(q="marfan"), "q=marfan&rows=20&start=1&facet=false"),
        (SolrQuery(facet=True, facet_fields=["category"]),
         "q=%2A%3A%2A&rows=20&start=1&facet=true&facet.field=category"),
        (SolrQuery(facet=True, facet_fields=["category", "taxon"]),
         "q=%2A%3A%2A&rows=20&start=1&facet=true&facet.field=category&facet.field=taxon"),
        (SolrQuery(filter_queries=["subject_category:\"biolink:Gene\""]),
         "q=%2A%3A%2A&rows=20&start=1&facet=false&fq=subject_category%3A%22biolink%3AGene%22"),
    ]
)
def test_query(query, query_string):
    assert query.query_string() == query_string
