# evolutionary_algorithm

## Manual for running my program:
1)	Install following Python libraries: mido, music21
2)	Prepare .mid input file with simple song (better in one octave)
3)	Place this song near code file .py
4)	Edit in code variables for input and output file
5)	Run the program
6)	Listen output .mid file with initial song and generated accompaniment
## Algorithm flow:
1)	Key detection algorithm:
	I use music21 library for song’s key detection and save the result into two variables: mid_mode and mid_scale.
2)	Parsing initial .mid file:
I use mido library for parsing. Firstly, I find the number of chords from accompaniment and create the list of mido.Message with this size. After that I divide initial song into sections of chord’s duration and put in every section first note from song. Now each chord will depend on his relevant note from initial song.
3)	Evolutionary algorithm:
Population consists of chromosomes with their chords list and score.
Chord – base note and list with integer notation of chord. Integer notation can represent major, minor and dim chords.
Chromosome – list of chords and score.
Chromosome has score field – rating for evolutionary algorithm. The flow of rating algorithm:
Check each chord from chromosome and rate by following criteria:
1) Each note of chord have minimum dissonance;
2) Chord fit for song tonic;
3) Chord’s base note fit for their type’s rules.
Each iteration (in my algorithm I have 1000 iterations) of evolution algorithm consists of crossovers, mutations, ratings, and cuttings off weak individuals from population.
Crossover: we take 2 random individuals from population and create 2 new individuals from their halves.
 Mutation: we take random individual and swap 2 chords in his chords list. Therefore, we get new individual.
Rating: we compute rating for each chromosome by rating algorithm (which is described above). After that we sort population by this rating score and cut off individuals with minimum rating from population.
4)	Saving song with generated accompaniment:
Add list of the best chromosome to the tracks of the initial song and save to the new output file by using mido functionality.
