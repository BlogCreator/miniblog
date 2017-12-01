#! /usr/bin/python3
import markdown
import sys
import os
import pymdownx
from pymdownx import emoji
extensions = [
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.emoji',
    'pymdownx.tasklist',
    'pymdownx.superfences'
]

extension_config = {
    "pymdownx.magiclink": {
        "repo_url_shortener": True,
        "repo_url_shorthand": True,
        "provider": "github",
        "user": "facelessuser",
        "repo": "pymdown-extensions"
    },
    "pymdownx.tilde": {
        "subscript": False
    },
    "pymdownx.emoji": {
        "emoji_index": pymdownx.emoji.gemoji,
        "emoji_generator": pymdownx.emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {
                "align": "absmiddle",
                "height": "20px",
                "width": "20px"
            },
            "image_path": "https://assets-cdn.github.com/images/icons/emoji/unicode/",
            "non_standard_image_path": "https://assets-cdn.github.com/images/icons/emoji/"
        }
    },
    "pymdownx.superfences": {
        "highlight_code": True,
        "custom_fences": "```"
    }
}
md = markdown.Markdown(
    extensions=extensions,
    extension_config=extension_config,
)
if __name__=='__main__':
    if len(sys.argv) != 3:
        print('usage:\n\tconvert input output')
        sys.exit()
    else:
        inputf = sys.argv[1]
        outputf = sys.argv[2]

        with open(inputf,'r',encoding='utf-8') as mdf:
            html = md.convert(mdf.read())
            with open(outputf,"w") as htmlf:
                htmlf.write("""
                <head>
                    <meta charset="utf-8">

                </head>
                <link rel="stylesheet" href="style.css"></link>
                """)
                htmlf.write(html)
