import json

from config import DefaultConfig
from shapely.geometry import Polygon

def get_scores(obj):
    # Getting only the scores for reordering purposes
    return [x for x in obj if x['name'] == 'SCORE']

def score_sort_key(ll_score):
    # Returns the y coordinate for the score
    return ll_score['relative_coordinates']['center_y']

def object_sort_key(obj):
    return obj['relative_coordinates']['center_x']

# List of list of scores.
# One list of scores for every frame in the result.json.
def get_arranged_output(output_file):
    # Opens the file in read only mode.
    data = []
    with open(output_file, 'r') as file:
    # Reads the content as JSON object
        data = json.load(file)

    # This will maintain the list of list of scores necessary to sort the readings by row, for the current frame.
    # This will maintain the list of rows
    arranged_output = []
    for entry in data:
        arranged_entry_output = []
        # Passing found classes to the get scores function and ordering them based on the Y coordinate.
        entry_scores = get_scores(entry['objects'])
        entry_scores.sort(key=score_sort_key)
        # Scores are sorted so we'll explore them top to bottom.
        for score in entry_scores:
            # Add for every score object the notes that fall within its boundaries
            # print(score['relative_coordinates']['center_y'])
            # print(score['relative_coordinates']['height'])
            # For every score we create a list that contains all of the objects for said score.
            score_scope = []
            for obj in entry['objects']:
                if score['relative_coordinates']['center_y'] - (score['relative_coordinates']['height']/2) <= obj['relative_coordinates']['center_y'] <= score['relative_coordinates']['center_y'] + (score['relative_coordinates']['height']/2):
                    score_scope.append(obj)

            # Refine this step so that we know which comes first and which comes second when there's a half notehead.
            score_scope.sort(key=object_sort_key)
            # Adding current row to the arranged entry output
            arranged_entry_output.append(score_scope)
        arranged_output.append(arranged_entry_output)
    return arranged_output


def get_intersected_elements(row, beam):
    intersected_elements = []
    beam_center_x = beam['relative_coordinates']['center_x']
    beam_center_y = beam['relative_coordinates']['center_y']
    height = beam['relative_coordinates']['height']
    width = beam['relative_coordinates']['width']

    beam_box = Polygon([(beam_center_x - width/2, beam_center_y - height/2), (beam_center_x + width/2, beam_center_y - height/2), (beam_center_x + width/2, beam_center_y + height/2), (beam_center_x-width/2, beam_center_y+height/2)])
    for element in row:
        if element['name'] != 'beam' and element['name'] != 'SCORE':
            element_center_x = element['relative_coordinates']['center_x']
            element_center_y = element['relative_coordinates']['center_y']
            element_height = element['relative_coordinates']['height']
            element_width = element['relative_coordinates']['width']
            element_box = Polygon([(element_center_x - element_width/2, element_center_y - element_height/2), (element_center_x + element_width/2, element_center_y - element_height/2), (element_center_x + element_width/2, element_center_y + element_height/2), (element_center_x-element_width/2, element_center_y+element_height/2)])
            if beam_box.intersects(element_box):
                intersected_elements.append(element)
    return intersected_elements

def extract_beams(arranged_output):
    counter = 0
    for entry in arranged_output:
        for row in entry:
            for element in row:
                if element['name']=='beam':
                    counter+=1
                    # search in the row
                    intersecting_notes = get_intersected_elements(row, element)
                    #print(f"Sono il beam {counter}! Queste sono le note che contengo.")
                    #print(intersecting_notes)
                    for intersected_element in intersecting_notes:
                        # If I already found this note in another beam
                        if 'beams' in intersected_element.keys():
                            intersected_element['beams'] += 1
                        # If this is the first beam this note touches
                        else:
                            intersected_element['beams'] = 1
    return arranged_output


def map_to_json(beam_number):
    if beam_number == 1:
        return {'name': 'flag8thUp'}
    elif beam_number == 2:
        return {'name': 'flag16thUp'}
    elif beam_number == 3:
        return {'name': 'flag32ndUp'}
    elif beam_number == 4:
        return {'name': 'flag64thUp'}

def normalize_durations(arranged_output):
    beams_normalized_output = extract_beams(arranged_output)
    for entry in arranged_output:
        for row in entry:
            index = 0
            while index < len(row):
                element = row[index]
                if 'beams' in element.keys():
                    # create an equivalent json object
                        element_to_add = map_to_json(element['beams'])
                    # add it after the current note
                        row.insert(index, element_to_add)
                        index+=1
                index+=1
    return beam_removal(beams_normalized_output)

def beam_removal(beam_normalized_output):
    return [[[element for element in row if element['name'] != 'beam'] for row in entry] for entry in beam_normalized_output]


def element_higher(element, suspect):
    element_center = element['relative_coordinates']['center_y']
    suspect_center = suspect['relative_coordinates']['center_y']
    if element_center < suspect_center:
        return True
    else: return False


def tagTimeSign(beams_cleaned_output):
    for entry in beams_cleaned_output:
        for row in entry:
            for element in row:
                if 'timeSig' in element['name']:
                    # Check if you haven't already tagged it
                    if 'tag' not in element.keys():
                        element['tag'] = 0
                        # Search for the other one
                        # Obviously you can do it in a more efficient way by thinking about the problem from the start
                        # Simple brutal solution
                        for suspect in row:
                            # If it's the other timeSig
                            if 'timeSig' in suspect['name'] and 'tag' not in suspect.keys():
                                # Check which one is the denominator and which one is the numerator
                                # Returns true if element is higher than suspect
                                if element_higher(element, suspect):
                                    element['tag'] = 'num'
                                    suspect['tag'] = 'den'
                                else:
                                    element['tag'] = 'den'
                                    suspect['tag'] = 'num'



def write_output(arranged_output, file_name):
    with open(file_name, 'w') as out:
        json.dump(arranged_output, out)



arranged_output = get_arranged_output(DefaultConfig.INPUT_FOLDER + "/" + DefaultConfig.INPUT_FILE)
beams_cleaned_normalized_output = normalize_durations(arranged_output)
tagTimeSign(beams_cleaned_normalized_output)
write_output(beams_cleaned_normalized_output, DefaultConfig.OUTPUT_FOLDER + "/" + DefaultConfig.OUTPUT_NORMALIZED_FILE)

# After executing the function, you will have a list of lists (of lists, since there could be more frames). Every list inside the ll will be a row of the score.
# All of the "beam" element will be replaced by an information on how many beam there are for each note and every note will be followed (or preceded, up to you) by its duration class.
# Just as an example here's the first line.
# This approach will make us lose some specific beam patterns, but the other viable option is to basically have a beam group and basically redo the class model from scratch.


#print([x['name'] for x in beams_cleaned_normalized_output[0][0]])

# Here, arranged output is [0][0] because the input melody has only one frame, so there's always the first [0].
