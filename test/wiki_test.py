from app.services.wiki import get_wiki_rev

def revision_id():
   rev_id = get_wiki_rev('Alias_(TV_series)', '20120601')
   assert rev_id == 493281697
   