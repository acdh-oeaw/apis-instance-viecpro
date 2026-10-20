labels_schema = {
    "title": "Labels",
    "type": "array",
    "format": "table",
    "items": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "pattern": "^.+$",
                "options": {
                    "inputAttributes": {
                        "required": True,
                    },
                },
            },
            "label": {
                "type": "string",
                "pattern": "^.+$",
                "options": {
                    "inputAttributes": {
                        "required": True,
                    },
                },
            },
            "begin": {
                "type": "string",
                "options": {
                    "inputAttributes": {
                        "placeholder": "begin",
                    },
                },
            },
            "end": {
                "type": "string",
                "options": {
                    "inputAttributes": {
                        "placeholder": "end",
                    },
                },
            },
        },
    },
}
