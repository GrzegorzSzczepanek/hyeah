LOAN_TAX_RATE = 0.005
CAR_PURCHASE_TAX_RATE = 0.02

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
            
            return 0.0

        tax = amount * LOAN_TAX_RATE
        return tax

    elif transaction_type == 'car_purchase':
        if amount <= 1000:
            return 0.0

        tax = amount * CAR_PURCHASE_TAX_RATE
        return tax

    else:
        raise ValueError("Invalid transaction type. Must be 'loan' or 'car_purchase'.")


def test_anna_loan_scenario():

    transaction_type = 'loan'
    amount = 20000

    tax = calculate_pcc_tax(
        transaction_type=transaction_type,
        amount=amount
    )
    print(f"The PCC tax that Anna needs to pay is: {tax} PLN")

if __name__ == "__main__":
    test_anna_loan_scenario()
