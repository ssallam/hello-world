# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""Dialogues classes for the ABCI connection."""

from aea.protocols.base import Address, Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue

from packages.valory.connections.abci import PUBLIC_ID
from packages.valory.protocols.abci.dialogues import AbciDialogue as BaseAbciDialogue
from packages.valory.protocols.abci.dialogues import AbciDialogues as BaseAbciDialogues


AbciDialogue = BaseAbciDialogue


class AbciDialogues(BaseAbciDialogues):
    """The dialogues class keeps track of all ABCI dialogues."""

    def __init__(self) -> None:
        """Initialize dialogues."""

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return AbciDialogue.Role.CLIENT

        BaseAbciDialogues.__init__(
            self,
            self_address=str(PUBLIC_ID),
            role_from_first_message=role_from_first_message,
            dialogue_class=AbciDialogue,
        )
