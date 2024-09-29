def calculate_pcc_tax(
    transaction_type,
    amount
):
    """
    Calculate PCC (Podatek od czynności cywilnoprawnych) tax for loan agreements and car purchases.

    Parameters:
    - transaction_type: 'loan' or 'car_purchase'
    - amount: amount of the transaction (value of the loan or market value of the car)

    Returns:
    - tax amount due in PLN
    """

    if transaction_type == 'loan':
        
        if amount <= 1000:
            # Loan amount does not exceed 1000 PLN and lender is outside first tax group
            # Loan is exempt
            return 0.0

        # Standard tax rate for loans is 0.5%
        tax = amount * 0.005
        return tax

    elif transaction_type == 'car_purchase':
        # Check for car purchase exemptions
        if amount <= 1000:
            # Transaction is exempt
            return 0.0

        # Standard tax rate for car purchases is 2%
        tax = amount * 0.02
        return tax

    else:
        raise ValueError("Invalid transaction type. Must be 'loan' or 'car_purchase'.")


def test_anna_loan_scenario():
    # Parameters based on the scenario
    transaction_type = 'loan'
    amount = 20000

    # Calculate the tax
    tax = calculate_pcc_tax(
        transaction_type=transaction_type,
        amount=amount
    )

    # Print the result
    print(f"The PCC tax that Anna needs to pay is: {tax} PLN")

if __name__ == "__main__":
    test_anna_loan_scenario()
