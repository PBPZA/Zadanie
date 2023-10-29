import numpy as np
import requests
import pandas as pd

import argparse

def main(args):

    def fetching_curr_data(curr):
        request = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/"+curr+"/last/30/?format=json")

        if request.status_code == 200:
            curr_data = request.json()
        else:
            print(f"Fetching data failed, status code: {request.status_code}")
        return (curr_data)

    eur_pln = fetching_curr_data("eur")
    usd_pln = fetching_curr_data("usd")
    chf_pln = fetching_curr_data("chf")

    eur_pln_column = np.array([eur_pln['rates'][i]['mid'] for i in range(len(eur_pln['rates']))])
    usd_pln_column = np.array([usd_pln['rates'][i]['mid'] for i in range(len(usd_pln['rates']))])
    chf_pln_column = np.array([chf_pln['rates'][i]['mid'] for i in range(len(chf_pln['rates']))])
    eur_usd_column = eur_pln_column/usd_pln_column
    chf_usd_column = chf_pln_column/usd_pln_column
    dates = [eur_pln['rates'][i]['effectiveDate'] for i in range(len(eur_pln['rates']))]

    data = {
        'Date': dates,
        'EUR/PLN': eur_pln_column,
        'USD/PLN': usd_pln_column,
        'CHF/PLN': chf_pln_column,
        'EUR/USD': eur_usd_column,
        'CHF/USD': chf_usd_column
        }

    df = pd.DataFrame(data)
    df = df.round(4)

    df.set_index("Date", inplace = True)

    print('Printing all currencies')
    print(df)



    def access_pairs():

        pairs = []

        while True:
            print("Valid pairs are EUR/PLN, USD/PLN, CHF/PLN, EUR/USD, CHF/USD, (to quit enter 'q'): ")
            pair = input("Enter a valid currency pair to access or 'q' to quit: ")

            if pair in ['q', 'EUR/PLN', 'USD/PLN', 'CHF/PLN', 'EUR/USD', 'CHF/USD']:
                print("Valid input")
                if pair == 'q':
                    break
                pairs.append(pair)
            else:
                print("Invalid input")

        pairs = list(set(pairs))


        selected_columns = df[pairs]
        print(selected_columns)
    if args.ac:
        access_pairs()

    ###Export the 5 column dataframe to csv- overwriting the file only with new entries

    try:
        existing_data = pd.read_csv('all_currency_data.csv')
        existing_data.set_index("Date", inplace = True)
        existing_data = existing_data.round(4)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    new_data = pd.concat([existing_data, df])
    new_data = new_data.drop_duplicates(keep = 'first')

    new_data.to_csv('all_currency_data.csv')

    print("Data for all currency pairs has been saved!")



    #Function to permit the saving of user-selected currency pairs to a CSV file
    def choose_pairs():
        pairs = []

        while True:
            print("Valid pairs are EUR/PLN, USD/PLN, CHF/PLN, EUR/USD, CHF/USD, (to quit enter 'q'): ")
            pair = input("Enter a valid currency pair to save or 'q' to quit: ")
            print('Valid input')
            if pair in ['q', 'EUR/PLN', 'USD/PLN', 'CHF/PLN', 'EUR/USD', 'CHF/USD']:
                if pair == 'q':
                    break
                pairs.append(pair)
            else:
                print("Invalid input")

        pairs = list(set(pairs))
        selected_columns = df[pairs]
        selected_columns.to_csv('selected_currency_data.csv')
        print("Data for "+str(pairs)+" has been saved!")
    if args.ch:
        choose_pairs()



    def data_analysis():
        pairs = []

        while True:
            print("Valid pairs are EUR/PLN, USD/PLN, CHF/PLN, EUR/USD, CHF/USD, (to quit enter 'q'): ")
            pair = input("Enter a valid currency pair to analyze or 'q' to quit: ")
            print('Valid input')
            if pair in ['q', 'EUR/PLN', 'USD/PLN', 'CHF/PLN', 'EUR/USD', 'CHF/USD']:
                if pair == 'q':
                    break
                pairs.append(pair)
            else:
                print("Invalid input")

        pairs = list(set(pairs))

        selected_columns = df[pairs]

        summary = pd.DataFrame({
        'Mean': selected_columns.mean(),
        'Median': selected_columns.median(),
        'Maximum': selected_columns.max(),
        'Minimum': selected_columns.min()
        })

        print(summary)
    if args.da:
        data_analysis()






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #flag to be able to choose pairs to access
    parser.add_argument('-ac', action='store_true')
    #flag to be able to choose pairs to save
    parser.add_argument('-ch', action='store_true')
    #flag to be able to choose pairs to analyze
    parser.add_argument('-da', action='store_true')

    args = parser.parse_args()


    main(args)