# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
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

"""Tests for abstract_round_abci/test_tools/integration.py"""

from pathlib import Path
from typing import Type, cast

import pytest
from aea.test_tools.utils import copy_class

from packages.open_aea.protocols.signing import SigningMessage
from packages.open_aea.protocols.signing.custom_types import SignedMessage
from packages.valory.connections.ledger.tests.conftest import make_ledger_api_connection
from packages.valory.skills.abstract_round_abci.base import AbciAppDB, _MetaPayload
from packages.valory.skills.abstract_round_abci.test_tools.integration import (
    IntegrationBaseCase,
)
from packages.valory.skills.abstract_round_abci.tests.data.dummy_abci import (
    PATH_TO_SKILL,
)
from packages.valory.skills.abstract_round_abci.tests.data.dummy_abci.behaviours import (
    DummyRoundBehaviour,
    DummyStartingBehaviour,
)
from packages.valory.skills.abstract_round_abci.tests.data.dummy_abci.rounds import (
    SynchronizedData,
)


class TestIntegrationBaseCase:
    """TestIntegrationBaseCase"""

    test_cls: Type[IntegrationBaseCase]

    @classmethod
    def setup_class(cls) -> None:
        """Setup class"""
        cls.old_value = _MetaPayload.transaction_type_to_payload_cls.copy()  # type: ignore
        _MetaPayload.transaction_type_to_payload_cls.clear()

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown class"""
        _MetaPayload.transaction_type_to_payload_cls = cls.old_value  # type: ignore

    def setup(self) -> None:
        """Setup test"""

        # must `copy` the class to avoid test interference
        test_cls = copy_class(IntegrationBaseCase)
        self.test_cls = cast(Type[IntegrationBaseCase], test_cls)

    def teardown(self) -> None:
        """Teardown test"""
        self.test_cls.teardown_class()  # otherwise keeps hanging

    def setup_test_cls(self) -> IntegrationBaseCase:
        """Helper method to setup test to be tested"""

        self.test_cls.setup_class()

        test_instance = self.test_cls()  # type: ignore
        test_instance.setup()
        return test_instance

    def set_path_to_skill(self, path_to_skill: Path = PATH_TO_SKILL) -> None:
        """Set path_to_skill"""
        self.test_cls.path_to_skill = path_to_skill

    def test_instantiation(self) -> None:
        """Test instantiation"""

        self.set_path_to_skill()
        self.test_cls.make_ledger_api_connection_callable = make_ledger_api_connection
        self.test_cls.behaviour = DummyRoundBehaviour
        test_instance = cast(IntegrationBaseCase, self.setup_test_cls())

        assert test_instance
        assert test_instance.get_message_from_outbox() is None
        assert test_instance.get_message_from_decision_maker_inbox() is None
        assert test_instance.process_n_messages(ncycles=0) is tuple()

        expected = "Invalid number of messages in outbox. Expected 1. Found 0."
        with pytest.raises(AssertionError, match=expected):
            assert test_instance.process_message_cycle()
        with pytest.raises(AssertionError, match=expected):
            assert test_instance.process_n_messages(ncycles=1)

    def test_process_n_messages(self) -> None:
        """Test process_n_messages"""

        self.set_path_to_skill()
        self.test_cls.make_ledger_api_connection_callable = make_ledger_api_connection
        self.test_cls.behaviour = DummyRoundBehaviour
        test_instance = cast(IntegrationBaseCase, self.setup_test_cls())

        behaviour_id = DummyStartingBehaviour.behaviour_id
        synchronized_data = SynchronizedData(
            AbciAppDB(setup_data=dict(participants=[frozenset("abcd")]))
        )

        # must have a handler!
        handlers = [test_instance.signing_handler]
        expected_content = [
            {"performative": SigningMessage.Performative.SIGNED_MESSAGE}
        ]
        expected_types = [{"signed_message": SignedMessage}]

        messages = test_instance.process_n_messages(
            ncycles=1,
            behaviour_id=behaviour_id,
            synchronized_data=synchronized_data,
            handlers=handlers,
            expected_content=expected_content,
            expected_types=expected_types,
            fail_send_a2a=True,
        )
        assert len(messages) == 1
