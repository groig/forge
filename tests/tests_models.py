import pytest

# Not using relative imports bc some stupid pytest conflict
from forge.models import Data, Structure

from .fixtures import FULL_STRUCTURE_VALID


@pytest.fixture
def structure(admin_user):
    return Structure.objects.create(name='test structure', structure=FULL_STRUCTURE_VALID, created_by=admin_user)


@pytest.fixture(scope='module')
def data():
    return {"first_name": "asdads"}


def test_data_manager_structureless(data, admin_user): # pylint: disable=redefined-outer-name
    data_object = Data.objects.create(created_by=admin_user, data=data)
    assert Data.objects.structureless()[0].id == data_object.id
    Data.objects.create(created_by=admin_user, data=data)
    assert len(Data.objects.structureless()) == 2

def test_data_manager_orphans(data, admin_user): # pylint: disable=redefined-outer-name
    data_parent = Data.objects.create(created_by=admin_user, data=data)
    data_child1 = Data.objects.create(created_by=admin_user, data=data, parent=data_parent)
    data_child2 = Data.objects.create(created_by=admin_user, data=data, parent=data_parent)
    data_parent.delete()
    assert len(Data.objects.orphans()) == 2
    assert data_child1 in Data.objects.orphans()
    assert data_child2 in Data.objects.orphans()
