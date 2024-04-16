# Manganato API Wrapper

## Description

This project is an API wrapper for Manganato.com, designed to interact programmatically with the site's content. The API enables functionalities such as listing the latest manga updates, viewing manga details, reading chapters, and performing searches.

## Disclaimer

This API has been developed solely for educational purposes. It is intended to demonstrate API development using [RestCraft](https://github.com/lsfratel/restcraft) and is not endorsed or affiliated with Manganato.com. Users are responsible for ensuring that their use of this API complies with Manganato.com's terms of service and applicable laws.

## Features

- **List Latest Updates**: Fetch the latest manga updates with options for pagination.
- **View Manga**: Access detailed information about manga titles including genres, ratings, and summaries.
- **Read Chapters**: Read manga chapters directly through the API.
- **Search Manga**: Search for manga by keywords such as title or genre.

## Usage

Here are basic examples of how to interact with the API:

```bash
# List the latest manga updates
GET /v1/mangas
```

```bash
# Search for manga by title
GET /v1/mangas?q=naruto
```

```bash
# Get details for a specific manga
GET /v1/mangas/{manga_id}
```

```bash
# List all images for a chapter
GET /v1/chapters/{chapter_id}
```

```bash
# Preview an image of a chapter
GET /v1/images/{image_id}
```
