import json
from typing import List
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


class ScoreElement(object):
    def __init__(self, type: ScoreTypes, asString: str):
        self.type = type
        self.asString = asString

    @classmethod
    def typeOf(cls, asString: str):
        if asString in timeSignatures or asString.split('-')[0] in timeSignatures: # dirty workaround
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
            raise Exception('Element not recognized - ', asString)

    @classmethod
    def initScoreElement(cls, asString: str):
        if asString in timeSignatures or asString.split('-')[0] in timeSignatures: # dirty workaround
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
            return MyDuration(asString)
        elif asString in metas:
            return MyMeta(asString)
        elif asString in others:
            return MyOther(asString)
        else:
            raise Exception('Element not recognized - ', asString)


class MyTimeSignature(ScoreElement):
    def __init__(self, asString: str):
        super().__init__(ScoreTypes.timeSignature, asString)
        if asString in ['timeSigCommon', 'combTimeSignature']:
            pass  # Nothing more to do
        else:
            try:
                self.duration: int = int(asString.split('timeSig')[1].split('-')[0])
                self.tag: str = asString.split('-')[1] #num or den
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
        super().__init__(ScoreTypes.note, asString)
        self.pitch: str = self.itToIntMapping.get(asString.split('_')[0])
        self.octave: int = int(asString.split('_')[1])


class MyModifier(ScoreElement):
    def __init__(self, asString: str):
        super().__init__(ScoreTypes.modifier, asString)


class MyClef(ScoreElement):
    pitchToLine = {
        'c': 3,
        'f': 4,
        'g': 2
    }

    def __init__(self, asString: str):
        super().__init__(ScoreTypes.clef, asString)
        self.pitch: str = asString.split('Clef')[0].lower()
        self.line: int = self.pitchToLine.get(self.pitch)


class MyRest(ScoreElement):
    def __init__(self, asString: str):
        super().__init__(ScoreTypes.rest, asString)
        if asString == 'rest8th':
            self.restDuration: str = 'eighth'
        elif asString == 'restQuarter':
            self.restDuration: str = 'quarter'
        elif asString == 'restWhole':
            self.restDuration: str = 'whole'
        elif asString == 'rest16th':
            self.restDuration: str = '16th'
        elif asString == 'restHBar':
            pass
        elif asString == 'rest32nd':
            self.restDuration: str = '32nd'
        elif asString == 'rest64th':
            self.restDuration: str = '64th'


class MyDuration(ScoreElement):
    def __init__(self, asString: str):
        super().__init__(ScoreTypes.duration, asString)
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
        super().__init__(ScoreTypes.meta, asString)


class MyOther(ScoreElement):
    def __init__(self, asString: str):
        super().__init__(ScoreTypes.other, asString)


class DurationalObjectMappingNotFound(Exception):
    pass


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

    # List containing all elements that will be read from the json file
    allElementsAsStrings: [str] = []

    # Open file
    with open('/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results/risultato_normalizzato.json') as f:
        # Parse JSON
        data = json.load(f)[0]

        # Add all elements in the JSON to a list
        allElementsAsStrings = [element['name'] for line in data for element in line]  # Python's crazy

    # Create new measure
    # Arbitray values for TS and Key, but we need them to have properties to modify while we read the Score from the .json
    measure: Measure = Measure(time_signature=(3, 4), key=0)

    # Logic to determine if duration changing is needed
    duration: Duration = None
    changeDurationSemaphore: bool = False

    # For each element in the list, parse it (e te pare facile) and add it to the measure
    for element in allElementsAsStrings:
        scoreElement: ScoreElement = ScoreElement.initScoreElement(element)
        try:
            durationalObject = scoreElementToDurationalObject(scoreElement)
            if isinstance(durationalObject, Clef):
                try:
                    if measure.clef.pitch == durationalObject.pitch and measure.clef.line == durationalObject.line:
                        pass
                    else:
                        measure.clef = durationalObject
                except AttributeError:
                    pass
                continue
            elif isinstance(durationalObject, Duration):
                duration = durationalObject
                changeDurationSemaphore = True
                continue
            elif changeDurationSemaphore:
                durationalObject.duration = duration
                changeDurationSemaphore = False
            measure.append(durationalObject)
        except DurationalObjectMappingNotFound:
            if scoreElement.type == ScoreTypes.other:
                if scoreElement.asString == 'barlineSingle':
                    # Add actual measure to the measures list
                    measures.append(measure)
                    # Finish actual measure and start a new one - no TS and Key 'cause otherwise they'll be displayed and we don't need this
                    newMeasure: Measure = Measure()
                    measure = newMeasure
                elif scoreElement.asString == 'brace':
                    pass
            elif scoreElement.type == ScoreTypes.modifier:
                if scoreElement.asString == 'beam':
                    pass
                elif scoreElement.asString == 'augmentationDot':
                    measure.contents[-1].duration.num_dots += 1
                elif scoreElement.asString == 'keySharp':
                    try:
                        measure.contents[-1].pitch.alteration += 1
                    except IndexError:
                        # It's a key signature
                        try:
                            measure.key += 1
                        except TypeError:
                            continue
                elif scoreElement.asString == 'keyNatural':
                    try:
                        measure.contents[-1].pitch.alteration = 0
                    except IndexError:
                        # It's a key signature
                        measure.key = 0
                elif scoreElement.asString == 'keyFlat':
                    try:
                        measure.contents[-1].pitch.alteration -= 1
                    except IndexError:
                        # It's a key signature
                        measure.key -= 1
                elif scoreElement.asString == 'doubleSharp':
                    try:
                        measure.contents[-1].pitch.alteration += 2
                    except IndexError:
                        # It's a key signature
                        measure.key += 2
            elif scoreElement.type == ScoreTypes.timeSignature:
                try:
                    actualTimeSignature: tuple = measure.time_signature
                    if scoreElement.tag == 'num':
                        measure.time_signature = (scoreElement.duration, actualTimeSignature[1])
                    elif scoreElement.tag == 'den':
                        measure.time_signature = (actualTimeSignature[0], scoreElement.duration)
                except AttributeError:
                    continue
            elif scoreElement.type == ScoreTypes.meta:
                pass

    filteredMeasures = [m for m in measures if len(m.contents)!=0]
    score.parts[0].extend(filteredMeasures)

    # Open file to capture name
    with open('/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results/risultato.json') as f:
        # Parse JSON
        data = json.load(f)[0]

        # Find name
        filename = data['filename'].split('/')[-1].split('.')[0]
        
        # Export score
        score.export_to_file(f"/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results/{filename}.musicxml")