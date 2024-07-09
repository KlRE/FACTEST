from yices import *
import numpy as np

def segment_intersects_rectangle_yices(p1, p2, Ao, bo):
    cfg = Config()
    cfg.default_config_for_logic('QF_LRA')
    ctx = Context(cfg)

    x_dim = len(p1)
    constraints = []

    # Add constraints for each edge of the rectangle
    for row in range(len(Ao)):
        a = Ao[row]
        b = bo[row][0]

        # Rectangle edge: a*x <= b
        lhs_p1 = sum(a[dim] * p1[dim] for dim in range(x_dim))
        lhs_p2 = sum(a[dim] * p2[dim] for dim in range(x_dim))

        fmla1 = Terms.arith_leq_atom(lhs_p1, Terms.integer(b))
        fmla2 = Terms.arith_leq_atom(lhs_p2, Terms.integer(b))

        constraints.append(fmla1)
        constraints.append(fmla2)

    # Add constraint to ensure line segment is within rectangle bounds
    for dim in range(x_dim):
        min_val = min(p1[dim], p2[dim])
        max_val = max(p1[dim], p2[dim])
        constraints.append(Terms.arith_geq_atom(Terms.integer(max_val), Terms.select(Terms.new_uninterpreted_term(Types.real_type()), dim)))
        constraints.append(Terms.arith_leq_atom(Terms.integer(min_val), Terms.select(Terms.new_uninterpreted_term(Types.real_type()), dim)))

    # Assert the conjunction of all constraints
    ctx.assert_formulas(constraints)

    # Check satisfiability
    status = ctx.check_context()

    ctx.dispose()

    return status == Status.SAT

# Example usage
p1 = [0, 0]
p2 = [1, 1]

Ao = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
bo = np.array([[-1], [2], [-1], [2]])

intersects = segment_intersects_rectangle_yices(p1, p2, Ao, bo)
print(f"Segment [{p1}, {p2}] intersects with rectangle: {intersects}")
