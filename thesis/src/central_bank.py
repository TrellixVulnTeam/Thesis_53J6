#!/usr/bin/env python
# [SublimeLinter pep8-max-line-length:150]
# -*- coding: utf-8 -*-

"""
black_rhino is a multi-agent simulator for financial network analysis
Copyright (C) 2016 Co-Pierre Georg (co-pierre.georg@keble.ox.ac.uk)
Pawel Fiedor (pawel@fiedor.eu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from abm_template.src.baseagent import BaseAgent

# ============================================================================
#
# class Bank
#
# ============================================================================


class CentralBank(BaseAgent):
    #
    #
    # VARIABLES
    #
    #

    identifier = ""  # identifier of the central bank
    parameters = {}  # parameters of the central bank
    state_variables = {}  # state variables of the central bank
    accounts = []  # all accounts of the central bank (filled with transactions)

    #
    #
    # CODE
    #
    #

    # -------------------------------------------------------------------------
    # functions for setting/changing id, parameters, and state variables
    # these either return or set specific value to the above variables
    # with the exception of append (2 last ones) which append the dictionaries
    # which contain parameters or state variables
    # -------------------------------------------------------------------------
    def get_identifier(self):
        return self.identifier

    def set_identifier(self, value):
        super(CentralBank, self).set_identifier(value)

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, value):
        super(CentralBank, self).set_parameters(value)

    def get_state_variables(self):
        return self.state_variables

    def set_state_variables(self, value):
        super(CentralBank, self).set_state_variables(value)

    def append_parameters(self, value):
        super(CentralBank, self).append_parameters(value)

    def append_state_variables(self, value):
        super(CentralBank, self).append_state_variables(value)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # functions needed to make CentralBank() hashable
    # -------------------------------------------------------------------------
    def __key__(self):
        return self.identifier

    def __eq__(self, other):
        return self.__key__() == other.__key__()

    def __hash__(self):
        return hash(self.__key__())
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # __init__
    # -------------------------------------------------------------------------
    def __init__(self):
        self.identifier = ""  # identifier of the central bank
        self.parameters = {}  # parameters of the central bank
        self.state_variables = {}  # state variables of the central bank
        self.accounts = []  # all accounts of the bank (filled with transactions)
        # DO NOT EVER ASSIGN PARAMETERS BY HAND AS DONE BELOW IN PRODUCTION CODE
        # ALWAYS READ THE PARAMETERS FROM CONFIG FILES
        # OR USE THE FUNCTIONS FOR SETTING / CHANGING VARIABLES
        # CONVERSELY, IF YOU WANT TO READ THE VALUE, DON'T USE THE FULL NAMES
        # INSTEAD USE __getattr__ POWER TO CHANGE THE COMMAND FROM
        # instance.static_parameters["xyz"] TO instance.xyz - THE LATTER IS PREFERRED
        self.parameters["interest_rate_cb_loans"] = 0.0  # interest rate on loans
    # -------------------------------------------------------------------------


    # -------------------------------------------------------------------------
    # central_bank_initialize_bank
    # household randomly choices proportion of endowment held in bank deposits
    # and proportion held in CBDC
    # -------------------------------------------------------------------------
    def central_bank_initialize_bank(self, environment, tranx):
        # Create reserves for bank
        environment.new_transaction(type_="reserves_required", asset='', from_= tranx["from_"], to = tranx["to"], amount = tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Create Open Market Transactions agreement with Bank
        environment.new_transaction(type_="omt_endow", asset='', from_= tranx["from_"], to = tranx["to"], amount = tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
    # -------------------------------------------------------------------------



    # -------------------------------------------------------------------------
    # make_cbdc_payment
    # takes in transaction details from household and makes payment
    # -------------------------------------------------------------------------
    def make_cbdc_payment(self, environment, tranx, time):
		# Transfer funds from household to central bank to household
        environment.new_transaction(type_="cbdc", asset='', from_=tranx["from_"], to="central_bank", amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Transfer funds from central bank to household
        environment.new_transaction(type_="cbdc", asset='', from_="central_bank", to=tranx["to"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
		# We print the action of selling to the screen
        print("{}s paid {}f of cbdc to {}s for {}s at time {}d.").format(tranx["from_"], tranx["amount"], "central_bank", tranx["to"], tranx["time"])
        print("{}s settled {}f of cbdc to {}s at time {}d.").format("central_bank", tranx["amount"], tranx["to"], tranx["to"], tranx["time"])
        #logging.info("  payments made on step: %s",  time)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # make_bank_notes_payment
    # takes in transaction details from household and makes payment
    # -------------------------------------------------------------------------
    def make_bank_notes_payment(self, environment, tranx, time):
		# Transfer funds from household to central bank to household
        environment.new_transaction(type_="bank_notes", asset='', from_=tranx["from_"], to="central_bank", amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Transfer funds from central bank to household
        environment.new_transaction(type_="bank_notes", asset='', from_="central_bank", to=tranx["to"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
		# We print the action of selling to the screen
        print("{}s paid {}f of cbdc to {}s for {}s at time {}d.").format(tranx["from_"], tranx["amount"], "central_bank", tranx["to"], tranx["time"])
        print("{}s settled {}f of cbdc to {}s at time {}d.").format("central_bank", tranx["amount"], tranx["to"], tranx["to"], tranx["time"])
        #logging.info("  payments made on step: %s",  time)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # rgts_payment
    # takes in transaction details from household and makes payment
    # -------------------------------------------------------------------------
    def rgts_payment(self, environment, tranx, time):
		# Transfer funds from central bank to bank
        environment.new_transaction(type_="reserves", asset='', from_=self.identifier, to=tranx["bank_to"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        environment.get_agent_by_id(tranx["bank_to"]).settle_payment(environment, tranx, time)
        print("{} RTGSed {} of reserves to {} at time {}d.").format(self.identifier, tranx["amount"], tranx["bank_to"],tranx["time"])
        #logging.info("  payments made on step: %s",  time)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # balance
    # net payments and receipts plus initial deposits
    # returns balance
    # -------------------------------------------------------------------------
    def balance(self, type_):
        # Determine Endowments
        reserves = self.get_account("reserves_required")
        omt = self.get_account("omt_endow")
        cbdc = self.get_account("cbdc_endow")
        bank_notes = self.get_account("bank_notes_endow")
        # Track Changes for different asset classes
        for tranx in self.accounts:
            if tranx.from_.identifier == self.identifier:
                if tranx.type_ == "reserves":
                   reserves += tranx.amount
                elif tranx.type_ == "omt":
                   omt += tranx.amount
                elif tranx.type_ == "cbdc":
                   cbdc += tranx.amount
                elif tranx.type_ == "bank_notes":
                   bank_notes += tranx.amount
            elif tranx.from_.identifier != self.identifier:
                if tranx.type_ == "reserves":
                   reserves -= tranx.amount
                elif tranx.type_ == "omt":
                   omt -= tranx.amount
                elif tranx.type_ == "cbdc":
                   cbdc -= tranx.amount
                elif tranx.type_ == "bank_notes":
                   bank_notes -= tranx.amount
        # Return Requested Balance
        if type_ == "reserves":
            return reserves
        elif type_ == "omt":
            return omt
        elif type_ == "cbdc":
            return cbdc
        elif type_ == "bank_notes":
            return bank_notes
        elif type_ == "assets":
            return (omt)
        elif type_ == "liabilities":
            return (reserves + cbdc + bank_notes)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # cbdc_settle
    # Household exchanges deposits at bank for cbdc at central bank
    # -------------------------------------------------------------------------
    def cbdc_settle(self, environment, tranx, time):
        # Transfer Banks Reserves for CBDC
        # Decrease Reserves for Bank and Central Bank
        environment.new_transaction(type_="reserves", asset='', from_= tranx["bank_from"], to = "central_bank", amount = tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Transfer CBDC to Household
        environment.new_transaction(type_="cbdc", asset='', from_="central_bank", to=tranx["from_"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Transfer Open Market Transactions to Bank
        environment.new_transaction(type_="omt", asset='', from_="central_bank", to=tranx["bank_from"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Increase Bank Reserves equal to increase Open Market Transactions agreement
        environment.new_transaction(type_="reserves", asset='', from_= "central_bank", to= tranx["bank_from"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        print("CBDC settlement of {} to {} complete").format(tranx["from_"], tranx["amount"])
    # -------------------------------------------------------------------------


    # -------------------------------------------------------------------------
    # bank_notes_settle
    # Household exchanges deposits at bank for Bank Notes at Central Bank
    # -------------------------------------------------------------------------
    def bank_notes_settle(self, environment, tranx, time):
        # Decrease Reserves for Bank and Central Bank
        environment.new_transaction(type_="reserves", asset='', from_= tranx["bank_from"], to = "central_bank", amount = tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Transfer Bank Notes to Household
        environment.new_transaction(type_="bank_notes", asset='', from_="central_bank", to=tranx["from_"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Transfer Open Market Transactions to Bank
        environment.new_transaction(type_="omt", asset='', from_="central_bank", to=tranx["bank_from"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        # Increase Bank Reserves equal to increase Open Market Transactions agreement
        environment.new_transaction(type_="reserves", asset='', from_= "central_bank", to= tranx["bank_from"], amount=tranx["amount"], interest=0.00, maturity=0, time_of_default=-1)
        print("Bank Notes settlement of {} to {} complete").format(tranx["from_"], tranx["amount"])
    # -------------------------------------------------------------------------


    # -------------------------------------------------------------------------
    # __del__
    # -------------------------------------------------------------------------
    def __del__(self):
        pass
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # __str__
    # returns a string describing the central bank and its properties
    # based on the implementation in the abstract class BaseAgent
    # but adds the type of agent (bank) and lists all transactions
    # -------------------------------------------------------------------------
    def __str__(self):
        bank_string = super(CentralBank, self).__str__()
        bank_string = bank_string.replace("\n", "\n    <type value='central_bank'>\n", 1)
        text = "\n"
        text = text + "  </agent>"
        return bank_string.replace("\n  </agent>", text, 1)
    # ------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # get_parameters_from_file
    # reads the specified config file given the environment
    # and sets parameters to the ones found in the config file
    # the config file should be an xml file that looks like the below:
    # <central_bank identifier='string'>
    #     <parameter name='string' value='string'></parameter>
    # </central_bank>
    # -------------------------------------------------------------------------
    def get_parameters_from_file(self,  bank_filename, environment):
        super(CentralBank, self).get_parameters_from_file(bank_filename, environment)
    # ------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # check_consistency
    # Central bank is not balance sheet consistent in the model
    # -------------------------------------------------------------------------
    def check_consistency(self):
        assets = round(self.balance("assets"), 0)
        liabilities = round(self.balance("liabilities"), 0)
        return (assets == liabilities)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # get_account
    # returns the value of all transactions of a given type
    # -------------------------------------------------------------------------
    def get_account(self,  type_):
        return super(CentralBank, self).get_account(type_)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # get_account_num_transactions
    # returns the number of transactions of a given type
    # -------------------------------------------------------------------------
    def get_account_num_transactions(self,  type_):
        return super(CentralBank, self).get_account_num_transactions(type_)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # add_transaction
    # adds a transaction to the accounts
    # the transaction is endowed with the following information:
    #   type_           - type of transactions, e.g. "deposit"
    #   assets          - type of asset, used for investment types
    #   from_id         - agent being the originator of the transaction
    #   to_id           - agent being the recipient of the transaction
    #   amount          - amount of the transaction
    #   interest        - interest rate paid to the originator each time step
    #   maturity        - time (in steps) to maturity
    #   time_of_default - control variable checking for defaulted transactions
    # -------------------------------------------------------------------------
    def add_transaction(self, type_, asset,  from_id,  to_id,  amount,  interest,  maturity, time_of_default, environment):
        from src.transaction import Transaction
        transaction = Transaction()
        transaction.add_transaction(type_, asset, from_id,  to_id,  amount,  interest,  maturity,  time_of_default, environment)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # clear_accounts
    # removes all transactions from central bank's accounts
    # only for testing, the one in transaction should be used in production
    # -------------------------------------------------------------------------
    def clear_accounts(self, environment):
        super(CentralBank, self).clear_accounts(environment)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # purge_accounts
    # removes worthless transactions from central bank's accounts
    # -------------------------------------------------------------------------
    def purge_accounts(self, environment):
        super(CentralBank, self).purge_accounts(environment)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # get_transactions_from_file
    # reads transactions from the config file to the central bank's accounts
    # -------------------------------------------------------------------------
    def get_transactions_from_file(self, filename, environment):
        super(CentralBank, self).get_transactions_from_file(filename, environment)
    # -------------------------------------------------------------------------

    # __getattr__
    # if the attribute isn't found by Python we tell Python
    # to look for it first in parameters and then in state variables
    # which allows for directly fetching parameters from the Bank
    # i.e. bank.active instead of a bit more bulky
    # bank.parameters["active"]
    # makes sure we don't have it in both containers, which
    # would be bad practice [provides additional checks]
    # -------------------------------------------------------------------------
    def __getattr__(self, attr):
        return super(CentralBank, self).__getattr__(attr)
    # -------------------------------------------------------------------------
