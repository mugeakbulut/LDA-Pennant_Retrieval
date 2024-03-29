# -*- coding: utf-8 -*-
"""Kesme noktalarında mmr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ei56xhKFudXvXH-nQxiK-nxFHbmobkGv
"""

from sklearn.metrics.pairwise import cosine_similarity
def maximal_marginal_relevance(sentence_vector, phrases, embedding_matrix, lambda_constant=0.9, threshold_terms=5):
    """
    Return ranked phrases using MMR. Cosine similarity is used as similarity measure.
    :param sentence_vector: Query vector
    :param phrases: list of candidate phrases
    :param embedding_matrix: matrix having index as phrases and values as vector
    :param lambda_constant: 0.5 to balance diversity and accuracy. if lambda_constant is high, then higher accuracy. If lambda_constant is low then high diversity.
    :param threshold_terms: number of terms to include in result set
    :return: Ranked phrases with score
    """
    # todo: Use cosine similarity matrix for lookup among phrases instead of making call everytime.
    s = []
    print(sorted(phrases))
    r = sorted(phrases,  reverse=True)

    r = [i.split() for i in r]

    k = []
    for i in r:
        for j in i:
            k.append(j)

    r = k
    print(r)
    while len(r) > 0:
        score = 0
        phrase_to_add = ''
        for i in r:

            first_part = cosine_similarity([sentence_vector[i]], [embedding_matrix[i]])[0][0]
            second_part = 0
            #print("i =" + str(i))
            for j in s:
                cos_sim = cosine_similarity([embedding_matrix[i]], [embedding_matrix[j[0]]])[0][0]
                #print("j =" + str(j))
                if cos_sim > second_part:
                    second_part = cos_sim
            equation_score = lambda_constant * (first_part) - (1 - lambda_constant) * second_part
            if equation_score > score:
                score = equation_score
                phrase_to_add = i
        if phrase_to_add == '':
            phrase_to_add = i
        r.remove(phrase_to_add)
        s.append((phrase_to_add, score))
    return (s, s[:threshold_terms])[threshold_terms > len(s)]

#dene

#manual_title = ['']

manual_title = ['On the Selection and Evolution of Regulatory DNA Motifs',
'Increased Concentration of Polyvalent Phospholipids in the Adsorption Domain of a Charged Protein',
'Surface-dependent Coagulation Enzymes: Flow Kinetics of Factor Xa Generation on Live Membranes',
'Physics of Solutions and Networks of Semiflexible Macromolecules and the Control of Cell Function',
'The osmotic pressure of charged colloidal suspensions: A unified approach to linearized Poisson-Boltzmann theory',
'Theoretical aspects of vertical and lateral manipulation of atoms',
'Complexation of a polyelectrolyte with oppositely charged spherical macroions: Giant inversion of charge',
'Independent Ion Migration in Suspensions of Strongly Interacting Charged Colloidal Spheres',
'First-principles study of the polar O-terminated ZnO surface in thermodynamic equilibrium with oxygen and hydrogen',
'Statics and Dynamics of Strongly Charged Soft Matter',
'Screening of a charged particle by multivalent counterions in salty water: Giant charge inversion',
'Model for nucleation in GaAs homoepitaxy derived from first principles',
'Adaptive evolution of transcription factor binding sites',
'Generalized Poland-Scheraga model for DNA hybridization',
'Effects of droplet fluctuations on the scattering of neutrons and light by microemulsions',
'Molecular dynamics simulation of polymer insertion into lipid bilayers',
'Effect of pressure on the phase behavior and structure of water confined between nanoscale hydrophobic and hydrophilic plates',
'First principles study of adsorbed Cu_n (n=1-4) microclusters on MgO(100): structural and electronic properties',
'Induced-Charge Electro-Osmosis',
'Quasispecies evolution in general mean-field landscapes',
'Actin Polymerization Kinetics, Cap Structure and Fluctuations',
'Physical Constraints and Functional Characteristics of Transcription Factor-DNA Interaction',
'Polyelectrolytes in Solution and at Surfaces',
'Protein Adsorption on Lipid Monolayers at their Coexistence Region',
'Nonlinear effects in charge stabilized colloidal suspensions',
'How a Vicinal Layer of Solvent Modulates the Dynamics of Proteins',
'Introduction to the statistical theory of Darwinian evolution',
'Ab initio calculations for bromine adlayers on the Ag(100) and Au(100) surfaces: the c(2x2) structure',
'Inhomogeneous exclusion processes with extended objects: The effect of defect locations',
'Statistical properties of neutral evolution',
'A-Tract Induced DNA Bending is A Local Non-Electrostatic Effect',
'The Physical Origin of Intrinsic Bends in Double Helical DNA',
'Maternal effects in molecular evolution',
'Topological Generalizations of network motifs',
'The Enhancement of Confocal Images of Tissues at Bulk Optical Immersion',
'Roles of stiffness and excluded volume in DNA denaturation',
'Complexation of DNA with positive spheres: phase diagram of charge inversion and reentrant condensation',
'What is the time scale of random sequential adsorption?',
'Lack of self-averaging in neutral evolution of proteins',
'Equilibrium state of molecular breeding',
'Optimal adaptive performance and delocalization in NK fitness landscapes',
'A Minimal Model of B-DNA',
'Screening of a macroion by multivalent ions: Correlation induced inversion of charge',
'Why is the DNA Denaturation Transition First Order?',
'Extinction transition in bacterial colonies under forced convection',
'Mutation-Selection Balance: Ancestry, Load, and Maximum Principle',
'Connectivity of neutral networks and structural conservation in protein evolution',
'Dynamics of Competitive Evolution on a Smooth Landscape',
'Folding Pathways of Prion and Doppel',
'Bottleneck-induced transitions in a minimal model for intracellular transport']

manual_title

from gensim.models import word2vec

# passing the splitted sentences to the model (tokenization) 
tokenized_text_manual= [sentence.split() for sentence in manual_title]
print(tokenized_text_manual)
sentence_vector_manual = word2vec.Word2Vec(tokenized_text_manual, min_count=1)

# summarize the loaded model
print(sentence_vector_manual)
# summarize vocabulary
words = list(sentence_vector_manual.wv.vocab)
print(words)
# access vector for one word
#print(sentence_vector_manual['Topic'])
# save model
sentence_vector_manual.save('model.bin')
# load model
new_model_manual = word2vec.Word2Vec.load('model.bin')
print(list(sentence_vector_manual.wv.vocab))

from sklearn.metrics.pairwise import cosine_similarity
mmr_manual = maximal_marginal_relevance(sentence_vector_manual, manual_title, new_model_manual, lambda_constant=1.0, threshold_terms=5)

mmr_dict_manual = dict(mmr_manual)
manual_tittle_score = {"manual_tittle":[] , "score":[]}

import math
import operator
i=0
for i in range(len(manual_title)):
    manual_title_tokes= manual_title[i].split()
    mmr_score_manual=operator.itemgetter(*manual_title_tokes)(mmr_dict_manual)
    mmr_score_manual=(math.fsum((mmr_score_manual)))
    manual_tittle_score["manual_tittle"].append(manual_title[i])
    manual_tittle_score["score"].append(mmr_score_manual)

for i in range(39):
  # print(str(manual_tittle_score['manual_tittle'][i]) + str(" ---> (Benzerlik: ") + str(manual_tittle_score['score'][i]) + str(")"))
  print(str(manual_tittle_score['manual_tittle'][i]) + str("₺") + str(manual_tittle_score['score'][i]))