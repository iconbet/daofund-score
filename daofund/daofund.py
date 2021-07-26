from iconservice import *

TAG = 'ICONbet DAOfund'


def remove_array_item(array_db, target) -> bool:
    _out = array_db[-1]
    if _out == target:
        array_db.pop()
        return True
    for index in range(len(array_db) - 1):
        if array_db[index] == target:
            array_db[index] = _out
            array_db.pop()
            return True
    return False


class DaoFund(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self.admins = ArrayDB('admins', db, value_type=Address)
        self.withdraw_count = VarDB('withdraw_count', db, value_type=int)
        self.withdraw_record = DictDB('withdraw_record', db, value_type=str, depth=2)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()
        self.admins.put(self.owner)
        self.withdraw_count.set(0)

    @external(readonly=True)
    def name(self) -> str:
        """
        :return: name of the Score
        """
        return TAG

    @external
    def add_admin(self, _admin: Address):
        if self.msg.sender != self.owner:
            revert(f'{TAG}: Only admins can set new admins.')

        if _admin == self.owner:
            revert(f'{TAG}: Owner address cannot be removed from the admins list.')

        if _admin not in self.admins:
            self.admins.put(_admin)
            self.AdminAdded(_admin)

    @external
    def remove_admin(self, _admin: Address):
        if self.msg.sender != self.owner:
            revert(f'{TAG}: Only admins can remove the admins.')

        if _admin == self.owner:
            revert(f'{TAG}: Owner address cannot be removed from the admins list.')

        if _admin in self.admins:
            remove_array_item(self.admins, _admin)
            self.AdminRemoved(_admin)

        else:
            revert(f'{TAG}: {_admin} not in Admins List')

    @external(readonly=True)
    def get_admins(self) -> list:
        return [_address for _address in self.admins]

    @external
    @payable
    def add_fund(self) -> None:
        """
        Add fund to the daoFund wallet
        :return:
        """
        pass

    @external
    def withdraw_fund(self, _address: Address, _amount: int, _memo: str) -> None:
        if self.msg.sender not in self.admins:
            revert(f'{TAG}: Only admins can run this method.')

        _available_amount = self.icx.get_balance(self.address)
        if _available_amount >= _amount:
            try:
                self.withdraw_count.set(self.withdraw_count.get() + 1)
                _withdraw_count: int = self.withdraw_count.get()
                self.withdraw_record[_withdraw_count]['withdraw_amount'] = str(_amount)
                self.withdraw_record[_withdraw_count]['withdraw_address'] = str(_address)
                self.withdraw_record[_withdraw_count]['withdraw_memo'] = _memo
                self.withdraw_record[_withdraw_count]['withdraw_timestamp'] = str(self.now() // 10 ** 6)
                self.icx.transfer(_address, _amount)
                self.FundTransferred(_address, f"{_amount} transferred to {_address} for {_memo}")
            except BaseException as e:
                revert(f"{TAG} : Network problem. Claiming Reward. Reason: {e}")

        else:
            revert(f"{TAG} :Not Enough balance. Available Balance = {_available_amount}.")

    @external(readonly=True)
    def get_withdraw_count(self) -> int:
        return self.withdraw_count.get()

    @external(readonly=True)
    def get_withdraw_records(self) -> list:
        wd_count: int = self.withdraw_count.get()
        return [{"withdraw_address": self.withdraw_record[_withdraw]['withdraw_address'],
                 "withdraw_timestamp": self.withdraw_record[_withdraw]['withdraw_timestamp'],
                 "withdraw_reason": self.withdraw_record[_withdraw]['withdraw_memo'],
                 "withdraw_amount": self.withdraw_record[_withdraw]['withdraw_amount']}
                for _withdraw in range(1, wd_count + 1)]

    @payable
    def fallback(self):
        pass

    @eventlog(indexed=1)
    def AdminAdded(self, _address: Address):
        pass

    @eventlog(indexed=1)
    def AdminRemoved(self, _address: Address):
        pass

    @eventlog(indexed=1)
    def FundTransferred(self, _address: Address, note: str):
        pass
