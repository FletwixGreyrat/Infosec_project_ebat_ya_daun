from aiogram.dispatcher.filters.state import State, StatesGroup


class OSINTFSM(StatesGroup):
    request = State()


class antivirusFSM(StatesGroup):
    request = State()


class coderFSM(StatesGroup):
    request = State()