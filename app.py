from search_agent import ResearchSearchAgent
from llm import extract_query


def main():

    print("=" * 60)
    print(" AI Research Search Agent ")
    print("=" * 60)

    user_query = input("\nAsk your research question:\n")

    # Gemini extracts the topic
    query = extract_query(user_query)

    topic = query["topic"]
    count = query["count"]

    print("Topic:", topic)
    print("Number of Papers:", count)
    print("Searching arXiv, please wait...\n")

    agent = ResearchSearchAgent()
    papers = agent.search_papers(topic, count)

    if not papers:
        print("No papers were found or the search failed. Please try again later.")
        return

    print("\nFound", len(papers), "papers.\n")

    for i, paper in enumerate(papers, start=1):

        print("=" * 60)
        print(f"Paper {i}")
        print("=" * 60)

        print("Title:")
        print(paper["title"])

        print("\nAuthors:")
        print(paper["authors"])

        print("\nPublished:")
        print(paper["published"])

        print("\nAbstract:")
        print(paper["summary"])

        print("\nPDF:")
        print(paper["pdf_link"])

        print("\n")


if __name__ == "__main__":
    main()