from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import BigInteger, CheckConstraint, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ._track import Track


class AudioCodec(StrEnum):
    """The audio codecs supported by the catalog."""

    FLAC = "flac"
    MP3 = "mp3"
    AAC = "aac"
    ALAC = "alac"
    OPUS = "opus"
    VORBIS = "vorbis"


class AudioFile(UUIDAuditBase):
    """A stored audio file that can be used to play a track."""

    __tablename__ = "audio_file"
    __table_args__ = (
        CheckConstraint(
            "duration_ms > 0",
            name="duration_ms_positive",
        ),
        CheckConstraint(
            "size_bytes > 0",
            name="size_bytes_positive",
        ),
        CheckConstraint(
            "length(trim(storage_key)) > 0",
            name="storage_key_nonblank",
        ),
    )

    track_id: Mapped[UUID] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    storage_key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    container: Mapped[str | None] = mapped_column(String, nullable=True)
    codec: Mapped[AudioCodec] = mapped_column(
        Enum(
            AudioCodec,
            name="audio_codec",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            native_enum=False,
            create_constraint=True,
        ),
        nullable=False,
    )
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)

    track: Mapped[Track] = relationship(
        back_populates="audio_files",
        lazy="raise",
    )
