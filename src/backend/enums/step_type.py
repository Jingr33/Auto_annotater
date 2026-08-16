from enum import Enum


class StepType(str, Enum):
    LOAD = 'LOAD'
    ANNOTATE = 'ANNOTATE'
    SELECT = 'SELECT'
