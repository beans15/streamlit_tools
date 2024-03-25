from typing import TypeVar, Generic, Hashable, overload
from dataclasses import dataclass
import streamlit as st
import inspect

T = TypeVar("T")
K = TypeVar("K", bound=(str | int), covariant=True)


@dataclass
class Reactive(Generic[T]):
    key: str

    @property
    def value(self) -> T:
        return st.session_state[self.key]

    @value.setter
    def value(self, value: T):
        st.session_state[self.key] = value


def use_reactive(
    name: str, initial_value: T, dependency: Hashable | None = None
) -> Reactive[T]:
    caller_name = inspect.currentframe().f_back.f_code.co_qualname  # type: ignore
    key = f"__reactive#{caller_name}#{name}"
    hash_key = f"__reactive_hash#{caller_name}#{name}"

    if dependency is not None and st.session_state.get(hash_key) != (
        hash_value := hash(dependency)
    ):
        st.session_state[hash_key] = hash_value
        if key in st.session_state:
            del st.session_state[key]

    if key not in st.session_state:
        st.session_state[key] = initial_value
    return Reactive(key)


@dataclass
class ReactiveFamily(Generic[T, K]):
    _key: str
    _keys: list[K]

    def get_key_for(self, key: str | int):
        return f"{self._key}[{key}]"

    def get(self, key: str | int, default: T | None = None) -> T | None:
        if key in self:
            return self[key]
        else:
            return default

    def keys(self):
        return (key for key in self._keys)

    def values(self):
        return (self[key] for key in self._keys)

    def items(self):
        return ((key, self[key]) for key in self._keys)

    def __contains__(self, key: str | int) -> bool:
        return self.get_key_for(key) in st.session_state

    def __getitem__(self, key: str | int) -> T:
        return st.session_state[self.get_key_for(key)]

    def __setitem__(self, key: str | int, value: T):
        st.session_state[self.get_key_for(key)] = value


@overload
def use_reactive_family(
    name: str, initial_value: dict[str, T], dependency: Hashable | None = None
) -> ReactiveFamily[T, str]: ...


@overload
def use_reactive_family(
    name: str, initial_value: list[T], dependency: Hashable | None = None
) -> ReactiveFamily[T, int]: ...


def use_reactive_family(
    name: str, initial_value: list[T] | dict[str, T], dependency: Hashable | None = None
) -> ReactiveFamily[T, str | int]:
    caller_name = inspect.currentframe().f_back.f_code.co_qualname  # type: ignore
    key = f"__reactive#{caller_name}#{name}"
    hash_key = f"__reactive_hash#{caller_name}#{name}"

    if dependency is not None and st.session_state.get(hash_key) != (
        hash_value := hash(dependency)
    ):
        st.session_state[hash_key] = hash_value
        if key in st.session_state:
            reactive: ReactiveFamily[T, str | int] = st.session_state[key]
            for item_key in reactive.keys():
                actual_key = reactive.get_key_for(item_key)
                if actual_key in st.session_state:
                    del st.session_state[actual_key]
            del st.session_state[key]

    if key not in st.session_state:
        if isinstance(initial_value, list):
            initial = dict(enumerate(initial_value))
        else:
            initial = initial_value
        reactive = ReactiveFamily(key, list(initial.keys()))
        st.session_state[key] = reactive
        for item_key, item_value in initial.items():
            reactive[item_key] = item_value
    else:
        reactive: ReactiveFamily[T, str | int] = st.session_state[key]

    return reactive
