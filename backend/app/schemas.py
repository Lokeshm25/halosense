"""
Pydantic schemas — the single source of truth for all JSON shapes.
These MUST match CONTRACT.md exactly. If they diverge, CONTRACT.md wins.
"""

from enum import StrEnum

from pydantic import BaseModel, Field

# ── Enums ──────────────────────────────────────────────────────────

class MoodLabel(StrEnum):
    CALM     = "CALM"
    STRESSED = "STRESSED"
    TIRED    = "TIRED"
    UNKNOWN  = "UNKNOWN"


class Quadrant(StrEnum):
    HIGH_AROUSAL_NEGATIVE = "HIGH_AROUSAL_NEGATIVE"
    HIGH_AROUSAL_POSITIVE = "HIGH_AROUSAL_POSITIVE"
    LOW_AROUSAL_NEGATIVE  = "LOW_AROUSAL_NEGATIVE"
    LOW_AROUSAL_POSITIVE  = "LOW_AROUSAL_POSITIVE"


class TrendDirection(StrEnum):
    IMPROVING = "IMPROVING"
    STABLE    = "STABLE"
    DEGRADING = "DEGRADING"


# ── Core objects ───────────────────────────────────────────────────

class WordTiming(BaseModel):
    word:  str
    start: float
    end:   float


class ProsodyFeatures(BaseModel):
    arousal:   float = Field(..., ge=0.0, le=1.0)
    dominance: float = Field(..., ge=0.0, le=1.0)
    valence:   float = Field(..., ge=0.0, le=1.0)
    speech_rate_wps: float | None = None
    pause_ratio:     float | None = Field(None, ge=0.0, le=1.0)
    mean_pause_s:    float | None = None
    longest_pause_s: float | None = None
    rms_energy:  float | None = Field(None, ge=0.0, le=1.0)
    pitch_hz:    float | None = None
    duration_s:  float
    word_count:  int


class MoodVerdict(BaseModel):
    label:      MoodLabel
    confidence: float = Field(..., ge=0.0, le=1.0)
    stress_index:  float = Field(..., ge=0.0, le=1.0)
    fatigue_index: float = Field(..., ge=0.0, le=1.0)
    quadrant: Quadrant
    rationale: str
    contributing_factors: list[str] = []


class LapPoint(BaseModel):
    lap_number: int
    lap_time_s: float | None = None
    delta_s:    float | None = None
    compound:   str | None = None
    stint:      int | None = None
    tyre_life:  int | None = None
    is_pit_lap: bool = False
    is_accurate: bool = True
    track_status: str | None = None
    is_radio_lap: bool = False


class LapSeries(BaseModel):
    driver:    str
    race:      str
    baseline_s: float | None = None
    total_laps: int
    laps:      list[LapPoint]


class LapContext(BaseModel):
    lap_number:       int
    lap_time_s:       float | None = None
    baseline_s:       float | None = None
    delta_s:          float | None = None
    next_lap_delta_s: float | None = None
    prev_lap_delta_s: float | None = None
    compound:         str | None = None
    trend:            TrendDirection
    window: list[LapPoint] = []


class ClipAnalysis(BaseModel):
    clip_id: str
    source:  str
    driver: str | None = None
    race:   str | None = None
    lap:    int | None = None
    session_type: str | None = None
    transcript: str
    words: list[WordTiming] = []
    asr_model: str
    prosody: ProsodyFeatures
    mood:    MoodVerdict
    lap_context: LapContext | None = None
    audio_url: str
    audio_peaks: list[float] = []
    processed_at: str
    processing_ms: int
    mocked: bool = False


class ClipSummary(BaseModel):
    clip_id:    str
    driver:     str | None = None
    race:       str | None = None
    lap:        int | None = None
    duration_s: float
    mood_label: MoodLabel
    stress_index: float
    delta_s:    float | None = None
    transcript_preview: str
    audio_url:  str


class CorrelationPoint(BaseModel):
    clip_id:      str
    driver:       str | None = None
    stress_index: float
    delta_s:      float
    mood_label:   MoodLabel


class CorrelationSummary(BaseModel):
    n: int
    pearson_r: float | None = None
    p_value:   float | None = None
    pearson_r_next_lap: float | None = None
    mean_delta_by_mood: dict[str, float] = {}
    points: list[CorrelationPoint] = []
    headline: str


class HealthStatus(BaseModel):
    status: str = "ok"
    mock_ml: bool
    models_loaded: bool
    clip_count: int
    version: str = "1.0.0"


class EvalSummary(BaseModel):
    n_labeled: int = 0
    agreement_rate: float | None = None
    confusion_matrix: dict | None = None
    mean_stress_by_human_label: dict | None = None
    notes: str = ""


class ErrorResponse(BaseModel):
    error: str
    detail: str
    hint: str | None = None
