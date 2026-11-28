from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ._release import Release
    from ._track import TrackArtist


class Artist(UUIDAuditBase):
    """An artist credited on tracks or releases."""

    __tablename__ = "artist"
    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="name_nonblank",
        ),
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    releases: Mapped[list[Release]] = relationship(
        back_populates="album_artist",
        lazy="raise",
        passive_deletes=True,
    )
    track_credits: Mapped[list[TrackArtist]] = relationship(
        back_populates="artist",
        cascade="save-update, merge, delete, delete-orphan",
        lazy="raise",
        passive_deletes=True,
    )
