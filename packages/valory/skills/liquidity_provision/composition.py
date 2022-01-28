# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2022 Valory AG
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

"""This module contains the liquidity provision ABCI application."""

from packages.valory.skills.abstract_round_abci.abci_app_chain import (
    AbciAppTransitionMapping,
    chain,
)
from packages.valory.skills.liquidity_provision.rounds import (
    FinishedEnterPoolTransactionHashRound,
    FinishedExitPoolTransactionHashRound,
    FinishedSwapBackTransactionHashRound,
    LiquidityStrategyAbciApp,
    StrategyEvaluationRound,
)
from packages.valory.skills.registration_abci.rounds import (
    AgentRegistrationAbciApp,
    FinishedRegistrationFFWRound,
    FinishedRegistrationRound,
    RegistrationRound,
)
from packages.valory.skills.safe_deployment_abci.rounds import (
    FinishedSafeRound,
    RandomnessSafeRound,
    SafeDeploymentAbciApp,
)
from packages.valory.skills.transaction_settlement_abci.rounds import (
    FailedRound,
    FinishedTransactionSubmissionRound,
    RandomnessTransactionSubmissionRound,
    TransactionSubmissionAbciApp,
)


abci_app_transition_mapping: AbciAppTransitionMapping = {
    FinishedRegistrationRound: RandomnessSafeRound,
    FinishedSafeRound: StrategyEvaluationRound,
    FinishedRegistrationFFWRound: StrategyEvaluationRound,
    FinishedEnterPoolTransactionHashRound: RandomnessTransactionSubmissionRound,
    FinishedExitPoolTransactionHashRound: RandomnessTransactionSubmissionRound,
    FinishedSwapBackTransactionHashRound: RandomnessTransactionSubmissionRound,
    FinishedTransactionSubmissionRound: StrategyEvaluationRound,
    FailedRound: RegistrationRound,
}

LiquidityProvisionAbciApp = chain(
    (
        AgentRegistrationAbciApp,
        SafeDeploymentAbciApp,
        LiquidityStrategyAbciApp,
        TransactionSubmissionAbciApp,
    ),
    abci_app_transition_mapping,
)
