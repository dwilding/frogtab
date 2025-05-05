#!/usr/bin/env python3

from pathlib import Path
import os

from github import Github
from feedgen.feed import FeedGenerator
import markdown


def main():
    token = os.getenv("GITHUB_TOKEN")
    repo = Github(token).get_repo(f"dwilding/frogtab")
    closed_prs = repo.get_pulls(state="closed")
    release_prs = [pr for pr in closed_prs if include_pr(pr)]
    sorted_prs = sorted(release_prs, key=lambda pr: pr.merged_at)
    feed = FeedGenerator()
    feed.id("https://frogtab.com/changes.xml")
    feed.link(href="https://frogtab.com/changes.xml", rel="self")
    feed.link(
        href="https://github.com/dwilding/frogtab/pulls?q=state%3Amerged+label%3Aserver+sort%3Acreated-desc",
        rel="alternate",
    )
    feed.title("Frogtab changes that affect server installations")
    for pr in sorted_prs:
        entry = feed.add_entry()
        entry.id(pr.html_url)
        entry.link(href=pr.html_url)
        entry.title(pr.title.removeprefix("release: "))
        entry.author(name=pr.user.name)
        entry.content(markdown.markdown(pr.body), type="html")
        entry.updated(pr.merged_at)
    feed_string = feed.atom_str(pretty=True).decode("utf-8")
    Path("/home/public/changes.xml").write_text(feed_string)


def include_pr(pr) -> bool:
    if not pr.merged:
        return False
    labels = [label.name for label in pr.labels]
    return "server" in labels


if __name__ == "__main__":
    main()
