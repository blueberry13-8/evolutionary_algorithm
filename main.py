import random
import mido
import music21

"""Names of input and output files, var-s for evolutionary algorithm"""
INPUT_NAME = 'input3.mid'
OUTPUT_FILE = 'output3.mid'
ITERATIONS = 500
POPULATION_SIZE = 100
CROSS_NUMBER = 15
MUTATE_NUMBER = 30


class Chord:
    def __init__(self, base: int, third: list):
        """Class of chord.
            base - Base note of chord.
            third - Integer notation of chord.
        """
        self.base = base
        self.note_list = third

    def __eq__(self, other):
        """Compare chords by their fields"""
        return type(other) == Chord and self.base == other.base and self.note_list == other.note_list


class Chromosome:
    def __init__(self, chords: list):
        """Class of chromosome for evolutionary algorithm.
            chords - List of Chord instances for accompaniment.
        """
        self.size = len(chords)
        self.chords = chords
        self.score = 0
        if self.size != 0:
            return
        """Initialize random chords if we get empty chords' list"""
        for q in range(len(init_notes)):
            self.chords.append(Chord(random.randint(0, 120), random.choice(ALL_CHORDS)))

    def __eq__(self, other):
        """Compare chromosomes by their scores from evolutionary algorithm"""
        return self.score == other.score

    def __lt__(self, other):
        """Compare chromosomes by their scores from evolutionary algorithm"""
        return self.score < other.score

    def update_rating(self):
        """Update rating of current chromosome"""
        self.score = 0
        """Go through all chords"""
        for j in range(len(self.chords)):
            """Check each note from note_list of chord"""
            for k in range(3):
                """Note from chord and relevant note from original song"""
                chord_note = self.chords[j].note_list[k] + self.chords[j].base
                original_song_note = 0
                # if init_notes[j] is not None:
                #     original_song_note = init_notes[j].note
                """Check for dissonance"""
                ind = dissonance_scale.index((original_song_note - chord_note) % 12)
                if ind < 4:
                    self.score += 8
                else:
                    self.score -= 8
            """Check for tonic"""
            if mid_tonic - 25 < self.chords[j].base < mid_tonic - 8:
                self.score += 20
            else:
                self.score -= 20
            """Chord in his correct steps"""
            if self.chords[j].base % 12 in self.__check_base(j):
                self.score += 20

    def __check_base(self, ind: int):
        """Return the set of relevant scales for current chord according to his type and the original song scale"""
        # Cheat sheet: convert from original scales to midi scales
        # 0 2 4 5 7 9 11
        # 0 2 3 5 7 8 10
        if mid_mode == 'major':
            if self.chords[ind].note_list == ALL_CHORDS[0]:
                return {0, 5, 7}
            elif self.chords[ind].note_list == ALL_CHORDS[1]:
                return {2, 4, 9}
            elif self.chords[ind].note_list == ALL_CHORDS[2]:
                return {11}
        else:
            if self.chords[ind].note_list == ALL_CHORDS[0]:
                return {0, 5, 7}
            elif self.chords[ind].note_list == ALL_CHORDS[1]:
                return {3, 8, 10}
            elif self.chords[ind].note_list == ALL_CHORDS[2]:
                return {2}


"""Dissonance scale for checking of chords' fitting"""
dissonance_scale = [0, 7, 5, 4, 8, 3, 9, 10, 2, 6, 11, 1]


def cross(mother: Chromosome, father: Chromosome):
    """Crossover of 2 chromosomes from population. Return 2 new chromosomes"""
    chords1 = mother.chords[:len(mother.chords) // 2] + father.chords[len(father.chords) // 2:]
    chords2 = father.chords[:len(father.chords) // 2] + mother.chords[len(mother.chords) // 2:]
    gen1 = Chromosome(chords1)
    gen2 = Chromosome(chords2)
    return [gen1, gen2]


def mutate(ind1: Chromosome, ind2: Chromosome):
    """Mutate 2 individuals from population. Mutate by swap of 2 chords in their chord' lists"""
    r_1 = random.randint(0, ind1.size - 1)
    r_2 = random.randint(0, ind1.size - 1)
    ind1.chords[r_1], ind1.chords[r_2] = ind1.chords[r_2], ind1.chords[r_1]
    r_1 = random.randint(0, ind2.size - 1)
    r_2 = random.randint(0, ind2.size - 1)
    ind2.chords[r_1], ind2.chords[r_2] = ind2.chords[r_2], ind2.chords[r_1]


def notes_number():
    """Compute number of places for accompaniment chords"""
    time = 0
    for track_1 in mid_file.tracks:
        for note in track_1:
            time += note.time
    return (time + CHORD_TIME - 1) // CHORD_TIME


def get_input_notes():
    """Creation of list with original notes for each quarter"""
    notes = [None] * ac_note_number
    time = 0
    for track_1 in mid_file.tracks:
        for note in track_1:
            if type(note) is mido.Message:
                if note.type == 'note_off':
                    time += note.time
                if note.type == 'note_on' and time % CHORD_TIME == 0:
                    if notes[time // CHORD_TIME] is None:
                        notes[time // CHORD_TIME] = note
                    time += note.time
    for k in range(1, len(notes)):
        if notes[k] is None and notes[k - 1] is not None:
            notes[k] = notes[k - 1]
    return notes


def init_population():
    """Creation of initial random population for evolutionary algorithm"""
    temp_population = []
    for q in range(POPULATION_SIZE):
        temp_population.append(Chromosome([]))
    return temp_population


"""Original song"""
mid_file = mido.MidiFile(INPUT_NAME, clip=True)
"""Tonic of original song"""
mid_tonic = music21.converter.parse(INPUT_NAME).analyze('key').tonic.midi
"""Scale of original song"""
mid_mode = music21.converter.parse(INPUT_NAME).analyze('key').mode
"""List of lists with integer notations for some chords"""
#             major       minor      dim        sus4       sus2
ALL_CHORDS = [[0, 4, 7], [0, 3, 7], [0, 3, 6]]  # [0, 5, 7], [0, 2, 7]]
"""Duration of chords(1/4)"""
CHORD_TIME = mid_file.ticks_per_beat
"""Number of places for accompaniment chords"""
ac_note_number = notes_number()
"""List of notes from original song"""
init_notes = get_input_notes()
"""Population of chromosomes for evolutionary algorithm"""
population = init_population()
"""Do iterations of evolutionary algorithm"""
for t in range(ITERATIONS):
    """Perform crossover for random individuals"""
    for i in range(CROSS_NUMBER):
        r1 = random.randint(0, POPULATION_SIZE - 1)
        r2 = random.randint(0, POPULATION_SIZE - 1)
        population += cross(population[r1], population[r2])
    """Perform mutation for random individuals"""
    for i in range(MUTATE_NUMBER):
        r1 = random.randint(0, POPULATION_SIZE - 1)
        r2 = random.randint(0, POPULATION_SIZE - 1)
        mutate(population[r1], population[r2])
    """Update rating for each individual and sort them"""
    for i in range(len(population)):
        population[i].update_rating()
    population.sort()
    """Cut off weak individuals"""
    population = population[len(population) - POPULATION_SIZE:]
"""List for the best accompaniment"""
solution = []
"""Add all chords' notes to this list"""
for chord in population[-1].chords:
    solution.append(mido.Message('note_on', channel=0, note=chord.note_list[0] + chord.base, velocity=50, time=0))
    solution.append(mido.Message('note_on', channel=0, note=chord.note_list[1] + chord.base, velocity=50, time=0))
    solution.append(mido.Message('note_on', channel=0, note=chord.note_list[2] + chord.base, velocity=50, time=0))
    solution.append(
        mido.Message('note_off', channel=0, note=chord.note_list[0] + chord.base, velocity=50, time=CHORD_TIME))
    solution.append(mido.Message('note_off', channel=0, note=chord.note_list[1] + chord.base, velocity=50, time=0))
    solution.append(mido.Message('note_off', channel=0, note=chord.note_list[2] + chord.base, velocity=50, time=0))
"""Add accompaniment to the original song and save to the output file"""
mid_file.tracks.append(solution)
mid_file.save(OUTPUT_FILE)
