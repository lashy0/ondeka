from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ._artist import Artist
    from ._track import Track


class ReleaseType(StrEnum):
    """Categories used to group releases."""

    ALBUM = "album"
    SINGLE = "single"
    EP = "ep"
    COMPILATION = "compilation"


class Release(UUIDAuditBase):
    """A release such as an album, single, EP, or compilation."""

    __tablename__ = "release"
    __table_args__ = (
        CheckConstraint(
            "year > 0",
            name="year_positive",
        ),
        CheckConstraint(
            "length(trim(title)) > 0",
            name="title_nonblank",
        ),
        CheckConstraint(
            "length(trim(cover_storage_key)) > 0",
            name="cover_storage_key_nonblank",
        ),
    )

    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    album_artist_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("artist.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    release_type: Mapped[ReleaseType | None] = mapped_column(
        Enum(
            ReleaseType,
            name="release_type",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            native_enum=False,
            create_constraint=True,
        ),
        nullable=True,
    )
    cover_storage_key: Mapped[str | None] = mapped_column(String, nullable=True)

    album_artist: Mapped[Artist | None] = relationship(
        back_populates="releases",
        lazy="raise",
    )
    tracks: Mapped[list[Track]] = relationship(
        back_populates="release",
        lazy="raise",
        passive_deletes=True,
    )
