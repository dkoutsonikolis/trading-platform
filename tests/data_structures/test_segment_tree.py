import pytest
from app.data_structures.segment_tree import SegmentTree, StatsNode
from app.data_structures.exceptions import SegmentTreeCapacityLimitReachedException

@pytest.fixture
def segment_tree():
    return SegmentTree(capacity=10, max_window_size=10)

def test_build_tree(segment_tree):
    data = [1, 2, 3, 4, 5]
    segment_tree.build(data)

    assert segment_tree.size == len(data)
    assert segment_tree.tree[segment_tree.capacity + 0] == StatsNode(1, 1, 1, 1)
    assert segment_tree.tree[segment_tree.capacity + 1] == StatsNode(2, 2, 2, 4)
    assert segment_tree.tree[segment_tree.capacity + 2] == StatsNode(3, 3, 3, 9)
    assert segment_tree.tree[segment_tree.capacity + 3] == StatsNode(4, 4, 4, 16)
    assert segment_tree.tree[segment_tree.capacity + 4] == StatsNode(5, 5, 5, 25)
    assert segment_tree.tree[1] == StatsNode(1, 5, 15, 55)
    

def test_query(segment_tree):
    data = [1, 2, 3, 4, 5]
    segment_tree.build(data)

    result_min, result_max, result_last_num, result_avg, result_var = segment_tree.query(1)

    assert result_min == 1
    assert result_max == 5
    assert result_last_num == 5
    assert result_avg == 3.0
    assert result_var == 2.0

def test_append_data(segment_tree):
    segment_tree.build([1, 2, 3,])

    segment_tree.append_data([4,5])
    segment_tree.append_data([6,7])

    assert segment_tree.size == 7

    assert segment_tree.tree[segment_tree.capacity + 0] == StatsNode(1, 1, 1, 1)
    assert segment_tree.tree[segment_tree.capacity + 1] == StatsNode(2, 2, 2, 4)
    assert segment_tree.tree[segment_tree.capacity + 2] == StatsNode(3, 3, 3, 9)
    assert segment_tree.tree[segment_tree.capacity + 3] == StatsNode(4, 4, 4, 16)
    assert segment_tree.tree[segment_tree.capacity + 4] == StatsNode(5, 5, 5, 25)
    assert segment_tree.tree[segment_tree.capacity + 5] == StatsNode(6, 6, 6, 36)
    assert segment_tree.tree[segment_tree.capacity + 6] == StatsNode(7, 7, 7, 49)

def test_remove_old_data(segment_tree):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    segment_tree.build(data)

    segment_tree.remove_old_data(3)

    assert segment_tree.tree[segment_tree.capacity + 0].min == 4
    assert segment_tree.tree[segment_tree.capacity + 1].min == 5
    assert segment_tree.tree[segment_tree.capacity + 2].min == 6
    assert segment_tree.tree[segment_tree.capacity + 3].min == 7
    assert segment_tree.tree[segment_tree.capacity + 4].min == 8
    assert segment_tree.tree[segment_tree.capacity + 5].min == 9
    assert segment_tree.tree[segment_tree.capacity + 6].min == 10
    assert segment_tree.tree[segment_tree.capacity + 7].min == float('inf')
    assert segment_tree.tree[segment_tree.capacity + 8].min == float('inf')
    assert segment_tree.tree[segment_tree.capacity + 9].min == float('inf')
    

def test_capacity_limit(segment_tree):
    data = [1] * (segment_tree.capacity * 3)

    with pytest.raises(SegmentTreeCapacityLimitReachedException):
        segment_tree.build(data)

    with pytest.raises(SegmentTreeCapacityLimitReachedException):
        segment_tree.append_data(data)

def test_query_empty_tree(segment_tree):
    segment_tree.build([])

    result_min, result_max, result_last_number, result_avg, result_var = segment_tree.query(1)

    assert result_min == float('inf')
    assert result_max == float('-inf')
    assert result_last_number is None
    assert result_avg == 0
    assert result_var == 0

def test_resize():
    segment_tree = SegmentTree(capacity=10, max_window_size=30)
    segment_tree.build([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    segment_tree.append_data([11, 12, 13])

    result_min, result_max, result_last_number, result_avg, result_var = segment_tree.query(1)

    assert result_min == 4
    assert result_max == 13
    assert result_last_number == 13
    assert result_avg == 8.5
    assert result_var == 8.25
