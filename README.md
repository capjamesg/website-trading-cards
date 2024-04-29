# Website Trading Cards

Generate a "trading card" representation of a website.

This tool could be used to create a physical version of your blogroll.

Example:

<img width="432" alt="Screenshot 2024-04-29 at 10 46 28" src="https://github.com/capjamesg/website-trading-cards/assets/37276661/6fb66dfe-973c-4a14-bb57-a67a5a37fe86">

## Use this Tool

First, install the project from source:

```
git clone https://github.com/capjamesg/website-trading-cards
cd website-trading-cards
pip3 install -r requirements.txt
```

To generate a trading card, run:

```
python3 app.py --website=https://example.com
```

If a website has a semantically marked up description, the description will appear on the card.

If a website does not have an available description, the description space on the card will be used as space to render a larger screenshot of the website, like this:

![en-wikipedia-org_1](https://github.com/capjamesg/website-trading-cards/assets/37276661/07e039db-89ce-441c-8be9-59ee34add1aa)

## License

This project is licensed under an [MIT license](LICENSE).
