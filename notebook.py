import re
import datetime
from collections import UserDict


class _HashTag:
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return f"{self.tag}"


class _Note:
    def __init__(self, note_title: str, note_text: str, tags: list[_HashTag] = None):
        self.note_title = note_title
        self.note_text = note_text
        self.tags = tags

    # def set_new_tag(self, tag: _HashTag | list[_HashTag]):
    #     self.tags.extend(tag) if type(tag) == list else self.tags.append(tag)

    def __str__(self):
        tags_str = " ".join('#' + str(tag) for tag in self.tags)
        res = ["_" * 100
               + f"\n\033[1m{self.note_title.upper()}:\033[0m\n\n{self.note_text}"
               + f"\n\033[94m{tags_str}\033[0m\n"
               + "_" * 100
               + "\n"]
        return "\n".join(res)


class NoteBook(UserDict):

    def create_note(self):
        note_title = input("Enter note title: ")
        # Если заметка с таким же заголовком уже существует, то к названию плюсуеться текущее дата и время
        if note_title in self.data.keys():
            note_title += f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        note_content = input("Enter note text: ")
        tags_str = input("Enter tags (space separated): ").strip()
        tags_list = tags_str.split()
        tags = [_HashTag(tag.strip()) for tag in tags_list]
        new_note = _Note(note_title, note_content, tags)
        self.add_note(new_note)
        result = f"Note '{note_title}' created successfully!"
        return result

    def add_note(self, note: _Note):
        self.data[note.note_title] = note

    def ask_note(self):
        print("Choose the note you want to work with.")
        titles = []
        for i, title in enumerate(self.data.keys(), 1):
            titles.append(title)
            print(f"{i}. {title}")
        while True:
            try:
                pos_input = input("Enter positional number of the note or 'exit'\n>>> ")
                if pos_input.lower() == "exit":
                    return "exiting..."
                title_pos = int(pos_input) - 1
                if title_pos > len(self.data.keys()) or title_pos < 0:
                    raise IndexError
            except IndexError:
                print("Wrong position. Please try again.")
                continue
            except ValueError:
                print("Please enter a valid integer index.")
                continue
            return titles[title_pos]

    def change_note(self):
        note_title = self.ask_note()
        note = self.data[note_title].note_text
        ch_note = input(
            f"Your old note:\n\n{note}\n\nYou can do a few changes by copy/paste old note, or create new one.\n>>> "
        )
        self.data[note_title].note_text = ch_note
        return f'Note {note_title} was changed.'

    def del_note(self):
        note_title = self.ask_note()
        self.data.pop(note_title)
        return f"Note '{note_title}' was successfully deleted."

    def show_notes(self):
        for note in self.data.values():
            print(str(note))

    # Поиск
    def search_note(self, query):
        results = []
        for note in self.data.values():
            if re.search(query, note.note_title, re.IGNORECASE) or re.search(query, note.note_text, re.IGNORECASE):
                results.append(note)
        return results

    def find_tag(self, search_val):
        result = set()
        for note in self.data.values():
            tag_list = [str(tag) for tag in note.tags]
            for stag in search_val:
                if stag in tag_list:
                    result.add(note)
        return list(result)

    def change_title(self):
        old_title = self.ask_note()
        new_title = input("Provide new title for the note\n>>> ")
        if old_title in self.data:
            self.data[new_title] = self.data.pop(old_title)
            self.data[new_title].note_title = new_title
        return f'Old title name {old_title} was change on - {new_title}'

    def _get_tags(self):
        if self.data.values():
            note_title = self.ask_note()
            tags = self.data[note_title].tags
            mes = f'This note has next tags: {" ".join("#" + str(tag) for tag in tags)}' if tags \
                else "This note hasn't any tag yet."
            print(mes)
            new_tags_str = input("Enter new tag(s)\n>>> ")
            new_tags_list = new_tags_str.split()
            new_tags = [_HashTag(tag.strip()) for tag in new_tags_list]
            return [note_title, tags, new_tags]

    def set_tags(self):
        if self.data.values():
            got_tags = self._get_tags()
            tags, new_tags, title = got_tags[1], got_tags[2], got_tags[0]
            tags += new_tags
            self.data[title].tags = tags
            return "Tags added successfully."
        else:
            return "No notes to set tags for."

    def change_tags(self):
        if self.data.values():
            got_tags = self._get_tags()
            new_tags, title = got_tags[2], got_tags[0]
            self.data[title].tags = new_tags
            return "Tags set successfully."
        else:
            return "No notes to set tags for."

    def del_tags(self):
        if self.data.values():
            note_title = self.ask_note()
            self.data[note_title].tags = []
            return "Tags deleted successfully."
        else:
            return "No notes to set tags for."

    def __str__(self):
        return "\n".join(str(n) for n in self.data.values())


notebook = NoteBook()

if __name__ == "__main__":
    notebook.create_note()
    notebook.create_note()
    notebook.show_notes()
    # notebook.search_note()
