from collections import defaultdict
from dataclasses import dataclass
from app import app
from app.data_structures.exceptions import SegmentTreeCapacityLimitReachedException


@dataclass(frozen=True)
class StatsNode:
    """A data structure representing a segment tree node storing statistical data."""
    min: float
    max: float
    sum: float
    sum_of_squares: float
    
    @staticmethod
    def empty() -> 'StatsNode':
        return StatsNode(min=float('inf'), max=float('-inf'), sum=0, sum_of_squares=0)


class SegmentTree:
    def __init__(
        self, 
        capacity: int | None = 10 ** 2,
        max_window_size: int | None = 10 **8,
        capacity_buffer_factor: float | None = 1.2
    ):
        """
        Initializes a SegmentTree.

        Parameters:
        - capacity: The total capacity of the segment tree
        - max_window_size: The maximum window size for which we need to provide stats.
        - capacity_buffer_factor: a factor that determines how much more storage (as a percentage) 
                          to allocate beyond the initial capacity. A capacity_buffer of 1.2 
                          means the total capacity will be 120% of the initial capacity, 
                          providing a 20% buffer for potential future growth.

        Attributes:
        - size: The current size of the segment tree, initialized to 0.
        - tree: The internal array representing the segment tree. The array is structured such that:
          - The leaf nodes (representing the actual data) are stored in the second half of the array.
          - The internal nodes (representing merged data from the leaves) are stored in the first half of the array.
          - The size of the array is `2 * capacity`, providing sufficient space for both leaves and internal nodes.

        """
        self.size = 0 
        self.capacity = capacity
        self.max_window_size = max_window_size
        self.capacity_limit = self.max_window_size * capacity_buffer_factor
        self.tree = [StatsNode.empty()] * (2 * self.capacity) 

    def _resize(self) -> None:
        """Resize the tree array when it exceeds current capacity."""
        new_capacity = self.capacity * 10
    
        new_tree = SegmentTree(capacity=new_capacity)
        new_tree.build([data_leaf.min for data_leaf in self.tree[self.capacity:]])
        
        self.tree = new_tree.tree
        self.capacity = new_capacity

    def _build_internal_nodes(self):
        """
            Build internal nodes (statistical information)
        """
        for i in range(self.capacity - 1, 0, -1):
            left = self.tree[i * 2]
            right = self.tree[i * 2 + 1]
            self.tree[i] = StatsNode(
                min(left.min, right.min),
                max(left.max, right.max),
                left.sum + right.sum,
                left.sum_of_squares + right.sum_of_squares
            )

    def build(self, data: list[float]) -> None:
        self.size = len(data)

        if self.size > self.capacity_limit:
            raise SegmentTreeCapacityLimitReachedException()
        
        while self.size > self.capacity:
            self._resize()
        
        for i in range(self.size):
            self.tree[self.capacity + i] = StatsNode(data[i], data[i], data[i], data[i] ** 2)

        self._build_internal_nodes()

    def append_data(self, new_data: list[float]) -> None:
        new_size = self.size + len(new_data)

        if new_size > self.capacity_limit:
            raise SegmentTreeCapacityLimitReachedException()

        while new_size > self.capacity:
            self._resize()

        if new_size > self.max_window_size:
            excess_data = new_size - self.max_window_size
            self.remove_old_data(excess_data)

        for i in range(len(new_data)):
            self.tree[self.capacity + self.size + i] = StatsNode(new_data[i], new_data[i], new_data[i], new_data[i] ** 2)

        self.size += len(new_data)

        self._build_internal_nodes()

    def remove_old_data(self, count_to_remove: int) -> None:
        """Remove old data when max size is exceeded."""

        # Shift the leaf nodes left
        for i in range(self.capacity + count_to_remove, self.capacity + self.size):
            self.tree[i - count_to_remove] = self.tree[i]
            self.tree[i] = StatsNode.empty()

        self.size -= count_to_remove 

        self._build_internal_nodes()

    def query(self, k: int) -> tuple[float, float, float, float]:
        """
        Queries the last 10^k elements of the segment tree for statistical data.

        Args:
            k: The exponent defining the range of data to query. 
            For example, k=1 queries the last 10 elements, k=2 queries the last 100 elements, etc.

        Returns:
            A tuple containing:
                - Minimum value in the range.
                - Maximum value in the range.
                - Last number in the range.
                - Average value in the range.
                - Variance in the range.
        """
        num_elements = 10 ** k
        
        start_idx = max(self.size - num_elements, 0)
        
        l = self.capacity + start_idx
        r = self.capacity + self.size - 1
        
        result_min, result_max = float('inf'), float('-inf')
        result_sum, result_sum_of_squares = 0, 0
        count = r - l + 1
        last_number = self.tree[r].min if self.size > 0 else None
        
        # Traverse and query the segment tree from `l` to `r`
        while l <= r:
            if l % 2 == 1:
                result_min = min(result_min, self.tree[l].min)
                result_max = max(result_max, self.tree[l].max)
                result_sum += self.tree[l].sum
                result_sum_of_squares += self.tree[l].sum_of_squares
                l += 1
            if r % 2 == 0:
                result_min = min(result_min, self.tree[r].min)
                result_max = max(result_max, self.tree[r].max)
                result_sum += self.tree[r].sum
                result_sum_of_squares += self.tree[r].sum_of_squares
                r -= 1
            l //= 2
            r //= 2

        mean = round(result_sum / count, 2) if count > 0 else 0
        variance = round((result_sum_of_squares / count) - (mean ** 2), 2) if count > 0 else 0
        
        return result_min, result_max, last_number, mean, variance

        

