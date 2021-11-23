from app.services.wiki import get_wiki_rev

from datetime import datetime

def test_revision_id():
    rev_id = get_wiki_rev('Alias_(TV_series)', datetime(2012, 6, 1))
    assert rev_id == 493281697
