from time import time
from typing import Iterable, Iterator, Sized

import streamlit as st


def st_tqdm[
    T
](
    seq: Iterable[T], title: str = "", total: int | None = None, with_time: bool = True
) -> Iterator[T]:
    if isinstance(seq, Sized):
        total = len(seq)

    if total is not None:
        start = time()
        bar = st.progress(
            0.0,
            f"{title} [0/{total}]"
            + (" (elapsed: 0s, remaining: **s)" if with_time else ""),
        )
        for i, value in enumerate(seq):
            yield value

            ratio = float(i + 1) / total
            elapsed = time() - start
            remaining = (elapsed / ratio) - elapsed
            bar.progress(
                ratio,
                f"{title} [{i + 1}/{total}]"
                + (
                    f" (elapsed: {elapsed:.2f}s, remaining: {remaining:.2f}s)"
                    if with_time
                    else ""
                ),
            )
        bar.empty()
    else:
        with st.spinner(title):
            yield from seq
