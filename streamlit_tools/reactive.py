from typing import TypeVar, Generic
from dataclasses import dataclass
import streamlit as st
import inspect

T = TypeVar("T")


@dataclass
class Reactive(Generic[T]):
    key: str

    @property
    def value(self) -> T:
        return st.session_state[self.key]

    @value.setter
    def value(self, value: T):
        st.session_state[self.key] = value


def use_reactive(name: str, initial_value: T) -> Reactive[T]:
    caller_name = inspect.currentframe().f_back.f_code.co_qualname  # type: ignore
    key = f"__reactive#{caller_name}#{name}"
    if key not in st.session_state:
        st.session_state[key] = initial_value
    return Reactive(key)
