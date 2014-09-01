# constants.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on 2014-08-21.
#
# Please see the license info in the root folder of this package.

"""
=================================================
constants.py
=================================================
Purpose:
a place to store/generate conversion dictionaries and other useful things
needed across the whole package.

"""

__author__ = 'Gus Dunn'

import csv

from bunch import Bunch

from pkg_resources import Requirement, resource_filename


infection_status_conversion = {"TENERAL": "not dissected",
                               "DEAD": "not dissected",
                               "negative": "negative",
                               "-": "negative",
                               "0": "negative",
                               "+": "positive",
                               "1": "positive",
                               "positive": "positive", }

species_names = ['Glossina fuscipes fuscipes',
                 'Glossina morsitans morsitans',
                 'Glossina pallidipes']


def get_species_abbrv_conversion_dict():
    """
    Generates and returns a `dict` mapping of common abbreviations of Glossina
    species names to the full name. Generated from `tsetseDB.utils.constants.species_names`.

    :return: `dict`
    """
    conv_dict = {}
    for name in species_names:

        # species_abbrv_funcs defined near the bottom of the page
        for f in species_abbrv_funcs.values():
            abbrv = f(name)
            if abbrv is not None:
                conv_dict[abbrv] = name
            else:
                continue

    return conv_dict


village_id_map_path = resource_filename(Requirement.parse("tsetseDB"), "data/village_id_map.csv")


def get_village_id_map():
    """
    Generates and returns a `dict` mapping the two-way mappings of long-form village names
    and their unique 2 or 3 letter id symbols.
    :return: `dict`
    """

    village_id_map = {}

    with open(village_id_map_path, 'rb') as csv_file:
        village_ids = csv.reader(csv_file, delimiter=',')
        for pair in village_ids:
            village_id_map[pair[0]] = pair[1]
            village_id_map[pair[1]] = pair[0]

    return village_id_map


def get_village_ids():
    """
    Returns `set` of village ID strings
    :return: `set`
    """
    village_ids = []

    with open(village_id_map_path, 'rb') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        for pair in rows:
            village_ids.append(pair[0])

    return set(village_ids)


def get_village_names():
    """
    Returns `set` of village NAME strings
    :return: `set`
    """
    village_names = []

    with open(village_id_map_path, 'rb') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        for pair in rows:
            village_names.append(pair[1])

    return set(village_names)













#################################################################################
### species_abbrv_func definitions ##############################################
#################################################################################

species_abbrv_funcs = Bunch()


def species_abbrv_func_G_x(name):
    """
    Given: 'Glossina fuscipes fuscipes'
    Returns: 'G.f'

    :param name: species name as `str`
    :return: `str`
    """
    words = name.split()
    abbrv = []

    for i, word in enumerate(words):
        if i != 2:
            abbrv.append("%s." % (word[0]))
        else:
            continue

    return ''.join(abbrv)

species_abbrv_funcs.species_abbrv_func_G_x = species_abbrv_func_G_x


def species_abbrv_func_Gx(name):
    """
    Given: 'Glossina fuscipes fuscipes'
    Returns: 'Gf'

    :param name: species name as `str`
    :return: `str`
    """
    words = name.split()
    abbrv = []

    for i, word in enumerate(words):
        if i != 2:
            abbrv.append("%s" % (word[0]))
        else:
            continue

    return ''.join(abbrv)

species_abbrv_funcs.species_abbrv_func_Gx = species_abbrv_func_Gx

def species_abbrv_func_G_xx(name):
    """
    Given: 'Glossina fuscipes fuscipes'
    Returns: 'G.ff'

    :param name: species name as `str`
    :return: `str`
    """
    words = name.split()
    abbrv = []

    for i, word in enumerate(words):
        if i == 0:
            abbrv.append("%s." % (word[0]))
        else:
            abbrv.append("%s" % (word[0]))

    return ''.join(abbrv)

species_abbrv_funcs.species_abbrv_func_G_xx = species_abbrv_func_G_xx


def species_abbrv_func_GXX(name):
    """
    Given: 'Glossina fuscipes fuscipes'
    Returns: 'GFF'

    :param name: species name as `str`
    :return: `str`
    """
    words = name.split()
    abbrv = []

    for i, word in enumerate(words):
        abbrv.append("%s" % (word[0].upper()))

    return ''.join(abbrv)

species_abbrv_funcs.species_abbrv_func_GXX = species_abbrv_func_GXX


def species_abbrv_func_Gxx(name):
    """
    Given: 'Glossina fuscipes fuscipes'
    Returns: 'Gff'

    :param name: species name as `str`
    :return: `str`
    """
    words = name.split()
    abbrv = []

    for i, word in enumerate(words):
        abbrv.append("%s" % (word[0]))

    return ''.join(abbrv)

species_abbrv_funcs.species_abbrv_func_Gxx = species_abbrv_func_Gxx


def species_abbrv_func_G_x_x(name):
    """
    Given: 'Glossina fuscipes fuscipes'
    Returns: 'G.f.f.'

    :param name: species name as `str`
    :return: `str`
    """
    words = name.split()
    abbrv = []

    for i, word in enumerate(words):
        abbrv.append("%s." % (word[0]))

    return ''.join(abbrv)

species_abbrv_funcs.species_abbrv_func_G_x_x = species_abbrv_func_G_x_x


def species_abbrv_func_G_pd(name):
    """
    **Special Case**
    Given: 'Glossina pallidipes'
    Returns: 'G.pd'

    :param name: species name as `str`
    :return: `str`
    """
    if name == 'Glossina pallidipes':
        return 'G.pd'


species_abbrv_funcs.species_abbrv_func_G_pd = species_abbrv_func_G_pd