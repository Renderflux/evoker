# evoker
A webserver for serving Renderflux's GPT-2 based generative art prompt autocomplete model

# Training
training is very simple. Just use the already provided prompt dataset located in `/evoker/data/prompts.txt`, or replace it with your own.

The format is just prompts, seperated by newlines, like so:
```
A summer field, art by tyler edlin, trending on artstation
a majestic dragon flying through the clouds by typer edlin, trending on artstation
a mountain with an orb of energy above it by typer edlin, trending on artstation
A dark and dreary place, where the only light is the moonlight, the only sound is the wind, and the only smell is the stench of decay
```

once you have your dataset, you can begin training. From the root directory of the project, install dependencies with poetry

```bash
poetry install
```

then enter the virtualenv

```bash
poetry shell
```

now start training!

```bash
python evoker train {epochs}
```

a good amount for `epochs` is 50-200. You can experiement with this though.

after training, you can test your model quickly like so:

```bash
python evoker predict {prompt}
```

for axample,

```bash
python evoker predict a beautiful

['a beautiful dreary place and charming mountain goat palace, great outdoors field, charming and often secluded']
```

# Serving
once you have a good model trained up, you can start the webserver with

```bash
python evoker serve
```

once the webserver starts, you can make a `POST` request to `/predict` with a json body that looks something like:

```json
{
    "prompt": "a beautiful",
    "amount": 1
}
```

thats pretty much it. If you have any issue don't hesistate to make a PR!
