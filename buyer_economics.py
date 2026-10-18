"""Illustrative buyer economics for identity-verification solutions.

All scenario inputs must be validated before being used for an
actual purchasing decision. Released staff capacity is not
automatically equivalent to cash savings.
"""

def calculate_economics(
    annual_reviews,
    reduction_rate,
    loaded_cost_per_review,
    annual_vendor_fee,
    implementation_cost=0.0,
):
    """Calculate annual savings, net benefit and break-even metrics."""

    if annual_reviews < 0:
        raise ValueError("Annual reviews cannot be negative.")

    if not 0 <= reduction_rate <= 1:
        raise ValueError("Reduction rate must be between 0 and 1.")

    if loaded_cost_per_review < 0:
        raise ValueError("Review cost cannot be negative.")

    if annual_vendor_fee < 0 or implementation_cost < 0:
        raise ValueError("Costs cannot be negative.")

    reviews_avoided = annual_reviews * reduction_rate
    gross_labour_savings = (
        reviews_avoided * loaded_cost_per_review
    )

    annual_net_benefit = (
        gross_labour_savings - annual_vendor_fee
    )

    first_year_net_benefit = (
        annual_net_benefit - implementation_cost
    )

    if annual_reviews > 0 and loaded_cost_per_review > 0:
        break_even_reduction_rate = (
            annual_vendor_fee
            / (annual_reviews * loaded_cost_per_review)
        )
        break_even_reduction_rate = min(
            break_even_reduction_rate, float("inf")
        )
    else:
        break_even_reduction_rate = None

    if loaded_cost_per_review > 0:
        reviews_needed_for_recurring_break_even = (
            annual_vendor_fee / loaded_cost_per_review
        )
    else:
        reviews_needed_for_recurring_break_even = None

    return {
        "annual_reviews": annual_reviews,
        "reduction_rate_pct": reduction_rate * 100,
        "reviews_avoided": reviews_avoided,
        "loaded_cost_per_review": loaded_cost_per_review,
        "gross_labour_savings": gross_labour_savings,
        "annual_vendor_fee": annual_vendor_fee,
        "annual_net_benefit": annual_net_benefit,
        "implementation_cost": implementation_cost,
        "first_year_net_benefit": first_year_net_benefit,
        "break_even_reduction_rate_pct": (
            break_even_reduction_rate * 100
            if break_even_reduction_rate is not None
            else None
        ),
        "reviews_needed_for_recurring_break_even": (
            reviews_needed_for_recurring_break_even
        ),
        "cash_savings_validated": False,
        "inputs_validated": False,
    }


def run_sensitivity(
    annual_reviews,
    loaded_cost_per_review,
    annual_vendor_fee,
    implementation_cost,
    reduction_rates=(0.10, 0.25, 0.40),
):
    """Compare hypothetical review-reduction scenarios."""

    return [
        calculate_economics(
            annual_reviews=annual_reviews,
            reduction_rate=rate,
            loaded_cost_per_review=loaded_cost_per_review,
            annual_vendor_fee=annual_vendor_fee,
            implementation_cost=implementation_cost,
        )
        for rate in reduction_rates
    ]
