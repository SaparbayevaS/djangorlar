#!/usr/bin/env python3
"""
Простой CLI task manager.
Команды: add, list, done, remove, save, load, exit
Файловое сохранение в tasks.json
"""
import json
import datetime
import os
from dataclasses import dataclass, asdict, field
from typing import List

SAVE_FILE = "tasks.json"

@dataclass
class Task:
    id: int
    title: str
    created: str
    done: bool = False
    tags: List[str] = field(default_factory=list)

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id = 1

    def add(self, title: str, tags=None):
        if tags is None:
            tags = []
        t = Task(id=self._next_id, title=title, created=str(datetime.datetime.now()), tags=tags)
        self.tasks.append(t)
        self._next_id += 1
        print(f"Added task #{t.id}: {t.title}")

    def list(self, show_all=True):
        if not self.tasks:
            print("Задач нет.")
            return
        for t in self.tasks:
            if show_all or not t.done:
                status = "✓" if t.done else " "
                tags = f"[{', '.join(t.tags)}]" if t.tags else ""
                print(f"#{t.id:02d} [{status}] {t.title} {tags} (created: {t.created})")

    def mark_done(self, task_id: int):
        t = self._find(task_id)
        if t:
            t.done = True
            print(f"Task #{task_id} помечена как выполненная.")
        else:
            print("Task not found.")

    def remove(self, task_id: int):
        t = self._find(task_id)
        if t:
            self.tasks.remove(t)
            print(f"Task #{task_id} удалена.")
        else:
            print("Task not found.")

    def save(self, filename=SAVE_FILE):
        data = {
            "next_id": self._next_id,
            "tasks": [asdict(t) for t in self.tasks]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.tasks)} tasks to {filename}.")

    def load(self, filename=SAVE_FILE):
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден.")
            return
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._next_id = data.get("next_id", 1)
        self.tasks = [Task(**t) for t in data.get("tasks", [])]
        print(f"Загружено {len(self.tasks)} задач из {filename}.")

    def _find(self, task_id: int):
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

def repl():
    tm = TaskManager()
    tm.load()
    print("Простой таск-менеджер. help для списка команд.")
    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            tm.save()
            break
        if not cmd:
            continue
        parts = cmd.split()
        if parts[0] in ("q", "exit"):
            tm.save()
            break
        if parts[0] == "help":
            print("Команды: add <title> [#tags], list, list all, done <id>, remove <id>, save, load, exit")
            continue
        if parts[0] == "add":
            # syntax: add buy milk #groceries,#home
            if len(parts) < 2:
                print("Использование: add <title> [#tag1,#tag2]")
                continue
            title = " ".join(p for p in parts[1:] if not p.startswith("#"))
            tag_part = next((p for p in parts[1:] if p.startswith("#")), "")
            tags = [t for t in tag_part.lstrip("#").split(",") if t] if tag_part else []
            tm.add(title=title, tags=tags)
            continue
        if parts[0] == "list":
            if len(parts) > 1 and parts[1] == "all":
                tm.list(show_all=True)
            else:
                tm.list(show_all=False)
            continue
        if parts[0] == "done":
            if len(parts) != 2 or not parts[1].isdigit():
                print("Использование: done <id>")
                continue
            tm.mark_done(int(parts[1]))
            continue
        if parts[0] == "remove":
            if len(parts) != 2 or not parts[1].isdigit():
                print("Использование: remove <id>")
                continue
            tm.remove(int(parts[1]))
            continue
      
        print("help")
        
if __name__ == "__main__":
    repl()