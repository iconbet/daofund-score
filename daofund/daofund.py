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

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()
        self.admins.put(self.owner)

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

        if _admin in self.admins:
            remove_array_item(self.admins, _admin)
            self.AdminRemoved(_admin)

        else:
            revert(f'{TAG}: {_admin} not in Admins List')

    @external(readonly=True)
    def get_admins(self):
        return [_address for _address in self.admins]

    @external
    @payable
    def add_fund(self):
        """
        Add fund to the daoFund wallet
        :return:
        """
        pass

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
