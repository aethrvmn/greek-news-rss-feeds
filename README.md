# Greek News RSS Feed Generator

In today's media landscape, navigating through the barrage of news articles, overwhelming advertising, and revenue-driven news aggregation apps has become an arduous task. The purity of information is at times compromised, making it harder for readers to keep up with genuine content. Worse yet, some media outlets have ceased supporting RSS, a tool that once revolutionized content consumption by delivering news straight to readers without the fluff. The decision to withhold RSS support, in my personal opinion, is a disservice to readers and a step backward in the grand journey of information democratization.

## Origin

The idea of this project was inspired by [this repository](https://github.com/capjamesg/openai-blog-rss). Credits to the original authors for laying the groundwork.

## Current Support

- [liberal.gr](https://liberal.gr)

## How It Works

This generator extracts articles from different categories of the selected news website. After curating the content and removing ads and non-essential components, it produces an RSS feed for each category.

### Hosting and Updates

The RSS feeds are hosted on my personal website, and I've set up a cronjob to refresh the XML files every hour. You can subscribe to them to get the latest content directly to your favorite RSS reader.

### Future Goals

The goal is to expand this tool to other Greek media outlets.

## Contributions

Feel free to contribute! If you're familiar with the structure of other media outlets, your expertise can help expand the reach of this tool.