from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import DefaultBase, UUIDAuditBase
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ._artist import Artist
    from ._audio_file import AudioFile
    from ._release import Release


class Track(UUIDAuditBase):
    """A playable catalog entry, optionally placed on a release."""

    __tablename__ = "track"
    __table_args__ = (
        CheckConstraint(
            "disc_number > 0",
            name="disc_number_positive",
        ),
        CheckConstraint(
            "track_number > 0",
            name="track_number_positive",
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
    release_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("release.id", ondelete="SET NULL"),
        index=True,
    )
    disc_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    track_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cover_storage_key: Mapped[str | None] = mapped_column(String, nullable=True)

    release: Mapped[Release | None] = relationship(
        back_populates="tracks",
        lazy="raise",
    )
    artist_credits: Mapped[list[TrackArtist]] = relationship(
        back_populates="track",
        cascade="save-update, merge, delete, delete-orphan",
        lazy="raise",
        order_by="TrackArtist.position",
        passive_deletes=True,
    )
    audio_files: Mapped[list[AudioFile]] = relationship(
        back_populates="track",
        cascade="save-update, merge, delete, delete-orphan",
        lazy="raise",
        passive_deletes=True,
    )


class TrackArtist(DefaultBase):
    """An artist's position in a track's ordered credits."""

    __tablename__ = "track_artist"
    __table_args__ = (
        CheckConstraint(
            "position > 0",
            name="position_positive",
        ),
        UniqueConstraint("track_id", "position"),
    )

    track_id: Mapped[UUID] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE"),
        primary_key=True,
    )
    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    track: Mapped[Track] = relationship(
        back_populates="artist_credits",
        lazy="raise",
    )
    artist: Mapped[Artist] = relationship(
        back_populates="track_credits",
        lazy="raise",
    )
