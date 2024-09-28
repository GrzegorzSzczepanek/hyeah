class N:
    def __init__(self, data, children=[]):
        self.data = data
        self.children = children

    def print(self, level=0):
        indent = "  " * level
        print(f"{indent}{self.data}")
        for child in self.children:
            child.print(level + 1)


class PCC3:
    def __init__(self):
        DataCzynnosci = {"name": "DataCzynnosci"}
        Pesel = {"name": "Pesel"}
        UrzadSkarbowy = {"name": "UrzadSkarbowy"}
        CelDeklaracji = {"name": "CelDeklaracji"}
        Podmiot = {"name": "Podmiot"}
        RodzajPodatnika = {"name": "RodzajPodatnika"}
        Nazwisko = {"name": "Nazwisko"}
        PierwszeImie = {"name": "PierwszeImie"}
        DataUrodzenia = {"name": "DataUrodzenia"}
        ImieOjca = {"name": "ImieOjca"}
        ImieMatki = {"name": "ImieMatki"}
        Kraj = {"name": "Kraj"}
        Wojewodztwo = {"name": "Wojewodztwo"}
        Powiat = {"name": "Powiat"}
        Gmina = {"name": "Gmina"}
        Miejscowosc = {"name": "Miejscowosc"}
        Ulica = {"name": "Ulica"}
        NrDomu = {"name": "NrDomu"}
        NrLokalu = {"name": "NrLokalu"}
        KodPocztowy = {"name": "KodPocztowy"}
        PrzedmiotOpodatkowania = {"name": "PrzedmiotOpodatkowania"}
        MiejscePolozeniaRzeczy = {"name": "MiejscePolozeniaRzeczy"}
        MiejsceDokonaniaCzynnosci = {"name": "MiejsceDokonaniaCzynnosci"}
        TrescCzynnosci = {"name": "TrescCzynnosci"}
        PodstawaOpodatkowania = {"name": "PodstawaOpodatkowania"}
        StawkaPodatku = {"name": "StawkaPodatku"}
        ObliczonyNaleznyPodatek = {"name": "ObliczonyNaleznyPodatek"}
        KwotaNalaznegoPodatku = {"name": "KwotaNalaznegoPodatku"}
        KwotaPodatkuDoZaplaty = {"name": "KwotaPodatkuDoZaplaty"}
        Pouczenia = {"name": "Pouczenia"}

        self.form = N(
            "root",
            [
                N("SectionA", [N(DataCzynnosci), N(UrzadSkarbowy), N(CelDeklaracji)]),
                N(
                    "SectionB",
                    [
                        N(Podmiot),
                        N(RodzajPodatnika),
                        N(Pesel),
                        N(PierwszeImie),
                        N(Nazwisko),
                        N(DataUrodzenia),
                        N(ImieOjca),
                        N(ImieMatki),
                        N(Kraj),
                        N(Wojewodztwo),
                        N(Powiat),
                        N(Gmina),
                        N(Miejscowosc),
                        N(Ulica),
                        N(NrDomu),
                        N(NrLokalu),
                        N(KodPocztowy),
                    ],
                ),
                N(
                    "SectionC",
                    [
                        N(PrzedmiotOpodatkowania),
                        N(MiejscePolozeniaRzeczy),
                        N(MiejsceDokonaniaCzynnosci),
                        N(TrescCzynnosci),
                    ],
                ),
                N(
                    "SectionD",
                    [
                        N(PodstawaOpodatkowania),
                        N(StawkaPodatku),
                        N(ObliczonyNaleznyPodatek),
                        N(KwotaNalaznegoPodatku),
                    ],
                ),
                N("SectionF", [N(KwotaPodatkuDoZaplaty)]),
                N("Pouczenia", [N(Pouczenia)]),
            ],
        )
        self.form_pointer = (0, 0)

    def next(self):
        x = self.form.children[self.form_pointer[0]].children[self.form_pointer[1]]
        print(self.form_pointer)
        return x

    def fill_data(self, data):
        self.form.children[self.form_pointer[0]].children[self.form_pointer[1]] = data

        if self.form_pointer[1] + 1 < len(
            self.form.children[self.form_pointer[0]].children
        ):
            self.form_pointer = (self.form_pointer[0], self.form_pointer[1] + 1)
        else:
            if self.form_pointer[0] + 1 < len(self.form.children):
                self.form_pointer = (self.form_pointer[0] + 1, 0)
            else:
                return None
        return data


form = PCC3()
form.next().print()
while form.fill_data("dupa") is not None:
    form.next().print()
