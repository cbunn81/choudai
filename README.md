# choudai

![choudai](choudai.gif)

choudai is a command-line application for fetching web pages. It will fetch the source HTML as well as asset files (images, CSS, JS, etc.) It will also keep track of each fetch so that you can update a previous fetch and also fine out when the last time a fetch was completed. It will also give you some additional metadata such as the number of images and links found on the fetched web page.

## How to use choudai

Note: choudai is distributed using Docker for cross-platform accessibility, so you will need to have Docker installed and running on your system to use it.

1. Clone the repo:

```
git clone https://github.com/cbunn81/choudai.git
```

2. Build the Docker image

```
docker build -t choudai .
```

3. Make a directory for the Docker volume to use

```
mkdir data
```

4. Run choudai via Docker to fetch some web pages

```
docker run --rm -v $(pwd)/data:/data choudai https://www.wikipedia.org
```

Note that you may specify more than one URL at a time:

```
docker run --rm -v $(pwd)/data:/data choudai https://www.wikipedia.org https://www.google.com
```

5. Run choudai in Docker to get metadata on previously fetched web pages

```
docker run --rm -v $(pwd)/data:/data choudai --metadata https://www.wikipedia.org
```

Note that you may specify more than one URL at a time:

```
docker run --rm -v $(pwd)/data:/data choudai --metadata  https://www.wikipedia.org https://www.google.com
```

Results:

```
url: https://www.wikipedia.org
num_images: 1
num_links: 327
last_fetch: 2022-10-31 13:34:05.128109
url: https://www.google.com
num_images: 1
num_links: 18
last_fetch: 2022-10-31 13:34:05.374511
```

You can also ask for help:

```
docker run --rm -v $(pwd)/data:/data choudai --help
```
