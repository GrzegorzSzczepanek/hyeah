import os
import json

class TerytValidator:
    
    def __init__(self, teryt_data):
        """Inicjalizacja z dostępem do pełnych danych TERYT."""
        self.teryt_data = teryt_data

    # Weryfikacja danych TERC
    def validate_terc(self, woj: str = None, pow: str = None, gmi: str = None, rodz: str = None) -> bool:
        """
        Weryfikuj dane TERC (jednostki administracyjne). Sprawdza województwo, powiat, gminę i rodzaj.
        Można przekazać dowolną kombinację parametrów.
        """
        for row in self.teryt_data['TERC']:
            if (woj and row['WOJ'] != woj) or (pow and row['POW'] != pow) or (gmi and row['GMI'] != gmi) or (rodz and row['RODZ_GMI'] != rodz):
                continue
            return True  # Znaleziono zgodne dane
        return False  # Brak zgodnych danych
    
    # Weryfikacja danych SIMC
    def validate_simc(self, woj: str = None, pow: str = None, gmi: str = None, symbol: str = None, nazwa: str = None) -> bool:
        """
        Weryfikuj dane SIMC (miejscowości). Można przekazać dowolną kombinację parametrów.
        """
        for row in self.teryt_data['SIMC']:
            if (woj and row['WOJ'] != woj) or (pow and row['POW'] != pow) or (gmi and row['GMI'] != gmi) or (symbol and row['SYM'] != symbol) or (nazwa and row['NAZWA'] != nazwa):
                continue
            return True
        return False
    
    # Weryfikacja danych ULIC
    def validate_ulic(self, woj: str = None, pow: str = None, gmi: str = None, symbol_ul: str = None, nazwa_ul: str = None) -> bool:
        """
        Weryfikuj dane ULIC (ulice). Można przekazać dowolną kombinację parametrów.
        """
        for row in self.teryt_data['ULIC']:
            if (woj and row['WOJ'] != woj) or (pow and row['POW'] != pow) or (gmi and row['GMI'] != gmi) or (symbol_ul and row['SYM_UL'] != symbol_ul) or (nazwa_ul and row['NAZWA1'] != nazwa_ul):
                continue
            return True
        return False
    
    # Weryfikacja danych WMRODZ
    def validate_wmrodz(self, rodzaj_miejscowosci: str = None, nazwa_rodzaju: str = None) -> bool:
        """
        Weryfikuj dane WMRODZ (rodzaje miejscowości). Można przekazać dowolną kombinację parametrów.
        """
        for row in self.teryt_data['WMRODZ']:
            if (rodzaj_miejscowosci and row['RM'] != rodzaj_miejscowosci) or (nazwa_rodzaju and row['NAZWA_RM'] != nazwa_rodzaju):
                continue
            return True
        return False
    
    # Weryfikacja wszystkich danych naraz
    def validate_all(self, terc_params=None, simc_params=None, ulic_params=None, wmrodz_params=None) -> bool:
        """
        Weryfikacja wszystkich typów danych naraz. Każdy rodzaj danych można zweryfikować poprzez przekazanie odpowiednich parametrów.
        """
        terc_valid = self.validate_terc(**terc_params) if terc_params else True
        simc_valid = self.validate_simc(**simc_params) if simc_params else True
        ulic_valid = self.validate_ulic(**ulic_params) if ulic_params else True
        wmrodz_valid = self.validate_wmrodz(**wmrodz_params) if wmrodz_params else True
        
        return terc_valid and simc_valid and ulic_valid and wmrodz_valid
    
    def znajdz_numer_z_adresu(self,woj, powiat, gmina, ulica=None):
        """
        Znajdź numer identyfikacyjny jednostki administracyjnej na podstawie adresu.
        
        :param woj: Nazwa województwa.
        :param powiat: Nazwa powiatu.
        :param gmina: Nazwa gminy.
        :param ulica: Nazwa ulicy (opcjonalnie).
        :return: Numer identyfikacyjny jednostki administracyjnej.
        """


        for jednostka in self.teryt_data["TERC"]:  # Zakładamy, że dane o województwach są w zbiorze TERC
            if (jednostka["WOJ"] == woj and
                jednostka["POW"] == powiat and
                jednostka["GMI"] == gmina):
                
                if ulica:
                    # Sprawdzenie ulicy (jeśli dostępna)
                    for ulica_obj in self.teryt_data["ULIC"]:
                        if ulica_obj["NAZWA_2"] == ulica:
                            return ulica_obj["SYM_UL"]  # Zwróć identyfikator ulicy
                
                return jednostka["SYM"]  # Zwróć identyfikator jednostki terytorialnej
        
        return "Adres nie znaleziony"

    def load_teryt_data(self, file_path: str):
        """Ładuje dane TERYT z jednego pliku JSON i rozdziela wartości kluczowe."""
        teryt_data = {}
        
        # Define the expected structure for each type
        structure_mapping = {
            'TERC': ['WOJ', 'POW', 'GMI', 'RODZ', 'NAZWA', 'NAZWA_DOD', 'STAN_NA'],
            'SIMC': ['WOJ', 'POW', 'GMI', 'RODZ_GMI', 'RM', 'NAZWA', 'SYM', 'SYMPOD', 'STAN_NA'],
            'ULIC': ['WOJ', 'POW', 'GMI', 'SYM_UL', 'CECHA', 'NAZWA1', 'NAZWA2', 'STAN_NA'],
            'WMRODZ': ['RM', 'NAZWA_RM', 'STAN_NA']
        }
        
        with open(file_path, 'r', encoding='utf-8') as json_file:
            raw_data = json.load(json_file)

            for key, rows in raw_data.items():
                if key in structure_mapping:
                    headers = structure_mapping[key]
                    processed_data = []
                    
                    for row in rows:
                        # Get the single string value and split by semicolon
                        values = list(row.values())[0].split(';')
                        
                        # Map the split values to the correct header keys
                        processed_row = dict(zip(headers, values))
                        processed_data.append(processed_row)
                    
                    # Store the processed data in the teryt_data dictionary
                    teryt_data[key] = processed_data
        
        self.teryt_data = teryt_data
        print(f"Dane TERYT załadowano pomyślnie z {file_path}.")



# # Usage example:
# teryt_validator = TerytValidator({})
# teryt_validator.load_teryt_data('./Data')

# # Now you can validate
# is_valid = teryt_validator.validate_terc(woj='12', pow='03', gmi='01', rodz='2')
# print(f"Validation result: {is_valid}")
# is_valid = teryt_validator.validate_terc(woj='2', pow='12', gmi='03', rodz='4')
# print(f"Validation result: {is_valid}")

# Usage example for administration ID:
teryt_validator = TerytValidator({})
teryt_validator.load_teryt_data('./Data/merged_teryt_data.json')

wojewodztwo = "2"
powiat = "04"
gmina = "12"
ulica = "Słowackiego"

numer = teryt_validator.znajdz_numer_z_adresu(wojewodztwo, powiat, gmina, ulica)
print(f"Numer identyfikacyjny dla adresu to: {numer}")