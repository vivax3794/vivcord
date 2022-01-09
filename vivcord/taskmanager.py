"""Manage running tasks and await them when they are done."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, cast

from loguru import logger

if TYPE_CHECKING:
    from typing import Any, Coroutine


class TaskManger:
    """
    Manage multiple running async tasks.

    This will in a loop check for tasks that are done, then await them.
    It is like a asyncio.gather, but you can add tasks while it is running.
    """

    def __init__(self):
        """Create TaskManger."""
        self._tasks: list[asyncio.Task[None]] = []

    def add_task(self, task: asyncio.Task[None] | Coroutine[Any, Any, None]) -> None:
        """
        Add a task to be managed.

        Args:
            task (asyncio.Task[None]): Task to manage.
        """
        # logger.debug(f"adding task {task}")
        # https://github.com/microsoft/pyright/issues/2721
        if asyncio.iscoroutine(task):
            task = asyncio.create_task(task)
        else:
            task = cast(asyncio.Task[None], task)

        self._tasks.append(task)

    async def start(self):
        """Start the task managing loop."""
        while True:
            # allow other tasks to run
            await asyncio.sleep(0, None)

            complete: list[asyncio.Task[None]] = [
                task for task in self._tasks if task.done()
            ]

            for task in complete:
                self._tasks.remove(task)
                # logger.debug(f"task done, awaiting {task}")
                await task

    async def close(self):
        """Close task manager and await/close all remaining tasks."""
        for task in self._tasks:
            if task.done():
                logger.debug(f"TaskManager closing, awaiting task {task}")
                await task
            else:
                logger.debug(f"TaskManager closing, canceling task {task}")
                _ = task.cancel()
