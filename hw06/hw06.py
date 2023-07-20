class Mint:
    """A mint creates coins by stamping on years.

    The update method sets the mint's stamp to Mint.present_year.

    >>> mint = Mint()
    >>> mint.year
    2022
    >>> dime = mint.create(Dime)
    >>> dime.year
    2022
    >>> Mint.present_year = 2102  # Time passes
    >>> nickel = mint.create(Nickel)
    >>> nickel.year     # The mint has not updated its stamp yet
    2022
    >>> nickel.worth()  # 5 cents + (80 - 50 years)
    35
    >>> mint.update()   # The mint's year is updated to 2102
    >>> Mint.present_year = 2177     # More time passes
    >>> mint.create(Dime).worth()    # 10 cents + (75 - 50 years)
    35
    >>> Mint().create(Dime).worth()  # A new mint has the current year
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)
    115
    >>> Dime.cents = 20  # Upgrade all dimes!
    >>> dime.worth()     # 20 cents + (155 - 50 years)
    125
    """
    present_year = 2022

    def __init__(self):
        self.update()

    def create(self, coin):
        return coin(self.year)

    def update(self):
        self.year = Mint.present_year


class Coin:
    cents = None  # will be provided by subclasses, but not by Coin itself

    def __init__(self, year):
        self.year = year

    def worth(self):
        # print(self.cents, Mint.present_year, self.year)
        if Mint.present_year <= self.year + 50:
            return self.cents
        else:  # 这地方出现报错的原因我觉得是在父类Coin中他并不知道子类已经重写了cents使其可以被运算了
            return self.cents + Mint.present_year - self.year - 50


class Nickel(Coin):
    cents = 5


class Dime(Coin):
    cents = 10


def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> # a check for restricted functions
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    """
    if n < 10:
        return Link(n)
    else:
        # 太丑了，我不知道还有没有别的方式求，或者是说这道题的目的不是考虑正向递归？
        tmp = n
        lenth = 0
        while tmp > 10:
            lenth += 1
            tmp //= 10
        first = tmp
        without_first = n - first*pow(10, lenth)
        # print(first, without_first)
        return Link(first, store_digits(without_first))


def deep_map_mut(func, lnk):
    """Mutates a deep link lnk by replacing each item found with the
    result of calling func on the item.  Does NOT create new Links (so
    no use of Link's constructor).

    Does not return the modified Link object.

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> # Disallow the use of making new Links before calling deep_map_mut
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    if isinstance(lnk, Link):
        if isinstance(lnk.first, (int, float)):
            lnk.first = func(lnk.first)
            if isinstance(lnk.rest, Link):
                deep_map_mut(func, lnk.rest)
        elif isinstance(lnk.first, Link):
            deep_map_mut(func, lnk.first)
            if isinstance(lnk.rest, Link):
                deep_map_mut(func, lnk.rest)


def two_list(vals, counts):
    """
    Returns a linked list according to the two lists that were passed in. Assume
    vals and counts are the same size. Elements in vals represent the value, and the
    corresponding element in counts represents the number of this value desired in the
    final linked list. Assume all elements in counts are greater than 0. Assume both
    lists have at least one element.

    >>> a = [1, 3, 2]
    >>> b = [1, 1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3, Link(2)))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
    """
    # res是所有的头指针，pre是跟着移动的辅助指针
    # 之前应该是通常用的dummy node,虚拟指针，最后返回一个res.rest即可，这样可以省略最开始的节点判断
    res = None
    pre = None
    for val, cnt in zip(vals, counts):
        for _ in range(cnt):
            cur = Link(val)
            # 首节点刚出现
            if res is None and pre is None:
                res = cur
                pre = res
            elif res is not None and pre is not None:
                pre.rest = cur
                pre = cur
    return res


class VirFib():
    """A Virahanka Fibonacci number.

    >>> start = VirFib()
    >>> start
    VirFib object, value 0
    >>> start.next()
    VirFib object, value 1
    >>> start.next().next()
    VirFib object, value 1
    >>> start.next().next().next()
    VirFib object, value 2
    >>> start.next().next().next().next()
    VirFib object, value 3
    >>> start.next().next().next().next().next()
    VirFib object, value 5
    >>> start.next().next().next().next().next().next()
    VirFib object, value 8
    >>> start.next().next().next().next().next().next() # Ensure start isn't changed
    VirFib object, value 8
    """
    # 保留前一个状态，方式就是指针指向前一个的位置

    def __init__(self, value=0):
        self.value = value
        self.pre = None

    def next(self):
        if self.pre is None:
            new_value = 1
        else:
            new_value = self.value + self.pre.value
        new_fib = VirFib(new_value)
        new_fib.pre = self
        return new_fib

    def __repr__(self):
        return "VirFib object, value " + str(self.value)


def is_bst(t):
    """Returns True if the Tree t has the structure of a valid BST.

    >>> t1 = Tree(6, [Tree(2, [Tree(1), Tree(4)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t1)
    True
    >>> t2 = Tree(8, [Tree(2, [Tree(9), Tree(1)]), Tree(3, [Tree(6)]), Tree(5)])
    >>> is_bst(t2)
    False
    >>> t3 = Tree(6, [Tree(2, [Tree(4), Tree(1)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t3)
    False
    >>> t4 = Tree(1, [Tree(2, [Tree(3, [Tree(4)])])])
    >>> is_bst(t4)
    True
    >>> t5 = Tree(1, [Tree(0, [Tree(-1, [Tree(-2)])])])
    >>> is_bst(t5)
    True
    >>> t6 = Tree(1, [Tree(4, [Tree(2, [Tree(3)])])])
    >>> is_bst(t6)
    True
    >>> t7 = Tree(2, [Tree(1, [Tree(5)]), Tree(4)])
    >>> is_bst(t7)
    False
    """
    # 真的是及其丑陋，在写left和right的时候，返回的是一个[]，然后还要判断长度来确定到底是不是只有一个儿子
    # 我现在觉得如果只是用题目的Tree类那真的不知道还有什么其他优雅的写法了
    # 还是大致说一下思路：根据hint,先写两个bst_min,bst_max得到一个树的最小/大值方便和cur node比较
    # 注意不管任何时候，只要涉及到左右节点的时候，就要判断是不是有这两个东西
    # 还有注意一下judge函数里面的返回条件，比较多，实际拆分后就是大小关系是否满足，左右孩子是不是也满足judge
    # 需要注意的就是只有一个节点的时候既可以是左孩，也可以是右孩，因此要注意返回条件的不同
    def bst_min(tree):
        if tree.is_leaf():
            return tree.label
        else:
            left = tree.branches[0] if len(tree.branches) >= 1 else None
            right = tree.branches[1] if len(tree.branches) == 2 else None
            if left is None:
                return float('inf')
            if right is None:
                return min(tree.label, bst_min(left))
            return min(tree.label, bst_min(left), bst_min(right))

    def bst_max(tree):
        if tree.is_leaf():
            return tree.label
        else:
            left = tree.branches[0] if len(tree.branches) >= 1 else None
            right = tree.branches[1] if len(tree.branches) == 2 else None
            if left is None:
                return float('-inf')
            if right is None:
                return max(tree.label, bst_max(left))
            return max(tree.label, bst_max(left), bst_max(right))

    def judge(tree):
        if tree is None:
            return True
        if tree.is_leaf():
            return True
        else:
            left = tree.branches[0] if len(tree.branches) >= 1 else None
            right = tree.branches[1] if len(tree.branches) == 2 else None
            if left is not None and right is None:
                return (tree.label >= bst_max(left) or tree.label < bst_min(left)) and judge(left)
            return bst_max(left) <= tree.label < bst_min(right) and judge(left) and judge(right)

    return judge(t)


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'


class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """

    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()
