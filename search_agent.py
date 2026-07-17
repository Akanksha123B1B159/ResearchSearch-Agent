import arxiv
import requests


class TimeoutSession(requests.Session):
    def __init__(self, timeout=10):
        super().__init__()
        self.timeout = timeout

    def get(self, url, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return super().get(url, **kwargs)


class ResearchSearchAgent:

    def __init__(self, timeout=10):
        self.timeout = timeout

    def search_papers(self, topic, max_results=5):
        try:
            max_results = int(max_results)
        except (TypeError, ValueError):
            max_results = 5

        client = arxiv.Client()
        client._session = TimeoutSession(timeout=self.timeout)

        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers = []

        try:
            for result in client.results(search):
                paper = {
                    "title": result.title,
                    "authors": ", ".join(author.name for author in result.authors),
                    "published": result.published.strftime("%d-%m-%Y"),
                    "summary": result.summary,
                    "pdf_link": result.pdf_url
                }

                papers.append(paper)
        except (requests.exceptions.RequestException, arxiv.ArxivError) as e:
            print(f"\nSearch failed: {e}")
            return []

        return papers