from collections import defaultdict
import pytest

from code import g
from code.data import load_techs
from code.dirs import create_directories


def setup_module():
    create_directories(True)


@pytest.fixture
def techs():
    load_techs()
    return g.techs.copy()


def test_valid_prerequisites_techs(techs):
    prerequisites_references_valid_techs(techs, g.techs.values(), 'Tech')


def prerequisites_references_valid_techs(techs, prerequisites_list, prerequisite_typename):
    for prereq in prerequisites_list:
        spec = prereq.spec if hasattr(prereq, 'spec') else prereq.type
        conjunction = spec.prerequisites_in_cnf_format()
        if conjunction is None:
            # deliberately marked impossible
            continue
        for disjunction in conjunction:
            for tech_dep_id in disjunction:
                assert '|' not in tech_dep_id, '%s "%s" references unknown dependency tech "%s" (' \
                                               'did you use pre instead of pre_list?)' % (
                                                   prerequisite_typename, prereq.id, tech_dep_id)
                assert tech_dep_id in techs, '%s "%s" references unknown dependency tech "%s"' % (
                    prerequisite_typename, prereq.id, tech_dep_id)
            for keyword in ('impossible', 'OR'):
                assert keyword not in disjunction, 'The keyword "%s" must be the first in a pre_list (%s: "%s")' % (
                    prerequisite_typename, keyword, prereq.id
                )


def test_acyclic_dependencies():
    load_techs()
    techs = g.techs
    waiting_for = defaultdict(list)
    impossible_techs = set()
    researched_techs = set()
    researchable_techs = []

    for tech in techs.values():
        conjunction = tech.type.prerequisites_in_cnf_format()
        if conjunction is None:
            # deliberately marked impossible
            impossible_techs.add(tech.id)
            continue
        if not conjunction:
            researchable_techs.append(tech.id)
            continue
        for disjunction in conjunction:
            for tech_dep_id in disjunction:
                waiting_for[tech_dep_id].append(tech)

    while researchable_techs:
        new_tech = researchable_techs.pop()
        if new_tech in researched_techs:
            continue
        print("Researchable %s" % new_tech)
        researched_techs.add(new_tech)
        techs_waiting = waiting_for[new_tech]
        del waiting_for[new_tech]
        for t in techs_waiting:
            if t.id in researched_techs:
                continue
            conjunction = t.type.prerequisites_in_cnf_format()
            researchable = True
            for disjunction in conjunction:
                if not all(x in researched_techs for x in disjunction):
                    researchable = False
                    break
            if researchable:
                researchable_techs.append(t.id)

    for x, y in waiting_for.items():
        print("%s cannot be researched and is blocking %s" % (x, str(sorted(y))))

    assert not waiting_for
