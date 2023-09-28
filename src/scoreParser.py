from typing import List
from enum import Enum
from pymusicxml import *

timeSignatures: List[str] = ['timeSig6', 'timeSig8', 'timeSig3', 'timeSig4',
                             'timeSig2', 'timeSig5', 'timeSig7', 'timeSig12', 'timeSigCommon', 'combTimeSignature']
notes: List[str] = ['SI_2', 'LA_2', 'SOL_2', 'FA_2', 'RE_2', 'MI_2', 'DO_2', 'SI_1', 'LA_1',
                    'MI_1', 'SOL_1', 'FA_1', 'RE_1', 'DO_1', 'SI_0', 'SOL_0', 'DO_0', 'FA_0', 'LA_0', 'MI_0', 'RE_0']
modifiers: List[str] = ['beam', 'augmentationDot',
                        'keySharp', 'keyNatural', 'keyFlat', 'doubleSharp']
clefs: List[str] = ['gClef', 'fClef', 'cClefAlto']
rests: List[str] = ['rest8th', 'restQuarter', 'restWhole',
                    'rest16th', 'restHBar', 'rest32nd', 'rest64th']
durations: List[str] = ['flag8thDown', 'flag8thUp', 'noteheadHalf',
                        'flag16thUp', 'flag16thDown', 'flag64thDown', 'flag32ndDown']
metas: List[str] = ['SCORE', 'TITLE']
others: List[str] = ['barlineSingle', 'brace']


class ScoreTypes(Enum):
    timeSignature, note, modifier, clef, rest, duration, meta, other = range(
        1, 9)


class ScoreElement:
    def __init__(self, type: ScoreTypes, asString: str):
        self.type = type
        self.asString = asString

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

    @classmethod
    def initScoreElement(cls, asString: str):
        if asString in timeSignatures:
            return MyTimeSignature(asString)
        elif asString in notes:
            return MyNote(asString)
        elif asString in modifiers:
            return MyModifier(asString)
        elif asString in clefs:
            return MyClef(asString)
        elif asString in rests:
            return MyRest(asString)
        elif asString in durations:
            return Duration(asString)
        elif asString in metas:
            return MyMeta(asString)
        elif asString in others:
            return MyOther(asString)
        else:
            raise Exception('Element not recognized')


class MyTimeSignature(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.timeSignature, asString)
        if asString in ['timeSigCommon', 'combTimeSignature']:
            pass  # Nothing more to do
        else:
            try:
                self.duration: int = int(asString.split('timeSig')[0])
            except:
                raise TypeError('Time Signature not recognized')


class MyNote(ScoreElement):
    itToIntMapping = {
        'DO': 'c',
        'RE': 'd',
        'MI': 'e',
        'FA': 'f',
        'SOL': 'g',
        'LA': 'a',
        'SI': 'b'
    }

    def __init__(self, asString: str):
        super(ScoreTypes.note, asString)
        self.pitch: str = self.itToIntMapping.get(asString.split('_')[0])
        self.octave: int = int(asString.split('_')[1])


class MyModifier(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.modifier, asString)


class MyClef(ScoreElement):
    pitchToLine = {
        'c': 3,
        'f': 4,
        'g': 2
    }

    def __init__(self, asString: str):
        super(ScoreTypes.clef, asString)
        self.pitch: str = asString.split('Clef')[0].lower()
        self.line: int = self.pitchToLine.get(self.pitch)


class MyRest(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.rest, asString)
        if asString == 'rest8th':
            self.restDuration: str = 'eighth'
        elif asString == 'restQuarter':
            self.restDuration: str = 'quarter'
        elif asString == 'restWhole':
            self.restDuration: str = 'hole'
        elif asString == 'rest16th':
            self.restDuration: str = '16th'
        elif asString == 'restHBar':
            pass  # TODO handle this
        elif asString == 'rest32nd':
            self.restDuration: str = '32nd'
        elif asString == 'rest64th':
            self.restDuration: str = '64th'


class MyDuration(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.duration, asString)
        if asString == 'flag8thDown' or asString == 'flag8thUp':
            self.noteDuration: str = 'eighth'
        elif asString == 'noteheadHalf':
            self.noteDuration: str = 'half'
        elif asString == 'flag16thUp' or asString == 'flag16thDown':
            self.noteDuration: str = '16th'
        elif asString == 'flag64thDown':
            self.noteDuration: str = '64th'
        elif asString == 'flag32ndDown':
            self.noteDuration: str = '32nd'


class MyMeta(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.meta, asString)


class MyOther(ScoreElement):
    def __init__(self, asString: str):
        super(ScoreTypes.other, asString)


class ScoreElementNotFoundInLine(Exception):
    pass


class DurationalObjectMappingNotFound(Exception):
    pass

# def lineToScoreElement(line: str):
#     if line.strip().startswith('Name:'):
#         return ScoreElement.initScoreElement(line.split('Name:')[1].strip())
#     else:
#         raise ScoreElementNotFoundInLine


def scoreElementToDurationalObject(scoreElement: ScoreElement):
    if isinstance(scoreElement, MyNote):
        myNote: MyNote = scoreElement
        return Note(Pitch(myNote.pitch, myNote.octave + 3), Duration('quarter'))
    elif isinstance(scoreElement, MyClef):
        myClef: MyClef = scoreElement
        return Clef(myClef.pitch, myClef.line)
    elif isinstance(scoreElement, MyRest):
        myRest: MyRest = scoreElement
        return Rest(Duration(myRest.restDuration))
    elif isinstance(scoreElement, MyDuration):
        myDuration: MyDuration = scoreElement
        return Duration(myDuration.noteDuration)
    else:
        raise DurationalObjectMappingNotFound


def makeScore(scoreTitle: str = 'Test Score', partName: str = 'Test Part'):
    # New Score
    newScore = Score(title=scoreTitle)
    # New part
    newPart = Part(part_name=partName)
    # Append part to the score
    newScore.append(newPart)
    # That's it
    return newScore


if __name__ == "__main__":

    # Make score
    score: Score = makeScore()

    # Measures list
    measures: [Measure] = []

    # Open file

    # Parse JSON

    # Add all elements in the JSON to a list

    # For each element in the list, parse it and add it to a measure
    measure: Measure = Measure(time_signature=(3,4))
    
    # If it's a 'barlineSingle', add current measure to measures list and start a new one
    score.parts[0].extend(measure)

    
    ########################

    # TODO handle TimeSignature (to specify to each measure)

    # Add all elements to measure
    # This will be a for in
    # measure.append(Note('c', 'whole'))

    # Add measure to measures list
    # measures.append(measure)

    # Add measures to part
    # score.parts[0].extend(measures)

    # Export score
    # score.export_to_file("./results/TestScore.musicxml")
