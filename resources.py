import json
import os
from typing import List

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        return {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }

    @classmethod
    def from_json(cls, value: dict):
        new_enty = cls(value['title'])
        for item in value.get('entries', []):
            new_enty.add_entry(cls.from_json(item))
        return new_enty

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w', encoding='utf-8') as f:
            print(self.json())
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return cls.from_json(content)


class EntryManager():
    def __init__(self, data_path: str):
        self.data_path: str = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for file in os.listdir(self.data_path):
            if file.endswith('.json'):
                self.entries.append(Entry.load(os.path.join(self.data_path, file)))

    def add_entry(self, title: str):
        self.entries.append(Entry(title))


def print_with_indent(value, indent=0):
    indentation = "\t" * indent
    print(indentation + str(value))


grocery_list = {
    "title": "Продукты",
    "entries": [
        {
            "title": "Молочные",
            "entries": [
                {
                    "title": "Йогурт",
                    "entries": []
                },
                {
                    "title": "Сыр",
                    "entries": []
                }
            ]
        }
    ]
}
entry = Entry.from_json(grocery_list)
# entry.save('/tmp/')





