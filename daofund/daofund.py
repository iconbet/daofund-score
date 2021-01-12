from iconservice import *

TAG = 'ICONbet DAOfund'


class DaoFund(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def name(self) -> str:
        """
        :return: name of the Score
        """
        return TAG

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
