#  Drakkar-Software OctoBot
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import asyncio
import threading
import concurrent.futures as thread 

import octobot_commons.asyncio_tools as asyncio_tools
import octobot_commons.logging as logging

import octobot.constants as constants


class TaskManager:
    """TaskManager class:
        - Create, manage and stop octobot tasks
    """

    def __init__(self, octobot):
        self.octobot = octobot

        # Logger
        self.logger = logging.get_logger(self.get_name())

        self.async_loop = None
        self.ready = False
        self.watcher = None
        self.tools_task_group = None
        self.current_loop_thread = None
        self.executors = None
        self.bot_main_task = None
        self.loop_forever_thread = None

    def init_async_loop(self):
        self.async_loop = asyncio.new_event_loop()
        self.async_loop.set_exception_handler(self._loop_exception_handler)

    async def start_tools_tasks(self):
        task_list = []

        if self.octobot.community_handler:
            task_list.append(self.octobot.community_handler.start_community_task())

        self.octobot.async_loop = self.async_loop
        self.ready = True
        self.tools_task_group = asyncio.gather(*task_list)
        self.create_pool_executor()

    def run_bot_in_thread(self, coroutine):
        self.init_async_loop()
        self.bot_main_task = self.async_loop.create_task(coroutine)
        self.async_loop.run_forever()

    def run_forever(self, coroutine):
        self.loop_forever_thread = threading.Thread(target=self.run_bot_in_thread, args=(coroutine,),
                                                    name=f"OctoBot Main Thread")
        self.loop_forever_thread.start()

    def stop_tasks(self):
        self.logger.info("Stopping tasks...")
        stop_coroutines = [self.octobot.stop()]

        if self.tools_task_group:
            self.tools_task_group.cancel()

        # close community session
        if self.octobot.community_handler:
            stop_coroutines.append(self.octobot.community_handler.stop_task())

        self.async_loop.call_soon_threadsafe(asyncio.gather(*stop_coroutines, loop=self.async_loop))

        self.async_loop.stop()

        self.logger.info("Tasks stopped.")

    @classmethod
    def get_name(cls):
        return cls.__name__

    def create_pool_executor(self, workers=2):
        self.executors = thread.ThreadPoolExecutor(max_workers=workers)

    def _loop_exception_handler(self, loop, context):
        loop_str = "bot main async" if loop is self.async_loop else {loop}
        message = f"Error in {loop_str} loop: {context}"
        self.logger.warning(message)

    def _create_new_asyncio_main_loop(self):
        self.async_loop = asyncio.new_event_loop()
        self.async_loop.set_debug(constants.FORCE_ASYNCIO_DEBUG_OPTION)
        self.async_loop.set_exception_handler(self._loop_exception_handler)
        asyncio.set_event_loop(self.async_loop)
        self.current_loop_thread = threading.Thread(target=self.async_loop.run_forever,
                                                    name=f"{self.get_name()} new asyncio main loop")
        self.current_loop_thread.start()

    def run_in_main_asyncio_loop(self, coroutine):
        return asyncio_tools.run_coroutine_in_asyncio_loop(coroutine, self.async_loop)

    def run_in_async_executor(self, coroutine):
        if self.executors is not None:
            return self.executors.submit(asyncio.run, coroutine).result()
        return asyncio.run(coroutine)
