class Intersector:
    def __init__(self):
        pass

    def compute_intersection(self, mapping1, mapping2):
        set1 = set(mapping1)
        set2 = set(mapping2)
        intersection = set1 & set2
        return len(intersection)

    
