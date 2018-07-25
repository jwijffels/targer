from __future__ import print_function

import os.path
import torch
from classes.utils import read_CoNNL, write_CoNNL, read_CoNNL_dat_abs, write_CoNNL_dat_abs
from classes.evaluator import Evaluator
from classes.tag_component import TagComponent

print('Start!')

# Read data in CoNNL-2003 dat.abs format (Eger, 2017)
fn = 'data/persuasive_essays/Paragraph_Level/test.dat.abs'
token_sequences, tag_sequences = read_CoNNL_dat_abs(fn)

# Load tagger model
fn_checkpoint = 'tagger_model_es3_50ep.txt'
if os.path.isfile(fn_checkpoint):
    tagger = torch.load(fn_checkpoint)
else:
    raise ValueError('Can''t find tagger in file "%s". Please, run the main script with non-empty "--save_best_path" param to create it.' % fn_checkpoint)

# We take sequences_indexer from the tagger
sequences_indexer = tagger.sequences_indexer

# GPU device number, -1  means CPU
gpu = 0
if gpu >= 0:
    tagger = tagger.cuda(device=0)

# Get tags as sequences of strings
output_tag_sequences = tagger.predict_tags_from_tokens(token_sequences)

# Get scores
targets_idx = sequences_indexer.tag2idx(tag_sequences)
outputs_idx = sequences_indexer.tag2idx(output_tag_sequences)
acc = Evaluator.get_accuracy_token_level(targets_idx, outputs_idx)

#tag_components_test = TagComponent.extract_tag_components_sequences(token_sequences_test, tag_sequences_test)
target_tag_components_sequences_test = TagComponent.extract_tag_components_sequences(token_sequences, tag_sequences)
output_tag_components_sequences_test = TagComponent.extract_tag_components_sequences(token_sequences, output_tag_sequences)

f1 = Evaluator.get_f1(target_tag_components_sequences_test, output_tag_components_sequences_test)
print('\nAccuracy = %1.2f, F1 = %1.2f.\n' % (acc, f1))

# Macro-F1 for each class
print(Evaluator.get_f1_scores_details(tagger, token_sequences, tag_sequences))

# Write results to text file
#write_CoNNL('out.txt', token_sequences, tag_sequences, output_tag_sequences)
#write_CoNNL_dat_abs('oo.txt', token_sequences, output_tag_sequences)
#write_CoNNL_dat_abs('oo1.txt', token_sequences, tag_sequences)

print('\nThe end.')