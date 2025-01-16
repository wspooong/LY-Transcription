from pydantic import BaseModel


class TranscriptClass(BaseModel):
    filename: str
    index: int
    page_number: str | None
    speaker: str
    content: str


class GazetteInfo(BaseModel):
    comYear: str
    comVolume: str
    comBookId: str
    term: str
    sessionPeriod: str
    sessionTimes: str
    meetingTimes: str
    agendaNo: str
    agendaType: str
    meetingDate: str
    subject: str
    pageStart: str
    pageEnd: str
    docUrl: str
    selectTerm: str
