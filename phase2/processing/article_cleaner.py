import re
def clean_article(article):
    article.content = re.sub(r"\s+", " ", article.content or "").strip(); article.summary = article.summary or article.content[:600]; return article
