from io import BytesIO
from urllib.parse import quote_plus, urlparse

import cv2
import mf2py
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image
from sklearn.cluster import KMeans
import html2image
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--website", type=str, help="Website URL")

args = parser.parse_args()

WEBSITE = args.website

if not WEBSITE:
    exit("Please provide a website URL")

try:
    markup = mf2py.parse(url=WEBSITE, metaformats=True)
except Exception:
    exit("Invalid URL")

with open("figma-to-html/index.html") as html_file:
    soup = BeautifulSoup(html_file, "lxml")

data = markup["items"]

metaformats = [item for item in data if item.get("source", "") == "metaformats"]

if metaformats:
    metaformats = metaformats[0]["properties"]
    description = metaformats.get("summary", [""])[0]
else:
    metaformats = [item for item in data if "h-card" in item["type"]][0]["properties"]
    description = metaformats.get("note", [""])[0]

website_name = (
    metaformats.get("name", [""])[0]
    .split("|")[-1]
    .strip()
    .split("-")[0]
    .strip()
    .split(":")[0]
    .strip()
)
description = description.split(". ")
description = (
    ". ".join(description[:3]) if len(description) > 3 else ". ".join(description)
).strip(".")

if len(description) > 0:
    description += "."

domain = urlparse(WEBSITE).netloc

escaped_domain = quote_plus(WEBSITE)
photo_url = f"https://v1.screenshot.11ty.dev/{escaped_domain}/large/1:1/bigger/"

response = requests.get(photo_url)

img = Image.open(BytesIO(response.content))

img = np.array(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pixels = img.reshape(-1, 3)
model = KMeans(n_clusters=3, n_init=10)
model.fit(pixels)
palette = model.cluster_centers_
main_colors = palette[np.argsort(np.linalg.norm(palette, axis=1))][::-1]

soup.find("div", class_="v1_2").attrs["style"] = (
    f"background: linear-gradient(rgba({int(main_colors[0][0])}, {int(main_colors[0][1])}, {int(main_colors[0][2])}, 0.8), rgba({int(main_colors[1][0])}, {int(main_colors[1][1])}, {int(main_colors[1][2])}, 0.8));"
)

soup.find("span", class_="v1_11").string = description
soup.find("span", class_="name").string = website_name
soup.find("span", class_="v1_8").string = domain
soup.find("img", class_="v1_7").attrs["src"] = photo_url

if description.strip().strip(".") == "":
    soup.find("img", class_="v1_7").attrs["style"] = "height: 275px;"
    soup.find("div", class_="v1_5").attrs["style"] = "display: none;"
    soup.find("span", class_="v1_9").attrs["style"] = "display: none;"
    soup.find("span", class_="v1_8").attrs["style"] = "display: none;"

if markup["rels"].get("alternate") is None:
    soup.find("img", class_="rss").attrs["style"] = "display: none;"
else:
    soup.find("img", class_="rss").attrs["style"] = (
        "display: inline; float: right; margin-top: 2.5px;"
    )

h2i = html2image.Html2Image(output_path=".", size=(242, 336))

h2i.screenshot(html_str=soup, save_as=domain.replace(".", "-") + ".png")
