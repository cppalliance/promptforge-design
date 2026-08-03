"""Build a hand-verified seed catalog + eval set from real, well-known MCP servers.

Tool names and descriptions are taken from the public modelcontextprotocol
reference servers and popular community servers (github, filesystem, git, slack,
brave-search, google-maps, postgres, puppeteer, memory, fetch, time, sqlite).
Descriptions are paraphrased to realistic `tools/list` style.

The eval set exercises the three cases that break naive matchers:
  - positives (with several paraphrases per tool),
  - near-duplicates (two servers offering similar capabilities in one catalog),
  - hard negatives (needs with no matching tool in the given catalog).
"""

from __future__ import annotations

from common import Catalog, EvalExample, Tool, CATALOGS_DIR, EVAL_DIR, save_catalog, save_eval

# ---- Real-ish tool definitions per server -------------------------------------------------

SERVERS: dict[str, list[Tool]] = {
    "github": [
        Tool("github", "create_issue", "Create a new issue in a GitHub repository", ["owner", "repo", "title", "body"]),
        Tool("github", "create_pull_request", "Open a new pull request from a branch", ["owner", "repo", "head", "base", "title"]),
        Tool("github", "search_code", "Search for code across GitHub repositories", ["q", "sort", "order"]),
        Tool("github", "get_file_contents", "Read the contents of a file from a GitHub repository", ["owner", "repo", "path", "ref"]),
        Tool("github", "list_commits", "List commits on a branch of a repository", ["owner", "repo", "sha"]),
        Tool("github", "merge_pull_request", "Merge an open pull request", ["owner", "repo", "pull_number"]),
    ],
    "filesystem": [
        Tool("filesystem", "read_file", "Read the complete contents of a file from the local filesystem", ["path"]),
        Tool("filesystem", "write_file", "Create a new file or overwrite an existing file with content", ["path", "content"]),
        Tool("filesystem", "list_directory", "List the files and folders in a directory", ["path"]),
        Tool("filesystem", "move_file", "Move or rename a file or directory", ["source", "destination"]),
        Tool("filesystem", "search_files", "Recursively search for files matching a name pattern", ["path", "pattern"]),
        Tool("filesystem", "create_directory", "Create a new directory, including parent directories", ["path"]),
    ],
    "git": [
        Tool("git", "git_status", "Show the working tree status of a git repository", ["repo_path"]),
        Tool("git", "git_diff", "Show changes between commits or the working tree", ["repo_path", "target"]),
        Tool("git", "git_commit", "Record staged changes to the repository with a message", ["repo_path", "message"]),
        Tool("git", "git_log", "Show the commit history of a repository", ["repo_path", "max_count"]),
        Tool("git", "git_create_branch", "Create a new git branch", ["repo_path", "branch_name"]),
    ],
    "slack": [
        Tool("slack", "post_message", "Send a message to a Slack channel", ["channel_id", "text"]),
        Tool("slack", "list_channels", "List the public channels in the Slack workspace", ["limit"]),
        Tool("slack", "get_channel_history", "Fetch recent messages from a Slack channel", ["channel_id", "limit"]),
        Tool("slack", "add_reaction", "Add an emoji reaction to a message", ["channel_id", "timestamp", "reaction"]),
    ],
    "brave_search": [
        Tool("brave_search", "brave_web_search", "Search the web and return relevant results with snippets", ["query", "count"]),
        Tool("brave_search", "brave_local_search", "Search for local businesses and places", ["query", "count"]),
    ],
    "google_maps": [
        Tool("google_maps", "maps_geocode", "Convert an address into geographic coordinates", ["address"]),
        Tool("google_maps", "maps_directions", "Get travel directions between two locations", ["origin", "destination", "mode"]),
        Tool("google_maps", "maps_place_search", "Search for places near a location", ["query", "location", "radius"]),
        Tool("google_maps", "maps_distance_matrix", "Compute travel distance and time for a matrix of origins and destinations", ["origins", "destinations"]),
    ],
    "postgres": [
        Tool("postgres", "query", "Run a read-only SQL query against the connected PostgreSQL database", ["sql"]),
        Tool("postgres", "list_tables", "List the tables in the database schema", []),
        Tool("postgres", "describe_table", "Show the columns and types of a database table", ["table_name"]),
    ],
    "puppeteer": [
        Tool("puppeteer", "puppeteer_navigate", "Navigate a headless browser to a URL", ["url"]),
        Tool("puppeteer", "puppeteer_screenshot", "Take a screenshot of the current browser page", ["name", "selector"]),
        Tool("puppeteer", "puppeteer_click", "Click an element on the page by CSS selector", ["selector"]),
        Tool("puppeteer", "puppeteer_fill", "Type text into an input field on the page", ["selector", "value"]),
    ],
    "fetch": [
        Tool("fetch", "fetch", "Fetch a URL and return its content converted to markdown", ["url", "max_length"]),
    ],
    "memory": [
        Tool("memory", "create_entities", "Create entities in the knowledge graph memory", ["entities"]),
        Tool("memory", "search_nodes", "Search for nodes in the knowledge graph by query", ["query"]),
        Tool("memory", "read_graph", "Read the entire knowledge graph", []),
    ],
    "time": [
        Tool("time", "get_current_time", "Get the current time in a specific timezone", ["timezone"]),
        Tool("time", "convert_time", "Convert a time between two timezones", ["source_timezone", "time", "target_timezone"]),
    ],
    "sqlite": [
        Tool("sqlite", "read_query", "Execute a SELECT query on the SQLite database", ["query"]),
        Tool("sqlite", "write_query", "Execute an INSERT, UPDATE, or DELETE query", ["query"]),
        Tool("sqlite", "list_tables", "List all tables in the SQLite database", []),
    ],
}

# ---- Needs per tool: several paraphrases each (positives) ----------------------------------

NEEDS: dict[str, list[str]] = {
    "github::create_issue": [
        "file a bug report in our GitHub repo",
        "open a new issue on GitHub to track a task",
        "report a problem by creating a GitHub issue",
    ],
    "github::create_pull_request": [
        "open a pull request for my feature branch",
        "submit my changes for review as a PR",
    ],
    "github::search_code": [
        "find where a function is defined across our GitHub code",
        "search our source code on GitHub for a string",
    ],
    "github::get_file_contents": [
        "read a specific file from a GitHub repository",
        "fetch the contents of a file stored on GitHub",
    ],
    "github::list_commits": ["see the recent commits on a GitHub branch"],
    "github::merge_pull_request": ["merge an approved pull request on GitHub"],
    "filesystem::read_file": [
        "read a local text file from disk",
        "open a file on the local filesystem and get its contents",
    ],
    "filesystem::write_file": [
        "save some text to a file on disk",
        "create a new local file with content",
    ],
    "filesystem::list_directory": ["see what files are in a local folder"],
    "filesystem::move_file": ["rename a file on disk"],
    "filesystem::search_files": ["find local files matching a name pattern"],
    "filesystem::create_directory": ["make a new folder on disk"],
    "git::git_status": ["check which files changed in my local git checkout"],
    "git::git_diff": ["see the diff of my uncommitted changes"],
    "git::git_commit": ["commit my staged changes with a message"],
    "git::git_log": ["look at the commit history of this repo"],
    "git::git_create_branch": ["create a new git branch to work on"],
    "slack::post_message": [
        "send a message to a Slack channel",
        "post an announcement in Slack",
    ],
    "slack::list_channels": ["list the channels in our Slack workspace"],
    "slack::get_channel_history": ["read the recent messages from a Slack channel"],
    "slack::add_reaction": ["react to a Slack message with an emoji"],
    "brave_search::brave_web_search": [
        "search the web for current information",
        "look something up on the internet",
    ],
    "brave_search::brave_local_search": ["find restaurants near me"],
    "google_maps::maps_geocode": ["turn a street address into latitude and longitude"],
    "google_maps::maps_directions": ["get driving directions from one place to another"],
    "google_maps::maps_place_search": ["find coffee shops near a location"],
    "google_maps::maps_distance_matrix": ["compute travel times between several locations"],
    "postgres::query": ["run a SQL query against our Postgres database"],
    "postgres::list_tables": ["see what tables exist in the Postgres database"],
    "postgres::describe_table": ["show the columns of a database table"],
    "puppeteer::puppeteer_navigate": ["open a web page in a headless browser"],
    "puppeteer::puppeteer_screenshot": ["take a screenshot of a web page"],
    "puppeteer::puppeteer_click": ["click a button on a web page automatically"],
    "puppeteer::puppeteer_fill": ["fill in a form field on a web page"],
    "fetch::fetch": [
        "download a web page and convert it to markdown",
        "retrieve the text content of a URL",
    ],
    "memory::create_entities": ["store facts in the knowledge graph"],
    "memory::search_nodes": ["search my knowledge graph memory"],
    "memory::read_graph": ["dump the entire knowledge graph"],
    "time::get_current_time": ["what time is it in Tokyo right now"],
    "time::convert_time": ["convert 3pm New York time to London time"],
    "sqlite::read_query": ["select rows from the SQLite database"],
    "sqlite::write_query": ["insert a record into the SQLite database"],
    "sqlite::list_tables": ["list the tables in the SQLite file"],
}

# Hard negatives: needs describing capabilities absent from a given catalog.
HARD_NEGATIVES: dict[str, list[str]] = {
    # against a filesystem+git only catalog
    "local_dev": [
        "send an email to a customer",
        "charge a credit card",
        "translate this paragraph into French",
        "generate an image of a cat",
        "book a flight to Paris",
    ],
    # against a web/search catalog
    "web_stack": [
        "commit my code changes",
        "run a SQL query on the database",
        "post a message to Slack",
        "encrypt a file with a password",
    ],
}


def build() -> None:
    # Per-server catalogs.
    for server, tools in SERVERS.items():
        save_catalog(Catalog(server, tools), CATALOGS_DIR / f"seed_{server}.json")

    # A broad "everything" catalog (stress: many tools, cross-server duplicates).
    everything = [t for tools in SERVERS.values() for t in tools]
    save_catalog(Catalog("seed_everything", everything), CATALOGS_DIR / "seed_everything.json")

    # A near-duplicate catalog: two web-searchers + two file readers + two SQL tools.
    near_dupe = (
        SERVERS["brave_search"]
        + [Tool("fetch", "fetch", "Fetch a URL and return its content converted to markdown", ["url"])]
        + SERVERS["filesystem"][:2]
        + [Tool("github", "get_file_contents", "Read the contents of a file from a GitHub repository", ["owner", "repo", "path"])]
        + SERVERS["postgres"]
        + SERVERS["sqlite"]
    )
    save_catalog(Catalog("seed_near_dupe", near_dupe), CATALOGS_DIR / "seed_near_dupe.json")

    # A small local-dev catalog for hard negatives.
    local_dev = SERVERS["filesystem"] + SERVERS["git"]
    save_catalog(Catalog("local_dev", local_dev), CATALOGS_DIR / "seed_local_dev.json")
    web_stack = SERVERS["brave_search"] + SERVERS["google_maps"] + SERVERS["fetch"]
    save_catalog(Catalog("web_stack", web_stack), CATALOGS_DIR / "seed_web_stack.json")

    examples: list[EvalExample] = []

    # Positives against the everything catalog (hardest single-catalog retrieval).
    for gold, needs in NEEDS.items():
        for i, need in enumerate(needs):
            tags = ["positive", "everything"]
            if i > 0:
                tags.append("paraphrase")
            examples.append(EvalExample(need=need, catalog_id="seed_everything", gold=gold, tags=tags))

    # Near-duplicate disambiguation: needs that must pick the right one of two similar tools.
    near_dupe_cases = [
        ("search the public web for news", "brave_search::brave_web_search"),
        ("read a file from my local disk", "filesystem::read_file"),
        ("read a file stored in a GitHub repo", "github::get_file_contents"),
        ("query the postgres database with SQL", "postgres::query"),
        ("run a select against the sqlite database", "sqlite::read_query"),
        ("download the html of a web page as markdown", "fetch::fetch"),
    ]
    for need, gold in near_dupe_cases:
        examples.append(EvalExample(need=need, catalog_id="seed_near_dupe", gold=gold, tags=["near_duplicate", "positive"]))

    # Hard negatives.
    for need in HARD_NEGATIVES["local_dev"]:
        examples.append(EvalExample(need=need, catalog_id="local_dev", gold=None, tags=["hard_negative"]))
    for need in HARD_NEGATIVES["web_stack"]:
        examples.append(EvalExample(need=need, catalog_id="web_stack", gold=None, tags=["hard_negative"]))

    # Also test positives inside their own single-server catalog (easier retrieval baseline).
    for gold, needs in NEEDS.items():
        server = gold.split("::", 1)[0]
        examples.append(EvalExample(need=needs[0], catalog_id=server, gold=gold, tags=["positive", "single_server"]))

    save_eval(examples, EVAL_DIR / "seed.jsonl")
    print(f"catalogs: {len(list(CATALOGS_DIR.glob('seed_*.json')))} seed files")
    print(f"eval examples: {len(examples)}")
    pos = sum(1 for e in examples if e.gold)
    neg = sum(1 for e in examples if not e.gold)
    print(f"  positives: {pos}  hard_negatives: {neg}")


if __name__ == "__main__":
    build()
