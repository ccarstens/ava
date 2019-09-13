from spade.template import Template
from spade_bdi.bdi import BDIAgent

from log import log
import asyncio

from spade_bdi.bdi import parse_literal

from spade.message import Message

import aioconsole as ac



class Ava(BDIAgent):
    class AvasPersonality(BDIAgent.BDIBehaviour):
        def add_custom_actions(self):
            @self.agent.bdi_actions.add_function(".b_function", (int,))
            def _b_function(x):
                return x ** 2

            @self.agent.bdi_actions.add_function(".my_test", (int,))
            def _my_test(x):
                return "Hello this is the number: {}".format(x)

            @self.agent.bdi_actions.add_function(".your_test", (int,))
            def _your_test(x):
                print("this is my test")
                return x

            @self.agent.bdi_actions.add_function(".ask_user", (str,))
            def _ask_user(question):
                return input(question)

            @self.agent.bdi_actions.add_function(".log", (str,))
            def _log(message):
                log.debug("AVA: " + message)

            @self.agent.bdi_actions.add_function(".ask_user_options", (str, tuple))
            def _ask_user_options(question, options):
                readable = list(map(lambda l: str(l), options))
                response = input(question + "\n" + str(readable) + "\n: ")
                if response in readable:
                    return options[readable.index(response)]

            @self.agent.bdi_actions.add_function(".ask_user_a", (str,))
            def _ask_user_a(question):
                return "hello"

        async def run(self):
            await super().run()

            await asyncio.sleep(0.005)

        async def handle_message_with_custom_ilf_type(self, message: Message):

            functor, args = parse_literal(message.body)
            args = args[0]

            # handle communication with user here
            print("run: ", args[0])
            print("run: ", args[1])

            response = await ac.ainput("XX")
            self.add_achievement_goal("tell_va", response, source=message.sender)

    async def setup(self):
        log.debug("Ava agent setup")
        template = Template(metadata={"performative": "BDI"})
        personality = self.AvasPersonality()
        personality.custom_ilf_types = ['getuserinput']
        self.add_behaviour(personality, template)
        personality.setup()

