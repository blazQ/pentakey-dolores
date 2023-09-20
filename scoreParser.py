from typing import List
from enum import Enum

timeSignatures: List[str] = ['timeSig6' ,'timeSig8' ,'timeSig3' ,'timeSig4' ,'timeSig2' ,'timeSig5' ,'timeSig7' ,'timeSig12' ,'timeSigCommon' ,'combTimeSignature']
notes: List[str] = ['SI_2', 'LA_2', 'SOL_2', 'FA_2', 'RE_2', 'MI_2', 'DO_2', 'SI_1', 'LA_1', 'MI_1', 'SOL_1', 'FA_1', 'RE_1', 'DO_1', 'SI_0', 'SOL_0', 'DO_0', 'FA_0', 'LA_0', 'MI_0', 'RE_0']
modifiers: List[str] = ['augmentationDot','keySharp','keyNatural','keyFlat','doubleSharp']
clefs: List[str] = ['gClef','fClef','cClefAlto']
rests: List[str] = ['rest8th','restQuarter','restWhole','rest16th','restHBar','rest32nd','rest64th']
durations: List[str] = ['flag8thDown','flag8thUp','noteheadHalf','flag16thUp','flag16thDown','flag64thDown','flag32ndDown']
metas: List[str] = ['SCORE','TITLE']
others: List[str] = ['barlineSingle','beam','brace']

class ScoreTypes(Enum):
    timeSignature, note, modifier, clef, rest, duration, meta, other = range(1, 9)

class ScoreElement:
    def __init__(self, type: ScoreTypes):
        self.type = type

    @classmethod
    def typeOf(cls, asString: str):
        if asString in timeSignatures:
            return ScoreTypes.timeSignature
        elif asString in notes:
            return ScoreTypes.note
        elif asString in modifiers:
            return ScoreTypes.modifier
        elif asString in clefs:
            return ScoreTypes.clef
        elif asString in rests:
            return ScoreTypes.rest
        elif asString in durations:
            return ScoreTypes.duration
        elif asString in metas:
            return ScoreTypes.meta
        elif asString in others:
            return ScoreTypes.other
        else:
            raise Exception('Element not recognized')

class TimeSignature(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.timeSignature)
        try:
            #TODO handle combTimeSignature and timeSigCommon case
            self.duration: int = int(asString.split('timeSig')[0])
        except:
            raise TypeError('Time Signature not recognized')

class Note(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.note)
        self.noteName: str = asString.split('_')[0]
        self.octave: int = int(asString.split('_')[1])

class Modifier(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.modifier)
        self.modifier: str = asString

class Clef(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.clef)
        self.noteName: str = asString.split('Clef')[0]

class Rest(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.rest)
        restDurationAsString: str = asString.split('rest')[0]
        try:
            self.restDuration: int = int(restDurationAsString[:-2])
        except:
            #TODO handle calculation of duration in these cases
            if restDurationAsString == 'Quarter':
                pass
            elif restDurationAsString == 'Whole':
                pass
            elif restDurationAsString == 'HBar':
                pass

class Duration(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.duration)
        if asString == 'flag8thDown' or asString == 'flag8thUp':
            self.noteDuration: int = 8
        elif asString == 'noteheadHalf':
            self.noteDuration = 2
        elif asString == 'flag16thUp' or asString == 'flag16thDown':
            self.noteDuration: int = 16
        elif asString == 'flag64thDown':
            self.noteDuration: int = 64
        elif asString == 'flag32ndDown':
            self.noteDuration: int = 32

class Meta(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.meta)
        self.meta: str = asString

class Other(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.other)
        self.other: str = asString


if __name__ == "__main__":
    pass



